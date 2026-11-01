from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""One existing archive file to one existing visible mutation; no other writes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import probe_link_contract as links
from app_session import AppAuthentication
from private_output import PrivateOutput

prep, core, files = links.prep, links.core, links.files
base = prep.base
ROOT = runtime_area("links")


def load_input(path, expected):
    item = prep.checked(path, expected)
    if (item.get("scope") != "ONE_EXISTING_FILE_ONE_EXISTING_MUTATION_LINK" or
            item["payload"] != {"fileId": item["fileId"], "soort": 1, "koppelId": item["restBefore"]["id"]}
            or item["restBefore"].get("type") != 1 or not core.app.positive_integer(item["fileId"])):
        raise core.app.Stop("LINK_ONE_MANIFEST_SCOPE")
    return item


class LinkCommand:
    def __init__(self, payload, factory=core.tls_connection):
        self.expected = prep.fingerprint(payload)
        self.attempted = False
        self.transport = files.Transport("app", factory=factory, command_policy=self.allowed)

    def allowed(self, method, path, body):
        return method == "POST" and path == "/api/v4/bestanden/koppel" and prep.fingerprint(body) == self.expected

    def send(self, payload, token):
        if self.attempted or prep.fingerprint(payload) != self.expected:
            raise core.app.Stop("LINK_ONE_NO_RETRY_OR_CHANGED_PAYLOAD")
        self.attempted = True
        return self.transport.request("POST", "/api/v4/bestanden/koppel", payload, token=token)


def rest_read(client, item):
    number = item["restBefore"]["id"]
    return base.redact(prep.project_rest(client.get("/v1/mutation/" + str(number)), number), client.secrets)


def linked_read(session, item):
    number = item["restBefore"]["id"]
    reader, body = links.linked_query(number)
    rows = links.project_files(reader.request("POST", "/api/v4/bestanden/gekoppeld", body, token=session.token), session.secrets)
    if any(row.get("fileId") == item["positiveControlFileId"] for row in rows):
        raise core.app.Stop("LINK_ONE_OTHER_MUTATION_CONTROL_FILE_RETURNED_STOP")
    return rows, links.matches_file(rows, item["fileId"], number, body)


def verify_file(reader, token, item):
    identifier = item["fileId"]
    metadata = reader.request("GET", "/api/v4/bestanden/bestand/" + str(identifier), token=token)
    if not isinstance(metadata, dict) or metadata.get("id") != identifier or metadata.get("naam") != item["fileName"]:
        raise core.app.Stop("LINK_ONE_ARCHIVE_ID_OR_NAME_CHANGED")
    data = reader.request("GET", "/api/v4/bestanden/download/" + str(identifier), token=token)
    if (data["mime"] != "application/pdf" or len(data["bytes"]) != item["fileSize"]
            or hashlib.sha256(data["bytes"]).hexdigest() != item["fileSha256"]):
        raise core.app.Stop("LINK_ONE_PDF_HASH_OR_SIZE_CHANGED")
    return {key: metadata.get(key) for key in links.archive.FILE_FIELDS}


def events(path, fingerprint):
    if not path.exists():
        return []
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if any(row.get("inputHash") != fingerprint for row in rows):
        raise core.app.Stop("LINK_ONE_JOURNAL_OTHER_INPUT")
    return rows


def diagnostic(exc, stage):
    cause = str(exc) if isinstance(exc, core.app.Stop) and base.re.fullmatch(r"[A-Z0-9_]{1,180}", str(exc)) else type(exc).__name__
    result = {"stage": stage, "cause": cause, "exceptionType": type(exc).__name__}
    if isinstance(exc, core.RequestFailure):
        result["safeErrorFields"] = exc.fields
    return result


