from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""Header/name repair over existing bounded readers and one-shot App commands."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from repair_io import ROOT, prep, core, files, compose_reads, same_file_retention, outstanding_path
from repair_contract import (require, validate_catalog, build_description_payload, verify_description,
                             verify_rename)
from change_ledger import AppMutationCommand, safe_failure
from app_session import AppAuthentication
from private_output import PrivateOutput

HOME = runtime_area("metadata")

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_catalog(path, expected):
    path = private_path(path)
    value = prep.checked(path, expected)
    validate_catalog(value)
    for key in ("sourceSnapshot", "sourceFinalIndex"):
        source = private_path(ROOT / value[key]["path"])
        require(source.is_relative_to(ROOT.resolve()) and digest(source) == value[key]["sha256"],
                "REPAIR_SOURCE_EVIDENCE_CHANGED")
    return value

def select(catalog, action, key):
    collections = {"header": ("headers", "mutationNumber"), "rename": ("files", "fileId")}
    collection, field = collections[action]
    found = [v for v in catalog[collection] if v[field] == key]
    require(len(found) == 1, "REPAIR_TARGET_NOT_IN_OWNER_CATALOG")
    entry = found[0]
    if action == "rename":
        require(entry["action"] == "RENAME", "REPAIR_KEEP_FILE_NO_RENAME_ALLOWED")
        return entry, entry
    file_entry = next(v for v in catalog["files"] if v["fileId"] == entry["fileId"])
    return entry, file_entry

def payload_for(action, before, entry):
    if action == "header":
        number = entry["mutationNumber"]
        return build_description_payload(before["rests"][str(number)], before["appTarget"], entry)
    return {"id": entry["fileId"], "naam": entry["newName"]}

def desired(action, before, entry):
    if action == "header":
        return before["rests"][str(entry["mutationNumber"])]["description"] == entry["newHeader"]
    return before["metadata"]["naam"] == entry["newName"]

def prepare(reads, catalog, catalog_reference, action, key, output):
    entry, file_entry = select(catalog, action, key)
    before = reads.capture(file_entry, entry if action == "header" else None)
    reads.optimistic(before)
    payload = payload_for(action, before, entry)
    return {"scope": "ONE_METADATA_REPAIR_ONLY", "action": action, "target": key,
            "catalogReference": catalog_reference, "entry": entry, "fileEntry": file_entry,
            "before": before, "payload": payload, "payloadHash": prep.fingerprint(payload),
            "alreadyDesired": desired(action, before, entry), "financialChangesAuthorized": False,
            "raceCaveat": "Fresh snapshot comparison is not an atomic API conditional update.",
            "independentRowsGuarantee": False}

def facts(exc, stage, response_id=None):
    result = safe_failure(exc, stage, response_id)
    if isinstance(exc, ValueError) and re.fullmatch(r"[A-Z0-9_]{1,180}", str(exc)):
        result["cause"] = str(exc)
    return result

