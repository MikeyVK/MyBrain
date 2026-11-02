from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""Exactly one owner-authorized purchase-row ledger correction, hypothesis A."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = runtime_area("ledger")
import prepare_edit as prep
import processed_invoice_probe as transport
from app_session import AppAuthentication
from private_output import PrivateOutput

base, core = prep.base, prep.app


def load_input(path, expected):
    item = prep.checked(path, expected)
    if item.get("scope") != "ONE_OWNER_AUTHORIZED_ROW_LEDGER_CHANGE_A_ONLY":
        raise core.app.Stop("LEDGER_TRIAL_SCOPE")
    before, after, payload = item["restBefore"], item["restAfter"], item["payloadA"]
    if before.get("type") != 1 or len(before.get("rows", [])) != 1:
        raise core.app.Stop("LEDGER_TRIAL_ONLY_SINGLE_ROW_PURCHASE")
    if before["rows"][0].get("costCenterId") is not None:
        raise core.app.Stop("LEDGER_TRIAL_COST_CENTER_WRITE_PRESERVATION_UNPROVED_STOP")
    wanted = "/rows/0/ledgerId"
    if prep.field_diff(before, after) != [{"path": wanted, "before": item["oldLedgerId"], "after": item["newLedgerId"]}]:
        raise core.app.Stop("LEDGER_TRIAL_EXTRA_REST_CHANGE")
    keys = {"id", "mutatieNummer", "factuurNummer", "datum", "boekstuk", "omschrijving", "soort",
            "grootboekRekeningId", "isInclusiefBtw", "termijnInDagen", "relatieId", "mutatieRegels"}
    if set(payload) != keys or len(payload["mutatieRegels"]) != 1:
        raise core.app.Stop("LEDGER_TRIAL_A_PAYLOAD_CHANGED")
    row = payload["mutatieRegels"][0]
    if set(row) != {"index", "tegenRekeningId", "btwCode", "bedrag", "omschrijving"} or row["tegenRekeningId"] != item["newLedgerId"]:
        raise core.app.Stop("LEDGER_TRIAL_A_ROW_CHANGED")
    if (payload["mutatieNummer"] != before["id"] or payload["factuurNummer"] != before["invoiceNumber"]
            or payload["datum"][:10] != before["date"] or payload["soort"] != 1
            or payload["relatieId"] != before["relationId"] or payload["grootboekRekeningId"] != before["ledgerId"]
            or payload["isInclusiefBtw"] != (before["inExVat"] == "IN") or payload["termijnInDagen"] != before["termOfPayment"]
            or payload["omschrijving"] != before["description"] or payload["boekstuk"] != before["entryNumber"]
            or row["bedrag"] != before["rows"][0]["amount"] or row["btwCode"] != before["rows"][0]["vatCode"]
            or row["omschrijving"] != before["rows"][0]["description"]):
        raise core.app.Stop("LEDGER_TRIAL_A_FINANCIAL_OR_IDENTITY_MISMATCH")
    return item


class AppMutationCommand:
    """Narrow one-shot command over the existing verified HTTP exchange."""
    def __init__(self, payload, factory=core.tls_connection, *, endpoint="/api/v4/mutaties"):
        if endpoint not in ("/api/v4/mutaties", "/api/v4/bestanden"):
            raise core.app.Stop("APP_PUT_ENDPOINT_NOT_ALLOWED")
        self.endpoint = endpoint
        self.payload_hash = prep.fingerprint(payload)
        self.transport = transport.Transport("app", factory=factory, command_policy=self.allowed)
        self.attempted = False

    def allowed(self, method, path, body):
        return method == "PUT" and path == self.endpoint and prep.fingerprint(body) == self.payload_hash

    def send(self, payload, token):
        if self.attempted or prep.fingerprint(payload) != self.payload_hash:
            raise core.app.Stop("LEDGER_TRIAL_NO_SECOND_PUT_OR_PAYLOAD_CHANGE")
        self.attempted = True
        return self.transport.request("PUT", self.endpoint, payload, token=token)


def read_rest(client, identifier):
    return base.redact(prep.project_rest(client.get("/v1/mutation/" + str(identifier)), identifier), client.secrets)


