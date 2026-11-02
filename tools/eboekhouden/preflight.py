"""Private, read-only prebooking report. No registration/account writes."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area, live_connection

import argparse
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import http.client
import json
from pathlib import Path
import re
import ssl
import sys
import unicodedata
from urllib.parse import urlencode
import uuid

import certifi

ROOT = runtime_area("prebooking")
import app_probe as app
import probe_rest as rest
from credential_store import CredentialStore, CredentialFailure, WindowsBackend

MAX_CALLS = 300
MONEY = Decimal("0.01")


def money(value):
    return Decimal(str(value)).quantize(MONEY, rounding=ROUND_HALF_UP)


def iso_date(value):
    if isinstance(value, (int, float)):
        return (date(1899, 12, 30) + timedelta(days=int(value))).isoformat()
    return date.fromisoformat(str(value)[:10]).isoformat()


def table(snapshot, name):
    values = snapshot["ranges"][name]["values"]
    return [dict(zip(values[0], row + [""] * (len(values[0]) - len(row))))
            for row in values[1:] if any(cell not in ("", None) for cell in row)]


def normalize(value):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower())


def aliases(name):
    result = [name] + re.split(r"\s+/\s+", name)
    result += re.findall(r"\(([^)]+)\)", name)
    return list(dict.fromkeys(value.strip() for value in result if value.strip()))[:3]


def query(path, **parameters):
    return path + "?" + urlencode(parameters)


def mutation_query(number, offset):
    return query("/v1/mutation", invoiceNumber=str(number), limit=20, offset=offset)


def relation_queries(name):
    result = [query("/v1/relation", name=value, limit=5, offset=0) for value in aliases(name)]
    tokens = re.findall(r"[A-Za-z0-9]{4,}", name)
    if tokens:
        result.append(query("/v1/relation", **{"name[like]": "%" + tokens[0] + "%", "limit": 5, "offset": 0}))
    return result


class Client:
    def __init__(self, invoices, policy, factory=http.client.HTTPSConnection):
        self.factory = factory
        self.calls = 0
        self.token = None
        self.bearer = False
        self.secrets = []
        self.detail_paths = set()
        self.paths = {query("/v1/ledger", limit=200, offset=offset) for offset in range(0, 2000, 200)}
        self.paths |= {mutation_query(inv["factuurnummer"], offset) for inv in invoices for offset in (0, 20, 40)}
        self.paths |= {path for inv in invoices for path in relation_queries(inv["leverancier_naam"])}
        codes = [policy["acceptedAmazonCentralCode"]] + [hint["code"] for hint in policy.get("relationHints", [])]
        self.paths |= {query("/v1/relation", code=code, limit=5, offset=0) for code in codes}

    def request(self, method, path, body=None):
        login = method == "POST" and path == "/v1/session" and isinstance(body, dict) and set(body) == {"accessToken", "source"} and body["source"] == "MBProbe"
        logout = method == "DELETE" and path == "/v1/session" and body is None
        reading = method == "GET" and body is None and path in self.paths | self.detail_paths
        if not (login or logout or reading):
            raise app.app.Stop("PREFLIGHT_REQUEST_NOT_ALLOWED")
        if self.calls >= MAX_CALLS or (not logout and self.calls >= MAX_CALLS - 1):
            raise app.app.Stop("PREFLIGHT_CALL_BUDGET")
        self.calls += 1
        headers = {"Accept": "application/json"}
        if self.token:
            if "\r" in self.token or "\n" in self.token:
                raise app.app.Stop("INVALID_SESSION")
            headers["Authorization"] = ("Bearer " if self.bearer else "") + self.token
        payload = None
        if body is not None:
            self.secrets.append(body["accessToken"])
            payload = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
        connection = live_connection(self.factory, "api.e-boekhouden.nl", timeout=15, context=ssl.create_default_context(cafile=certifi.where()))
        try:
            connection.request(method, path, body=payload, headers=headers)
            response = connection.getresponse()
            if logout and response.status == 204:
                return None
            if response.status != 200:
                raise app.RequestFailure("HTTP_" + str(response.status), "PREFLIGHT_REST", app.error_fields(response, self.secrets))
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise app.app.Stop("PREFLIGHT_RESPONSE_NOT_JSON")
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise app.app.Stop("PREFLIGHT_RESPONSE_TOO_LARGE")
            return json.loads(raw)
        except app.app.Stop:
            raise
        except Exception:
            raise app.app.Stop("PREFLIGHT_NETWORK_OR_JSON_FAILURE") from None
        finally:
            connection.close()

    def get(self, path):
        try:
            return self.request("GET", path)
        except app.RequestFailure as exc:
            if str(exc) != "HTTP_401" or self.bearer:
                raise
        self.bearer = True
        return self.request("GET", path)

    def detail(self, kind, identifier):
        if kind not in ("relation", "mutation") or not app.app.positive_integer(identifier):
            raise app.app.Stop("PREFLIGHT_DETAIL_SCOPE")
        path = "/v1/" + kind + "/" + str(identifier)
        self.detail_paths.add(path)
        result = self.get(path)
        if not isinstance(result, dict) or result.get("id") != identifier:
            raise app.app.Stop("PREFLIGHT_DETAIL_ID_MISMATCH")
        return result


def complete_pages(get, make_path, limit, max_pages):
    rows, seen = [], set()
    for page in range(max_pages):
        result = get(make_path(page * limit))
        items = result.get("items") if isinstance(result, dict) else None
        if not isinstance(items, list) or len(items) > limit:
            return rows, False, "unexpected_page_shape"
        if "count" in result and (type(result["count"]) is not int or result["count"] != len(items)):
            return rows, False, "reported_count_disagrees_with_retrieved_items"
        for item in items:
            if not isinstance(item, dict) or not app.app.positive_integer(item.get("id")) or item["id"] in seen:
                return rows, False, "duplicate_or_invalid_page_id"
            seen.add(item["id"])
            rows.append(item)
        if len(items) < limit:
            return rows, True, None
    return rows, False, "page_budget_exhausted"


def map_ledgers(items, complete, codes):
    result = {}
    for code in codes:
        found = [item for item in items if str(item.get("code")) == code]
        if not complete or len(found) != 1:
            result[code] = {"status": "catalog_incomplete" if not complete else "missing_or_duplicate_code", "candidates": found}
            continue
        item = found[0]
        category = item.get("category")
        suitable = category == "CRED" if code == "1700" else category not in ("FIN", "CRED", "DEB", None, "")
        result[code] = {"status": "mapped" if suitable else "category_requires_review",
                        **{k: item.get(k) for k in ("id", "code", "description", "category", "group")},
                        "activeStatus": "not_exposed_by_rest_schema"}
    return result


class Relations:
    def __init__(self, client):
        self.client = client
        self.cache = {}
        self.query_cache = {}

    def detail(self, identifier):
        if identifier not in self.cache:
            self.cache[identifier] = self.client.detail("relation", identifier)
        return self.cache[identifier]

    def candidates(self, path):
        if path in self.query_cache:
            return self.query_cache[path]
        value = self.client.get(path)
        rows = value.get("items") if isinstance(value, dict) else None
        if not isinstance(rows, list) or len(rows) > 5:
            return [], False
        found = []
        for row in rows:
            if not isinstance(row, dict) or not app.app.positive_integer(row.get("id")):
                return [], False
            found.append(self.detail(row["id"]))
        result = found, len(rows) < 5
        self.query_cache[path] = result
        return result

    def resolve(self, supplier, policy):
        if "amazon" in supplier.lower():
            code, expected = policy["acceptedAmazonCentralCode"], policy["expectedAmazonRelationId"]
        else:
            hint = next((h for h in policy.get("relationHints", []) if h["supplier"] == supplier), None)
            code, expected = (hint["code"], hint["expectedId"]) if hint else (None, None)
        if code:
            rows, complete = self.candidates(query("/v1/relation", code=code, limit=5, offset=0))
            found = [row for row in rows if row.get("code") == code and row.get("id") == expected and row.get("inactive") is False]
            if complete and len(found) == 1:
                return {"status": "matched_verified_code", "relation": relation_projection(found[0])}
            return {"status": "expected_code_identity_or_active_conflict", "candidates": [relation_projection(r) for r in rows]}
        candidates, exact_ids, complete = {}, set(), True
        keys = {normalize(value) for value in aliases(supplier)}
        for path in relation_queries(supplier):
            rows, part_complete = self.candidates(path)
            complete = complete and part_complete
            for row in rows:
                candidates[row["id"]] = row
                if normalize(row.get("name", "")) in keys and row.get("inactive") is False:
                    exact_ids.add(row["id"])
        if complete and len(exact_ids) == 1:
            selected = candidates[next(iter(exact_ids))]
            status = "matched_exact_existing_name" if normalize(selected.get("name")) == normalize(supplier) else "matched_exact_source_alias"
            return {"status": status, "relation": relation_projection(selected)}
        return {"status": "ambiguous_or_unmatched_targeted_search", "searchCompleteWithinBound": complete,
                "candidates": [relation_projection(row) for row in list(candidates.values())[:10]]}


def relation_projection(row):
    return {key: row.get(key) for key in ("id", "code", "name", "type", "vatNumber", "inactive", "termOfPayment")}


def payment_term(explicit, relation):
    if explicit not in ("", None):
        value = Decimal(str(explicit))
        if value < 0 or value != value.to_integral_value():
            return {"status": "invalid_explicit_term"}
        return {"status": "source_explicit", "days": int(value)}
    value = relation.get("termOfPayment") if relation else None
    if type(value) is int and value >= 0:
        return {"status": "existing_relation_default_available", "days": value}
    return {"status": "missing_no_default_assumed"}


def gross(detail):
    amount = sum((money(row["amount"]) for row in detail["rows"]), Decimal(0))
    if detail.get("inExVat") == "IN":
        return money(amount)
    if detail.get("inExVat") == "EX":
        return money(amount + sum((money(row["amount"]) for row in detail["vat"]), Decimal(0)))
    raise app.app.Stop("MUTATION_AMOUNT_MODE_UNKNOWN")


def compare_duplicate(inv, detail, mapped_relation):
    if str(detail.get("type")) != "1":
        return {"status": "possible_existing_requires_review", "mutationId": detail["id"],
                "checks": {"invoiceNumber": detail.get("invoiceNumber") == str(inv["factuurnummer"]), "type": False},
                "existing": {"type": detail.get("type"), "date": detail.get("date"), "relationId": detail.get("relationId")},
                "reason": "non_purchase_mutation_reference_not_interpreted_as_purchase_amount"}
    checks = {"invoiceNumber": detail.get("invoiceNumber") == str(inv["factuurnummer"]),
              "type": str(detail.get("type")) == "1",
              "date": iso_date(detail.get("date")) == iso_date(inv["factuurdatum"]),
              "gross": gross(detail) == money(inv["totaal_incl_btw"]),
              "counterparty": mapped_relation is not None and detail.get("relationId") == mapped_relation.get("id")}
    return {"status": "confirmed_existing_duplicate" if all(checks.values()) else "possible_existing_requires_review",
            "mutationId": detail["id"], "checks": checks,
            "existing": {"date": detail.get("date"), "gross": str(gross(detail)), "relationId": detail.get("relationId")}}


def inspect_duplicates(client, inv, mapped_relation):
    number = str(inv["factuurnummer"])
    rows, complete, reason = complete_pages(client.get, lambda offset: mutation_query(number, offset), 20, 3)
    if any(row.get("invoiceNumber") != number or str(row.get("type")) not in {"1", "2", "3", "4", "5", "6", "7"} for row in rows):
        return {"status": "query_filter_not_honored", "complete": False}
    if not complete:
        return {"status": "duplicate_check_incomplete", "complete": False, "reason": reason}
    if not rows:
        return {"status": "no_existing_exact_invoice_number", "complete": True}
    if len(rows) > 5:
        return {"status": "too_many_exact_number_candidates", "complete": True, "candidateIds": [row["id"] for row in rows]}
    comparisons = [compare_duplicate(inv, client.detail("mutation", row["id"]), mapped_relation) for row in rows]
    return {"status": "confirmed_existing_duplicate" if any(x["status"] == "confirmed_existing_duplicate" for x in comparisons)
            else "possible_existing_requires_review", "complete": True, "comparisons": comparisons}


def line_proposal(line, invoice, policy, ledger_map):
    code = str(line["grootboekcode_voorgesteld"])
    private = code == policy["privateCode"]
    reverse = invoice["factuur_id"] in policy["reverseChargeInvoiceIds"]
    if private:
        vat_code, vat_status = "GEEN", "private_no_input_vat"
    elif reverse:
        vat_code, vat_status = "BI_EU_INK", "EU_reverse_charge_existing_practice_proposal"
    elif str(line["btw_percentage"]) == "21":
        vat_code, vat_status = "HOOG_INK_21", "source_21_percent_purchase"
    else:
        vat_code, vat_status = None, "requires_vat_review"
    source = {"net": str(money(line["bedrag_ex_btw"])), "vat": str(money(line["btw_bedrag"])), "gross": str(money(line["bedrag_incl_btw"]))}
    basis = source["gross"] if private or invoice["bedragen_incl_excl"] == "INCL" else source["net"]
    return {"line": line["regel_nr"], "description": line["omschrijving"], "ledgerCode": code,
            "ledger": ledger_map[code], "sourceAmounts": source, "proposedAmountBasis": basis,
            "vatCode": vat_code, "vatStatus": vat_status, "deductibleSourceVat": "0.00" if private else source["vat"],
            "policyAcceptedWorkClothing": code == policy["workClothingCode"]}


def redact(value, secrets):
    if isinstance(value, str):
        for secret in sorted(secrets, key=len, reverse=True):
            if secret:
                value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, list):
        return [redact(item, secrets) for item in value]
    if isinstance(value, dict):
        return {redact(str(key), secrets): redact(item, secrets) for key, item in value.items()}
    return value
