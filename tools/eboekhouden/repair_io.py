from toolkit_runtime import WORKROOT, runtime_area
"""Existing read adapters composed for bounded metadata-repair evidence."""
import copy
import hashlib
import math
import sys
from urllib.parse import urlencode
from pathlib import Path

ROOT = WORKROOT
import prepare_edit as prep
import app_probe as core
import processed_invoice_probe as files
import probe_link_contract as links
from repair_contract import require, payment_fields, without_descriptions

def outstanding_path(state):
    return "/v1/mutation/invoice/outstanding?" + urlencode({"credDeb": "C", "invoiceNumber": state["invoiceNumber"], "limit": 20, "offset": 0})

def historical_projection(current, expected):
    if isinstance(expected, dict):
        require(isinstance(current, dict) and set(expected) <= set(current), "REPAIR_HISTORICAL_FIELD_MISSING")
        return {k: historical_projection(current[k], v) for k, v in expected.items()}
    if isinstance(expected, list):
        require(isinstance(current, list) and len(current) == len(expected), "REPAIR_HISTORICAL_ROW_COUNT")
        return [historical_projection(a, b) for a, b in zip(current, expected)]
    return current

class RepairReads:
    def __init__(self, rest_get, app_read, file_read, linked_read, check_admin, outstanding_get, observe=None):
        self.rest_get = rest_get
        self.app_read = app_read
        self.file_read = file_read
        self.linked_read = linked_read
        self.check_admin = check_admin
        self.outstanding_get = outstanding_get
        self.last_observation = {}
        self.observe = observe

    def record(self, kind, value):
        self.last_observation.setdefault("rawObservations", []).append({"kind": kind, "value": copy.deepcopy(value)})
        if self.observe is not None:
            self.observe(kind, value)

    def rest(self, number):
        value = self.rest_get("/v1/mutation/" + str(number))
        self.record("rest", {"requestedMutationNumber": number, "response": value})
        require(isinstance(value, dict) and value.get("id") == number and value.get("type") == 1, "REPAIR_REST_IDENTITY")
        return value

    def payment_status(self, state, allow_absent=False):
        path = outstanding_path(state)
        value = self.outstanding_get(path)
        self.record("outstanding", {"requestedPath": path, "response": value})
        if allow_absent and isinstance(value, dict) and type(value.get("count")) is int and value["count"] == 0 and value.get("items") == []:
            return {"observation": "NOT_RETURNED_BY_API", "mutationId": state["id"],
                    "relationId": state["relationId"], "invoiceNumber": state["invoiceNumber"]}
        require(isinstance(value, dict) and isinstance(value.get("items"), list)
                and value.get("count") == len(value["items"]) and len(value["items"]) == 1, "REPAIR_OUTSTANDING_SCOPE_UNKNOWN")
        require(all(v.get("invoiceNumber") == state["invoiceNumber"] for v in value["items"]), "REPAIR_OUTSTANDING_FILTER_IGNORED")
        found = [v for v in value["items"] if v.get("mutationId") == state["id"]]
        require(len(found) == 1 and found[0].get("relationId") == state["relationId"], "REPAIR_PAYMENT_STATUS_NOT_UNIQUE_STOP")
        require(all(type(found[0].get(k)) in (int, float) and math.isfinite(found[0][k]) for k in ("totalAmount", "paidAmount", "outstandingAmount")), "REPAIR_PAYMENT_AMOUNTS_UNKNOWN")
        return found[0]

    def capture(self, file_entry, header_entry=None):
        self.check_admin()
        states = {}
        linked = {}
        payments = {}
        self.last_observation = {"rests": states, "linkedFiles": linked, "outstandingInvoices": payments}
        for number in file_entry["coveredMutationNumbers"]:
            state = self.rest(number)
            historical = file_entry["historicalRests"][str(number)]
            require(without_descriptions(historical_projection(state, historical)) == without_descriptions(historical),
                    "REPAIR_HISTORICAL_FINANCIAL_CHANGE_STOP")
            states[str(number)] = state
            payments[str(number)] = self.payment_status(state, allow_absent=header_entry is None)
            members = self.linked_read(number)
            ids = [v["fileId"] for v in members]
            require(ids == [file_entry["fileId"]], "REPAIR_LINK_SCOPE_CHANGED")
            linked[str(number)] = members
        metadata = self.file_read("metadata", file_entry["fileId"])
        self.last_observation["metadata"] = metadata
        require(isinstance(metadata, dict) and metadata.get("id") == file_entry["fileId"]
                and metadata.get("directoryId") == file_entry["directoryId"]
                and metadata.get("naam") in {file_entry["oldName"], file_entry["newName"]}, "REPAIR_MANUAL_NAME_CHANGE_STOP")
        data = self.file_read("bytes", file_entry["fileId"])
        self.last_observation["downloadFacts"] = {"mime": data["mime"], "size": len(data["bytes"]), "sha256": hashlib.sha256(data["bytes"]).hexdigest()}
        require(data["mime"] == "application/pdf" and len(data["bytes"]) == file_entry["size"]
                and hashlib.sha256(data["bytes"]).hexdigest() == file_entry["sourceSha256"], "REPAIR_PDF_BYTES_CHANGED")
        observed = None
        if header_entry:
            state = states[str(header_entry["mutationNumber"])]
            require(state["description"] in {header_entry["oldHeader"], header_entry["newHeader"]},
                    "REPAIR_MANUAL_HEADER_CHANGE_STOP")
            observed = self.app_read(state["id"], state["date"])
            self.record("app", {"requestedMutationNumber": state["id"], "response": observed})
            prep.identity_mapping(state, observed)
            for row, wanted in zip(state["rows"], header_entry["sourceRowDescriptions"]):
                require(row.get("description") in {header_entry["oldHeader"], header_entry["newHeader"], wanted},
                        "REPAIR_MANUAL_ROW_DESCRIPTION_CHANGE_STOP")
        self.check_admin()
        return {"rests": states, "appTarget": observed, "metadata": metadata, "linkedFiles": linked,
                "pdf": {"sha256": file_entry["sourceSha256"], "size": file_entry["size"], "verified": True},
                "paymentFields": {"rest": payment_fields(states), "app": payment_fields(observed), "outstandingInvoices": payments},
                "outstandingPresenceRequired": header_entry is not None,
                "paymentCoverage": "Exact invoiceNumber-scoped official observations; header requires present exact status; rename-only absence is NOT_RETURNED_BY_API with no invented amounts"}

    def optimistic(self, captured):
        for key, state in captured["rests"].items():
            require(self.rest(int(key)) == state, "REPAIR_FRESH_REST_CHANGED")
            require(self.payment_status(state, allow_absent=not captured.get("outstandingPresenceRequired", True)) == captured["paymentFields"]["outstandingInvoices"][key], "REPAIR_FRESH_PAYMENT_STATUS_CHANGED")