def validate_app_before(app_record, item):
    mapping = prep.identity_mapping(item["restBefore"], app_record)
    payload = item["payloadA"]
    if mapping["appInternalId"] != payload["id"]:
        raise core.app.Stop("LEDGER_TRIAL_FRESH_APP_INTERNAL_ID_CHANGED")
    for key in ("relatieId", "grootboekRekeningId", "isInclusiefBtw", "termijnInDagen", "boekstuk", "omschrijving", "soort"):
        if app_record.get(key) != payload[key]:
            raise core.app.Stop("LEDGER_TRIAL_APP_HEADER_DRIFT")
    rows = app_record.get("mutatieRegels")
    if not isinstance(rows, list) or len(rows) != 1:
        raise core.app.Stop("LEDGER_TRIAL_APP_ROW_COUNT_CHANGED")
    row = rows[0]
    expected = dict(payload["mutatieRegels"][0], tegenRekeningId=item["oldLedgerId"])
    if any(row.get(key) != value for key, value in expected.items()):
        raise core.app.Stop("LEDGER_TRIAL_APP_ROW_DRIFT")
    # Read-only calculated amount/VAT/display fields are deliberately NOT copied.
    return mapping


def validate_accounts(client, item):
    ledger = client.get("/v1/ledger/" + str(item["newLedgerId"]))
    if (not isinstance(ledger, dict) or ledger.get("id") != item["newLedgerId"] or str(ledger.get("code")) != item["newLedgerCode"]
            or ledger.get("category") not in ("BAL", "VW")):
        raise core.app.Stop("LEDGER_TRIAL_NEW_LEDGER_ID_CODE_CATEGORY_MISMATCH")


def prior_events(path, input_hash):
    if not path.exists():
        return []
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if any(event.get("inputHash") != input_hash for event in events):
        raise core.app.Stop("LEDGER_TRIAL_JOURNAL_OTHER_INPUT")
    return events


def safe_failure(exc, stage, response_id=None):
    code = str(exc) if isinstance(exc, core.app.Stop) and base.re.fullmatch(r"[A-Z0-9_]{1,180}", str(exc)) else type(exc).__name__
    value = {"stage": stage, "cause": code, "exceptionType": type(exc).__name__}
    if isinstance(exc, core.RequestFailure):
        value["safeErrorFields"] = exc.fields
    if core.app.positive_integer(response_id):
        value["receivedAppInternalId"] = response_id
    return value


