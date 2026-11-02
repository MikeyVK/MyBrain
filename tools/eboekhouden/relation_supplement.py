from toolkit_runtime import WORKROOT, runtime_area
"""Read-only curated alias lookup. Never changes relations or mappings."""
import argparse
import hashlib
import json
from pathlib import Path
import uuid

import preflight as base


def planned_queries(group):
    result = []
    for field, terms in (("name", group["nameTerms"]), ("code", group["codeTerms"])):
        for term in terms:
            if not isinstance(term, str) or not 2 <= len(term) <= 80 or any(c in term for c in ("%", "?", "\r", "\n")):
                raise base.app.app.Stop("RELATION_HINT_INVALID")
            result.append((field, term))
    return result


def relation_path(field, term, offset):
    return base.query("/v1/relation", **{field + "[like]": "%" + term + "%", "limit": 10, "offset": offset})


class Client(base.Client):
    def __init__(self, hints, factory=base.http.client.HTTPSConnection):
        super().__init__([], {"acceptedAmazonCentralCode": "unused"}, factory)
        self.paths = {relation_path(field, term, offset) for group in hints["groups"]
                      for field, term in planned_queries(group) for offset in (0, 10)}
        control = hints["positiveControl"]
        self.control_paths = {base.mutation_query(control["invoiceNumber"], offset) for offset in (0, 20, 40)}
        self.paths |= self.control_paths

    def request(self, method, path, body=None):
        logout = method == "DELETE" and path == "/v1/session"
        if self.calls >= 150 or (not logout and self.calls >= 149):
            raise base.app.app.Stop("RELATION_SUPPLEMENT_CALL_BUDGET")
        if method == "GET" and (path.startswith("/v1/ledger") or (path.startswith("/v1/mutation") and path not in self.control_paths)):
            raise base.app.app.Stop("RELATION_SUPPLEMENT_QUERY_NOT_ALLOWED")
        return super().request(method, path, body)


def collect(client, hints, prior):
    unresolved = {row["supplierOriginal"] for row in prior["invoices"] if not row["relationMapping"].get("relation")}
    if {group["supplier"] for group in hints["groups"]} != unresolved:
        raise base.app.app.Stop("SUPPLIER_SCOPE_CHANGED")
    control = hints["positiveControl"]
    rows, complete, reason = base.complete_pages(client.get, lambda offset: base.mutation_query(control["invoiceNumber"], offset), 20, 3)
    valid = complete and all(row.get("invoiceNumber") == control["invoiceNumber"] for row in rows)
    found = any(row["id"] == control["expectedMutationId"] and str(row.get("type")) == str(control["type"]) for row in rows)
    if not valid or not found:
        raise base.app.app.Stop("PRIOR_EMPTY_DUPLICATE_EVIDENCE_UNCONFIRMED_POSITIVE_CONTROL_FAILED")
    query_cache, details, results = {}, {}, []
    for group in hints["groups"]:
        identifiers, checks = {}, []
        for field, term in planned_queries(group):
            key = field, term
            if key not in query_cache:
                query_cache[key] = base.complete_pages(client.get, lambda offset: relation_path(field, term, offset), 10, 2)
            rows, complete, reason = query_cache[key]
            checks.append({"field": field, "term": term, "complete": complete, "reason": reason, "matchCount": len(rows)})
            for row in rows:
                identifiers[row["id"]] = row
        candidates, detail_complete = [], True
        for identifier, summary in identifiers.items():
            if identifier not in details:
                if len(details) >= 60:
                    detail_complete = False
                    continue
                details[identifier] = client.detail("relation", identifier)
            candidate = details[identifier]
            if candidate.get("code") != summary.get("code"):
                raise base.app.app.Stop("RELATION_CODE_IDENTITY_CHANGED")
            candidates.append(base.relation_projection(candidate))
        complete = all(check["complete"] for check in checks) and detail_complete
        expected = group.get("expectedCurrentEntry")
        expected_found = bool(expected and any(row["id"] == expected["id"] and row["code"] == expected["code"]
                                             and row.get("inactive") is False for row in candidates))
        status = "existing_candidates_require_alias_review" if candidates else "no_matches_for_curated_aliases"
        if not complete:
            status = "bounded_search_or_details_incomplete"
        results.append({"supplierOriginal": group["supplier"], "status": status, "searchCompleteWithinBound": complete,
                        "queryEvidence": checks, "candidates": candidates,
                        "expectedCurrentEntryStillPresent": expected_found,
                        "verifiedHistoricalHint": expected,
                        "policyProposedRelation": group.get("policyProposedRelation"),
                        "automaticMappingPerformed": False})
        print("Aanvullende leverancierscontrole:", len(results), "van", len(hints["groups"]), flush=True)
    return {"status": "readonly_relation_supplement", "sourceDuplicateEvidenceReused": True,
            "positiveControlPassed": True, "positiveControlScope": "identical_exact_invoice_number_filter_without_type",
            "groups": results, "apiCalls": client.calls, "noWritesPerformed": True,
            "absenceMeaning": "No matches only within these explicit complete curated queries; not global proof of missing relation",
            "isolatechPolicy": hints["isolatechPolicy"]}


def load_checked(path, expected):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        raise base.app.app.Stop("RELATION_INPUT_FINGERPRINT_CHANGED")
    return json.loads(raw)