class ObservedAppReadTransport:
    """Observe only mutation detail responses, never auth/profile/session bodies."""
    def __init__(self, transport, observe):
        self.transport, self.observe = transport, observe

    def request(self, method, path, *args, **kwargs):
        value = self.transport.request(method, path, *args, **kwargs)
        prefix = "/api/v4/mutaties/"
        if method == "GET" and path.startswith(prefix) and path[len(prefix):].isdigit():
            self.observe("app-detail", {"requestedPath": path, "response": value})
        return value


def compose_reads(client, session, observe=None):
    def app_read(number, day):
        transport = core.Transport()
        if observe is not None:
            transport = ObservedAppReadTransport(transport, observe)
        return session.read_mutation_raw(transport, number, day)
    def file_read(kind, identifier):
        reader = files.Transport("app", file_id=identifier, factory=core.tls_connection)
        prefix = "/api/v4/bestanden/bestand/" if kind == "metadata" else "/api/v4/bestanden/download/"
        return reader.request("GET", prefix + str(identifier), token=session.token)
    def linked_read(number):
        reader, body = links.linked_query(number)
        result = reader.request("POST", "/api/v4/bestanden/gekoppeld", body, token=session.token)
        return links.project_files(result, session.secrets)
    return RepairReads(client.get, app_read, file_read, linked_read, session.require_same_admin, client.get, observe)

def same_file_retention(before, after):
    require(before["pdf"] == after["pdf"], "REPAIR_PDF_RETENTION_FAILED")
    before_ids = {k: [z["fileId"] for z in v] for k, v in before["linkedFiles"].items()}
    after_ids = {k: [z["fileId"] for z in v] for k, v in after["linkedFiles"].items()}
    require(before_ids == after_ids, "REPAIR_SHARED_LINK_RETENTION_FAILED")
    require(before["paymentFields"] == after["paymentFields"], "REPAIR_PAYMENT_FIELDS_CHANGED")