def execute(client, session, command, file_reader, item, journal, fingerprint, output, read_only=False,
            query=linked_read, file_check=verify_file):
    before = rest_read(client, item)
    prep.optimistic_check(item["restBefore"], before)
    baseline = output.save("link-rest-before", {"mutation": before})
    number = before["id"]
    selected = session.read_mutation(core.Transport(), number, before["date"])
    mapping = prep.identity_mapping(before, selected)
    if mapping["appInternalId"] != item["expectedAppInternalId"]:
        raise core.app.Stop("LINK_ONE_FRESH_APP_INTERNAL_ID_CHANGED")
    metadata_before = file_check(file_reader, session.token, item)
    rows_before, matched_before = query(session, item)
    output.save("link-before-query", {"requestTargetMutationNumber": number, "files": rows_before,
                "returnedItemKoppelIdMeaning": "UNKNOWN_REFERENCE_NOT_REQUEST_TARGET_OR_PROVEN_UNLINK_ID"})
    if len(matched_before) > 1:
        raise core.app.Stop("LINK_ONE_DUPLICATE_TARGET_FILE_MEMBERSHIP")
    if rows_before and not matched_before:
        raise core.app.Stop("LINK_ONE_UNEXPECTED_PREEXISTING_OTHER_ATTACHMENTS_STOP_REVIEW")
    prep.optimistic_check(before, rest_read(client, item))
    session.require_same_admin()
    evidence = {"inputHash": fingerprint, "visibleMutationNumber": number, "fileId": item["fileId"],
                "appInternalIdGuard": mapping["appInternalId"], "metadataBefore": metadata_before,
                "beforeQueryFiles": rows_before, "restBaselineFile": baseline.name,
                "restBaselineFileSha256": hashlib.sha256(baseline.read_bytes()).hexdigest()}
    if matched_before:
        result = {**evidence, "state": "ALREADY_LINKED_VERIFIED_NO_WRITE", "pdfHashVerified": True,
                  "officialRestUnchanged": True, "noNewLinkAttempt": True}
        if not read_only:
            output.append(journal, result)
        return result
    if read_only:
        return {**evidence, "state": "MAIN_TARGET_READ_CHECKED_EMPTY_NO_WRITE", "pdfHashVerified": True,
                "officialRestUnchanged": True, "positiveControlFileNotReturned": True}
    if events(journal, fingerprint):
        raise core.app.Stop("LINK_ONE_PREVIOUS_ATTEMPT_STOP_NO_RETRY")
    pending = {**evidence, "state": "PENDING", "payloadHash": prep.fingerprint(item["payload"])}
    output.append(journal, pending)
    response, attempt_error = None, None
    try:
        response = command.send(item["payload"], session.token)
    except Exception as exc:
        attempt_error = diagnostic(exc, "LINK_POST_RESPONSE_UNKNOWN")
    # Read verification deliberately runs even after an uncertain POST response.
    # It never retries, modifies, deletes or rolls back anything.
    stage = "REST_AFTER_READ"
    try:
        after = rest_read(client, item)
        output.save("link-rest-after", {"mutation": after})
        prep.optimistic_check(before, after)
        stage = "LINKED_FILES_AFTER_QUERY"
        rows_after, matched_after = query(session, item)
        output.save("link-after-query", {"requestTargetMutationNumber": number, "files": rows_after})
        if len(matched_after) != 1 or len(rows_after) != 1:
            raise core.app.Stop("LINK_ONE_EXACT_NEW_FILE_MEMBERSHIP_NOT_CONFIRMED")
        stage = "PDF_AFTER_HASH"
        metadata_after = file_check(file_reader, session.token, item)
        session.require_same_admin()
        response_facts = {key: response.get(key) for key in ("fileId", "koppelId", "naam", "datum")} if isinstance(response, dict) else None
        if attempt_error is None and (not isinstance(response, dict) or response.get("fileId") != item["fileId"]):
            attempt_error = {"stage": "LINK_POST_RESPONSE", "cause": "RESPONSE_FILE_ID_UNCONFIRMED_BUT_READBACK_PROVEN"}
        result = {**pending, "state": "RECONCILED_VERIFIED_AFTER_UNKNOWN_RESPONSE" if attempt_error else "VERIFIED",
                  "attemptDiagnostic": attempt_error, "responseFacts": response_facts,
                  "afterQueryFiles": rows_after, "metadataAfter": metadata_after, "pdfHashVerifiedBeforeAndAfter": True,
                  "officialRestUnchanged": True, "linkPostAttemptCount": 1,
                  "responseReferenceDomain": "Record koppelId values separately; no unlink-ID or target-ID equivalence asserted",
                  "noUploadMutationBankSheetOrUnlinkWrites": True}
        output.append(journal, result)
        return result
    except Exception as exc:
        failure = diagnostic(exc, stage)
        output.append(journal, {**pending, "state": "UNCERTAIN", "attemptDiagnostic": attempt_error,
                                "verificationDiagnostic": failure})
        raise core.app.Stop("LINK_ONE_STOPPED_RECONCILE_NO_RETRY_" + stage + "_" + failure["cause"]) from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-sha256", required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--read-check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    core.app.set_private_acl(ROOT, (core.owner_sid(),))
    item = load_input(ROOT / "link-input.json", args.input_sha256)
    output = PrivateOutput(ROOT)
    if not args.read_check and not args.apply:
        output.note("Lokale koppeldry-run, geen API: " + str(output.save("link-dryrun", item)))
        return
    lock, journal = ROOT / "link-one.lock", ROOT / "link-one-journal.jsonl"
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.input_sha256)
    try:
        client = base.Client([], {"acceptedAmazonCentralCode": "unused"})
        client.paths = {"/v1/mutation/" + str(item["restBefore"]["id"])}
        base.MAX_CALLS = 10
        access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
        response = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
        if not isinstance(response, dict) or not isinstance(response.get("token"), str) or not response["token"]:
            raise core.app.Stop("LINK_ONE_REST_SESSION_UNKNOWN")
        client.token = response["token"]
        client.secrets.append(client.token)
        output = PrivateOutput(ROOT, client.secrets)
        try:
            login = core.load_login(core.WindowsBackend().api)
            session = AppAuthentication(files.Transport("app", factory=core.tls_connection))
            session.login(login, item["expectedAppAdminId"])
            client.secrets.extend(session.secrets)
            result = execute(client, session, LinkCommand(item["payload"]),
                files.Transport("app", file_id=item["fileId"], factory=core.tls_connection),
                item, journal, args.input_sha256, output, read_only=args.read_check)
            output.note("Koppelingcontrole; privéresultaat: " + str(output.save("link-result", result)))
        except Exception as exc:
            output.save("link-stopped", diagnostic(exc, "COORDINATOR_PRE_OR_POST_WRITE"))
            raise
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
        main()
    except (core.app.Stop, base.CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: LINK_ONE_LOCAL_FAILURE; geen POST herhalen, inspecteer privéjournal.", flush=True)
