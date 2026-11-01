from toolkit_runtime import WORKROOT, runtime_area
"""Read-only purchase edit preparation/verification. No PUT implementation."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = runtime_area("edits")
import preflight as base
import app_probe as app
from private_output import PrivateOutput

REST_FIELDS = ("id", "type", "date", "description", "termOfPayment", "ledgerId", "relationId", "inExVat",
               "invoiceNumber", "entryNumber", "rows", "vat")
ROW_FIELDS = ("ledgerId", "vatCode", "vatAmount", "costCenterId", "amount", "description", "invoiceNumber", "relationId")
CONTRACT_GAPS = ["PUT required fields and partial-versus-replacement behavior unproved",
                 "Relation preservation: relationId observed in response but not captured PUT properties",
                 "Root/row money basis and calculated App fields unproved; never roundtrip derived zeroes",
                 "Row index/ID preservation and ordering semantics unproved",
                 "PUT response/internal ID stability unproved",
                 "No atomic conditional update/ETag guarantee established; fresh REST comparison is not a lock"]


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False, separators=(",", ":")).encode()).hexdigest()


def checked(path, expected):
    raw = path.read_bytes()
    if len(raw) > 1024 * 1024 or hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        raise app.app.Stop("EDIT_INPUT_HASH_OR_SIZE_CHANGED")
    return json.loads(raw)


def project_rest(value, number):
    if not isinstance(value, dict) or value.get("id") != number or value.get("type") != 1:
        raise app.app.Stop("EDIT_ONLY_EXACT_EXISTING_PURCHASE_ALLOWED")
    rows = value.get("rows")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 100 or not all(isinstance(r, dict) for r in rows):
        raise app.app.Stop("EDIT_REST_ROWS_UNKNOWN")
    result = {key: value[key] for key in REST_FIELDS if key in value}
    result["rows"] = [{key: row[key] for key in ROW_FIELDS if key in row} for row in rows]
    return result


def identity_mapping(rest, app_record):
    if (not isinstance(app_record, dict) or not app.app.positive_integer(app_record.get("id"))
            or app_record.get("mutatieNummer") != rest["id"] or app_record.get("factuurNummer") != rest.get("invoiceNumber")
            or str(app_record.get("datum", ""))[:10] != rest.get("date")):
        raise app.app.Stop("EDIT_APP_INTERNAL_ID_MAPPING_MISMATCH")
    return {"restVisibleNumber": rest["id"], "appInternalId": app_record["id"],
            "appVisibleNumber": app_record["mutatieNummer"], "sameNumberInvoiceDateConfirmed": True,
            "noIdNamespaceEquivalenceAssumed": True}


def field_diff(before, after, path=""):
    if isinstance(before, dict) and isinstance(after, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            target = path + "/" + key
            if key not in before or key not in after:
                result.append({"path": target, "before": before.get(key), "after": after.get(key), "presenceChanged": True})
            else:
                result.extend(field_diff(before[key], after[key], target))
        return result
    if isinstance(before, list) and isinstance(after, list) and len(before) == len(after):
        return [change for index, (a, b) in enumerate(zip(before, after)) for change in field_diff(a, b, path + "/" + str(index))]
    return [] if before == after else [{"path": path, "before": before, "after": after}]


def intended_state(before, changes):
    # Initial preparation supports descriptive fields only; no monetary patch.
    result = copy.deepcopy(before)
    if not isinstance(changes, list) or len(changes) > 2:
        raise app.app.Stop("EDIT_CHANGE_SET_UNKNOWN")
    seen = set()
    for change in changes:
        if not isinstance(change, dict) or set(change) != {"path", "before", "after"} or change["path"] in seen:
            raise app.app.Stop("EDIT_CHANGE_SHAPE_OR_DUPLICATE")
        seen.add(change["path"])
        if change["path"] == "/description":
            target, key = result, "description"
        elif change["path"] == "/rows/0/description" and len(result["rows"]) == 1:
            target, key = result["rows"][0], "description"
        else:
            raise app.app.Stop("EDIT_INITIAL_SCOPE_DESCRIPTION_ONLY")
        if target.get(key) != change["before"] or not isinstance(change["after"], str) or not change["after"] or len(change["after"]) > 200 or any(ord(c) < 32 for c in change["after"]):
            raise app.app.Stop("EDIT_CHANGE_BASELINE_OR_VALUE_MISMATCH")
        target[key] = change["after"]
    return result


def make_plan(rest, app_record, manifest, source_kind, baseline_reference):
    if rest["date"] != manifest["knownDate"] or rest["id"] != manifest["mutationNumber"]:
        raise app.app.Stop("EDIT_TARGET_DATE_OR_NUMBER_CHANGED")
    mapping = identity_mapping(rest, app_record) if app_record is not None else None
    changes = manifest["requestedChanges"]
    intended = intended_state(rest, changes)
    blockers = list(CONTRACT_GAPS)
    if not changes or manifest.get("ownerPatchApproved") is not True:
        blockers.insert(0, "No concrete owner-approved field patch supplied")
    if mapping is None:
        blockers.append("Current App internal ID/admin mapping not yet captured")
    return {"state": "EDIT_PREPARED_WRITE_DISABLED", "sourceKind": source_kind,
            "baseline": rest, "baselineHash": fingerprint(rest), "baselineReference": baseline_reference,
            "appIdMapping": mapping, "requestedChanges": changes, "intendedRestState": intended,
            "fieldDiff": field_diff(rest, intended), "unchangedFieldsProtection": "All captured official REST schema fields, including row costCenterId when returned",
            "appObservedSnapshotNotPutPayload": app_record, "putPayload": None, "applyEnabled": False,
            "writeContractGaps": blockers, "noBookkeepingWriteOccurred": True,
            "futureWriteDiscipline": "Fresh REST hash compare before any separately reviewed PUT; durable full baseline and PENDING before request; uncertain outcome stops, retain received ID and original cause; REST after-read verifies intended and every other captured field; no automatic rollback/delete/recreate"}


def optimistic_check(baseline, current):
    if fingerprint(baseline) != fingerprint(current):
        raise app.app.Stop("EDIT_FRESH_REST_BASELINE_CHANGED_STOP")


def verify_state(plan, current):
    differences = field_diff(plan["intendedRestState"], current)
    return {"state": "REST_POSTSTATE_MATCHES_PLAN" if not differences else "REST_POSTSTATE_MISMATCH_STOP",
            "differences": differences, "noWriteOrRollbackAttempted": True,
            "noPriorPutExecutionClaim": True, "planBaselineHash": plan["baselineHash"]}


def read_rest(client, access, number, output):
    session = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
    if not isinstance(session, dict) or not isinstance(session.get("token"), str) or not session["token"]:
        raise app.app.Stop("EDIT_REST_SESSION_UNKNOWN")
    client.token = session["token"]
    client.secrets.append(client.token)
    try:
        return base.redact(project_rest(client.get("/v1/mutation/" + str(number)), number), client.secrets)
    finally:
        try:
            client.request("DELETE", "/v1/session")
            output.note("Tijdelijke REST-leessessie ingetrokken.")
        except app.app.Stop:
            output.note("REST-sessiebeëindiging niet bevestigd.")


def compose_reader(number, output):
    client = base.Client([], {"acceptedAmazonCentralCode": "unused"})
    client.paths = {"/v1/mutation/" + str(number)}
    base.MAX_CALLS = 5
    access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
    return lambda: read_rest(client, access, number, output)


def capture(manifest, rest_reader, app_reader, rest_recheck, output):
    before = rest_reader()
    path = output.save("edit-rest-baseline", {"sourceKind": "CURRENT_OFFICIAL_REST_READ", "mutation": before})
    reference = {"file": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    app_record = app_reader()
    output.save("edit-app-observed-readonly", app_record)
    after = rest_recheck()
    output.save("edit-rest-concurrency-recheck", {"mutation": after})
    optimistic_check(before, after)
    return make_plan(before, app_record, manifest, "CURRENT_REST_APP_READS_NO_WRITE", reference)


def deny_apply():
    raise app.app.Stop("EDIT_APPLY_DISABLED_NO_OWNER_PATCH_OR_PROVEN_PUT_CONTRACT")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    sub = parser.add_subparsers(dest="mode", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--manifest-sha256", required=True)
    prepare.add_argument("--capture-readonly", action="store_true")
    verify = sub.add_parser("verify")
    verify.add_argument("--plan", required=True)
    verify.add_argument("--plan-sha256", required=True)
    args = parser.parse_args()
    if args.apply:
        deny_apply()  # Before credentials, sessions, snapshots or network.
    app.app.set_private_acl(ROOT, (app.owner_sid(),))
    output = PrivateOutput(ROOT)
    if args.mode == "verify":
        if Path(args.plan).name != args.plan or not args.plan.startswith("edit-plan-") or not args.plan.endswith(".json"):
            raise app.app.Stop("EDIT_PLAN_PATH_SCOPE")
        plan = checked(ROOT / args.plan, args.plan_sha256)
        number = plan["baseline"]["id"]
        current = compose_reader(number, output)()
        output.note("REST-nacontrole: " + str(output.save("edit-verify", verify_state(plan, current))))
        return
    manifest = checked(ROOT / "edit-input.json", args.manifest_sha256)
    if manifest.get("scope") != "PREPARE_EXISTING_TYPE1_NO_WRITE" or not app.app.positive_integer(manifest.get("mutationNumber")):
        raise app.app.Stop("EDIT_MANIFEST_SCOPE")
    app.filter_body(manifest["knownDate"], 1)
    if args.capture_readonly:
        if not app.app.positive_integer(manifest.get("expectedAppAdminId")):
            raise app.app.Stop("EDIT_EXPECTED_ADMIN_REQUIRED")
        number = manifest["mutationNumber"]
        def app_reader():
            login = app.load_login(app.WindowsBackend().api)
            return app.read_selected(app.Transport(), login, number, manifest["knownDate"],
                lambda active: active[0] == manifest["expectedAppAdminId"])
        plan = capture(manifest, lambda: compose_reader(number, output)(), app_reader,
                       lambda: compose_reader(number, output)(), output)
    else:
        leaf = manifest["archivalRestReceiptFile"]
        if Path(leaf).name != leaf or not leaf.startswith("processed-invoice-"):
            raise app.app.Stop("EDIT_ARCHIVAL_RECEIPT_SCOPE")
        receipt = checked(ROOT.parent / "app" / leaf, manifest["archivalRestReceiptSha256"])
        baseline = project_rest(receipt["mutation"], manifest["mutationNumber"])
        plan = make_plan(baseline, None, manifest, "ARCHIVAL_SAVED_REST_PROJECTION_NOT_CURRENT",
                         {"file": leaf, "sha256": manifest["archivalRestReceiptSha256"]})
    output.note("Voorbereiding, schrijven geblokkeerd: " + str(output.save("edit-plan", plan)))


if __name__ == "__main__":
    try:
        main()
    except app.RequestFailure as exc:
        print("Gestopt:", exc.label, str(exc), flush=True)
    except (app.app.Stop, base.CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: EDIT_PREPARATION_LOCAL_FAILURE; geen schrijfroute beschikbaar.", flush=True)