def execute(client, session_factory, command, item, journal, input_hash, output):
    events = prior_events(journal, input_hash)
    current = read_rest(client, item["restBefore"]["id"])
    baseline_file = output.save("ledger-rest-before", {"mutation": current})
    baseline_ref = {"file": baseline_file.name, "sha256": hashlib.sha256(baseline_file.read_bytes()).hexdigest()}
    validate_accounts(client, item)
    if not prep.field_diff(item["restAfter"], current):
        event = {"state": "ALREADY_TARGET_VERIFIED_NO_PUT", "inputHash": input_hash,
                 "visibleMutationNumber": current["id"], "restEvidence": baseline_ref}
        output.append(journal, event)
        return event
    prep.optimistic_check(item["restBefore"], current)
    if events:
        raise core.app.Stop("LEDGER_TRIAL_PRIOR_ATTEMPT_STOP_NO_RETRY")
    session = session_factory()
    app_before = session.read_mutation(core.Transport(), current["id"], current["date"])
    mapping = validate_app_before(app_before, item)
    output.save("ledger-app-before", app_before)
    fresh = read_rest(client, current["id"])
    prep.optimistic_check(current, fresh)
    session.require_same_admin()
    pending = {"state": "PENDING", "inputHash": input_hash, "payloadHash": prep.fingerprint(item["payloadA"]),
               "visibleMutationNumber": current["id"], "appInternalIdBefore": mapping["appInternalId"], "restEvidence": baseline_ref}
    output.append(journal, pending)
    stage, response_id, rest_verified = "PUT_REQUEST", None, False
    try:
        response = command.send(item["payloadA"], session.token)
        if isinstance(response, dict) and core.app.positive_integer(response.get("id")):
            response_id = response["id"]
        stage = "OFFICIAL_REST_AFTER_READ"
        after = read_rest(client, current["id"])
        output.save("ledger-rest-after", {"mutation": after})
        differences = prep.field_diff(item["restAfter"], after)
        if differences:
            output.save("ledger-unexpected-rest-diff", differences)
            raise core.app.Stop("LEDGER_TRIAL_REST_AFTER_DIFF_NOT_ONLY_INTENDED_LEDGER")
        rest_verified = True
        if not isinstance(response, dict) or (response.get("mutatieNummer") is not None and response["mutatieNummer"] != current["id"]):
            raise core.app.Stop("LEDGER_TRIAL_PUT_RESPONSE_IDENTITY_UNKNOWN")
        stage = "APP_RELOOKUP_VISIBLE_NUMBER"
        app_after = session.read_mutation(core.Transport(), current["id"], current["date"])
        after_mapping = prep.identity_mapping(after, app_after)
        output.save("ledger-app-after", app_after)
        session.require_same_admin()
        verified = {**pending, "state": "VERIFIED", "receivedAppInternalId": response_id,
                    "appInternalIdAfter": after_mapping["appInternalId"], "officialRestOnlyDesiredLedgerDeltaVerified": True,
                    "noOtherBookkeepingArchiveBankOrSheetWrites": True, "noAutomaticFallbackBOrRollback": True}
        output.append(journal, verified)
        return verified
    except Exception as exc:
        diagnostic = safe_failure(exc, stage, response_id)
        output.append(journal, {**pending, "state": "UNCERTAIN", "officialRestDesiredStateVerified": rest_verified,
                                "diagnostic": diagnostic})
        raise core.app.Stop("LEDGER_TRIAL_STOPPED_RECONCILE_NO_RETRY_" + stage + "_" + diagnostic["cause"]) from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    core.app.set_private_acl(ROOT, (core.owner_sid(),))
    item = load_input(ROOT / "trial-input.json", args.manifest_sha256)
    output = PrivateOutput(ROOT)
    if not args.apply:
        output.note("Lokale trialA dry-run, geen API: " + str(output.save("ledger-dryrun", item)))
        return
    lock, journal = ROOT / "ledger-trial.lock", ROOT / "ledger-trial-journal.jsonl"
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.manifest_sha256)
    try:
        client = base.Client([], {"acceptedAmazonCentralCode": "unused"})
        number = item["restBefore"]["id"]
        client.paths = {"/v1/mutation/" + str(number), "/v1/ledger/" + str(item["newLedgerId"])}
        base.MAX_CALLS = 15
        access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
        response = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
        if not isinstance(response, dict) or not isinstance(response.get("token"), str) or not response["token"]:
            raise core.app.Stop("LEDGER_TRIAL_REST_SESSION_UNKNOWN")
        client.token = response["token"]
        client.secrets.append(client.token)
        secrets = client.secrets
        output = PrivateOutput(ROOT, secrets)
        try:
            def session_factory():
                login = core.load_login(core.WindowsBackend().api)
                session = AppAuthentication(transport.Transport("app", factory=core.tls_connection))
                session.login(login, item["expectedAppAdminId"])
                secrets.extend(session.secrets)
                return session
            command = AppMutationCommand(item["payloadA"])
            try:
                result = execute(client, session_factory, command, item, journal, args.manifest_sha256, output)
            except Exception as exc:
                output.save("ledger-stopped", safe_failure(exc, "COORDINATOR_PRE_OR_POST_WRITE"))
                raise
            output.note("TrialA gecontroleerd; privéresultaat: " + str(output.save("ledger-result", result)))
        finally:
            try:
                client.request("DELETE", "/v1/session")
                output.note("Tijdelijke REST-sessie ingetrokken.")
            except core.app.Stop:
                output.note("REST-sessiebeëindiging niet bevestigd.")
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        if sys.argv[1:2] == ["description"]:
            from metadata_repair import main as repair_main
            repair_main(["header"] + sys.argv[2:])
        else:
            main()
    except (core.app.Stop, base.CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: LEDGER_TRIAL_LOCAL_FAILURE; geen PUT herhalen, inspecteer privéjournal.", flush=True)