def execute(reads, command, plan, plan_hash, journal, output):
    require(not journal.exists() or not journal.read_bytes().strip(), "REPAIR_PRIOR_ATTEMPT_NO_RETRY")
    action, entry, file_entry = plan["action"], plan["entry"], plan["fileEntry"]
    if action == "header":
        require(not re.search(r"\s", entry["invoiceNumber"]), "REPAIR_HEADER_INVOICE_WHITESPACE_WRITE_UNPROVED")
    before = reads.capture(file_entry, entry if action == "header" else None)
    require(before == plan["before"], "REPAIR_PREPARED_BASELINE_CHANGED")
    require(payload_for(action, before, entry) == plan["payload"]
            and prep.fingerprint(plan["payload"]) == plan["payloadHash"], "REPAIR_PAYLOAD_CHANGED")
    baseline = output.save("repair-before", before)
    if desired(action, before, entry):
        value = {"state": "ALREADY_DESIRED_VERIFIED_NO_PUT", "action": action, "target": plan["target"],
                 "planHash": plan_hash, "putAttemptCount": 0}
        output.append(journal, value)
        return value
    reads.optimistic(before)
    pending = {"state": "PENDING", "action": action, "target": plan["target"], "planHash": plan_hash,
               "catalogHash": plan["catalogReference"]["sha256"], "payloadHash": plan["payloadHash"],
               "beforeFile": baseline.name, "beforeSha256": digest(baseline)}
    output.append(journal, pending)
    response_id, attempt_error, ack, after_reference = None, None, None, None
    try:
        response = command.send(plan["payload"])
        ack = {"responseType": type(response).__name__, "knownFields": {k: {"present": isinstance(response, dict) and k in response, "type": type(response.get(k)).__name__ if isinstance(response, dict) and k in response else None} for k in ("id", "mutatieNummer", "naam")}}
        if isinstance(response, dict) and type(response.get("id")) is int and response["id"] > 0:
            response_id = response["id"]
        understood = response_id is not None and (response.get("mutatieNummer", entry.get("mutationNumber")) == entry.get("mutationNumber") if action == "header" else response_id == entry["fileId"] and response.get("naam") == entry["newName"])
        ack["receivedIdPositive"] = response_id is not None
        ack["visibleNumberMatches"] = isinstance(response, dict) and response.get("mutatieNummer") == entry.get("mutationNumber") if action == "header" else None
        ack["fileNameMatches"] = isinstance(response, dict) and response.get("naam") == entry.get("newName") if action == "rename" else None
        ack["identityShapeUnderstood"] = understood
        if not understood:
            attempt_error = {"stage": "PUT_ACK", "cause": "ACK_IDENTITY_UNCONFIRMED_READ_REQUIRED"}
    except Exception as exc:
        attempt_error = facts(exc, "PUT_RESPONSE_UNKNOWN")
    stage = "READ_AFTER"
    try:
        after = reads.capture(file_entry, entry if action == "header" else None)
        after_path = output.save("repair-after", after)
        after_reference = {"file": after_path.name, "sha256": digest(after_path)}
        same_file_retention(before, after)
        row_evidence = []
        if action == "header":
            target = str(entry["mutationNumber"])
            for key, old in before["rests"].items():
                if key != target:
                    require(after["rests"][key] == old, "REPAIR_OTHER_SHARED_MUTATION_CHANGED")
            row_evidence = verify_description(before["rests"][target], after["rests"][target], after["appTarget"], entry)
            require(before["metadata"] == after["metadata"], "REPAIR_HEADER_CHANGED_ARCHIVE_METADATA")
        else:
            require(before["rests"] == after["rests"], "REPAIR_RENAME_CHANGED_BOOKKEEPING")
            verify_rename(before["metadata"], after["metadata"], entry)
        value = {**pending, "state": "RECONCILED_VERIFIED_AFTER_UNKNOWN_RESPONSE" if attempt_error else "VERIFIED",
                 "receivedId": response_id, "putAttemptCount": 1,
                 "appInternalIdBefore": (before["appTarget"] or {}).get("id"),
                 "appInternalIdAfter": (after["appTarget"] or {}).get("id"), "attemptDiagnostic": attempt_error,
                 "acknowledgement": ack, "afterFile": after_path.name, "afterSha256": digest(after_path), "rowDescriptionEvidence": row_evidence,
                 "headerRestored": action == "header", "filenameRestored": action == "rename",
                 "nonDescriptionFinancialFieldsUnchanged": True, "pdfBytesAndAllSharedTargetsPreserved": True,
                 "noPaymentCreateUploadLinkDeleteRollbackOrSheetWrites": True}
        output.append(journal, value)
        return value
    except Exception as exc:
        if after_reference is None and getattr(reads, "last_observation", None):
            partial = output.save("repair-after-incomplete-observation", reads.last_observation)
            after_reference = {"file": partial.name, "sha256": digest(partial), "incomplete": True}
        output.append(journal, {**pending, "state": "UNCERTAIN", "receivedId": response_id,
                               "acknowledgement": ack, "afterEvidence": after_reference,
                               "attemptDiagnostic": attempt_error, "verificationDiagnostic": facts(exc, stage)})
        raise

class BoundCommand:
    def __init__(self, command, token):
        self.command, self.token = command, token
    def send(self, payload):
        return self.command.send(payload, self.token)

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("header", "rename"))
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--catalog-sha256", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--plan-sha256")
    args = parser.parse_args(argv)
    catalog = load_catalog(args.catalog, args.catalog_sha256)
    entry, file_entry = select(catalog, args.action, args.target)
    reference = {"path": str(args.catalog.resolve().relative_to(ROOT.resolve())).replace("\\", "/"),
                 "sha256": args.catalog_sha256.lower()}
    plan = None
    if args.apply:
        if args.action == "header":
            require(not re.search(r"\s", entry["invoiceNumber"]), "REPAIR_HEADER_INVOICE_WHITESPACE_WRITE_UNPROVED")
        require(args.plan is not None and args.plan_sha256 is not None, "REPAIR_PLAN_REQUIRED")
        plan = prep.checked(args.plan, args.plan_sha256)
        require(plan.get("scope") == "ONE_METADATA_REPAIR_ONLY" and plan["action"] == args.action
                and plan["target"] == args.target and plan["entry"] == entry and plan["fileEntry"] == file_entry
                and plan["catalogReference"] == reference, "REPAIR_PLAN_CATALOG_BINDING_CHANGED")
    case = HOME / "cases" / (args.action + "-" + str(args.target))
    case.mkdir(parents=True, exist_ok=True)
    journal, lock = case / "attempt.jsonl", case / "attempt.lock"
    if args.apply:
        require(not journal.exists() or not journal.read_bytes().strip(), "REPAIR_PRIOR_ATTEMPT_NO_RETRY")
    output = PrivateOutput(case)
    if not args.apply and not args.prepare:
        output.note(str(output.save("repair-dryrun", {"action": args.action, "target": args.target,
                    "entry": entry, "file": file_entry, "noCredentialsOrApiCalls": True})))
        return
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.catalog_sha256)
    client, session = None, None
    try:
        base = prep.base
        client = base.Client([], {"acceptedAmazonCentralCode": "unused"})
        client.paths = {"/v1/mutation/" + str(n) for n in file_entry["coveredMutationNumbers"]}
        client.paths.update(outstanding_path(state) for state in file_entry["historicalRests"].values())
        base.MAX_CALLS = 24
        access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
        response = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
        require(isinstance(response, dict) and isinstance(response.get("token"), str) and response["token"],
                "REPAIR_REST_SESSION_UNKNOWN")
        client.token = response["token"]
        client.secrets.extend([access, client.token])
        login = core.load_login(core.WindowsBackend().api)
        session = AppAuthentication(core.Transport())
        session.login(login, catalog["expectedAdminId"])
        client.secrets.extend(session.secrets)
        del login, access, response
        output = PrivateOutput(case, client.secrets)
        reads = compose_reads(client, session, lambda kind, value: output.save("repair-observation-" + kind, value))
        if args.prepare:
            value = prepare(reads, catalog, reference, args.action, args.target, output)
            output.note(str(output.save("repair-plan", value)))
        else:
            endpoint = {"header": "/api/v4/mutaties", "rename": "/api/v4/bestanden"}[args.action]
            command = BoundCommand(AppMutationCommand(plan["payload"], endpoint=endpoint), session.token)
            value = execute(reads, command, plan, args.plan_sha256, journal, output)
            output.note(str(output.save("repair-result", value)))
    except Exception as exc:
        stopped = output.save("repair-stopped", facts(exc, "CLI_BOUNDARY"))
        output.note(str(stopped))
        raise
    finally:
        if client is not None and client.token:
            try:
                client.request("DELETE", "/v1/session")
                output.note("REST_SESSION_REVOKED")
            except Exception as exc:
                output.save("repair-session-cleanup", facts(exc, "OWN_SESSION_REVOKE"))
        lock.unlink()

if __name__ == "__main__":
    main()
