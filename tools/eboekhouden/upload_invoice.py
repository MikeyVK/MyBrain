from toolkit_runtime import WORKROOT, runtime_area, private_path as runtime_private_path, live_connection
"""One hash-bound original PDF upload; no bookkeeping or archive-link writes."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys

ROOT = runtime_area("uploads")
import app_probe as core
import archive_read as archive
import processed_invoice_probe as files
from private_output import PrivateOutput
from app_session import AppAuthentication


def load_input(root, expected):
    raw = (root / "upload-input.json").read_bytes()
    if hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        raise core.app.Stop("UPLOAD_INPUT_FINGERPRINT_CHANGED")
    item = json.loads(raw)
    if (item.get("scope") != "ONE_ARCHIVE_UPLOAD_ONLY_NO_MUTATION_OR_LINK" or item.get("localCopy") != "source-invoice.pdf"
            or item.get("targetDirectoryId") != 0 or item.get("scan") is not False or item.get("mime") != "application/pdf"):
        raise core.app.Stop("UPLOAD_SCOPE_CHANGED")
    name = item.get("uploadFileName")
    if (not isinstance(name, str) or not name.lower().endswith(".pdf") or len(name) > 200
            or any(c in name for c in ("/", "\\", "\r", "\n"))):
        raise core.app.Stop("UPLOAD_FILENAME_INVALID")
    content = (root / item["localCopy"]).read_bytes()
    if (not content.startswith(b"%PDF-") or not 0 < len(content) <= 5 * 1024 * 1024 or len(content) != item.get("size")
            or hashlib.sha256(content).hexdigest() != item.get("sha256")):
        raise core.app.Stop("UPLOAD_PDF_FINGERPRINT_CHANGED")
    return item, content


def check_fresh_archive_name(item):
    name = item.get("uploadFileName")
    if (not isinstance(name, str) or not 5 <= len(name) <= 48 or not name.isascii()
            or not name.isprintable() or not name.lower().endswith(".pdf") or any(c in "/\\" for c in name)):
        raise core.app.Stop("UPLOAD_FRESH_NAME_MUST_BE_MAX48_PRINTABLE_ASCII_PDF")


def acknowledgement_diagnostic(result, item):
    """Allowlisted shape/predicate evidence only; never retain raw reply values."""
    def kind(value):
        return {type(None): "null", bool: "boolean", str: "string", int: "integer", float: "number", dict: "object", list: "array"}.get(type(value), "other")
    obj = result if isinstance(result, dict) else {}
    file = obj.get("file") if isinstance(obj.get("file"), dict) else {}
    predicates = {
        "responseIsObject": isinstance(result, dict),
        "savedIsTrue": obj.get("saved") is True,
        "scannedIsFalse": obj.get("scanned") is False,
        "originalFileNameMatches": obj.get("originalFileName") == item["uploadFileName"],
        "fileIsObject": isinstance(obj.get("file"), dict),
        "fileIdPositive": core.app.positive_integer(file.get("id")),
        "fileNameMatches": file.get("naam") == item["uploadFileName"],
        "fileDirectoryMatches": type(file.get("directoryId")) is int and file.get("directoryId") == 0,
    }
    diagnostic = {"jsonResponseType": kind(result),
        "knownKeys": {key: {"present": key in obj, "type": kind(obj.get(key)) if key in obj else "absent"}
            for key in ("saved", "scanned", "originalFileName", "file")},
        "knownFileKeys": {key: {"present": key in file, "type": kind(file.get(key)) if key in file else "absent"}
            for key in ("id", "naam", "directoryId")},
        "savedBoolean": obj.get("saved") if type(obj.get("saved")) is bool else None,
        "scannedBoolean": obj.get("scanned") if type(obj.get("scanned")) is bool else None,
        "originalFileNameLength": len(obj["originalFileName"]) if isinstance(obj.get("originalFileName"), str) else None,
        "fileNameLength": len(file["naam"]) if isinstance(file.get("naam"), str) else None,
        "predicates": predicates, "failedPredicates": [key for key, passed in predicates.items() if not passed],
        "unknownResponseNeverProvesFailedUploadOrRetrySafe": True}
    if predicates["fileIdPositive"]:
        diagnostic["unverifiedCandidateFileId"] = file["id"]
        diagnostic["candidateIsVerified"] = False
    return diagnostic


class UploadAPI:
    """Compose existing reviewed App auth, archive and binary transports."""
    def __init__(self, factory=core.tls_connection):
        self.factory = factory
        self.auth = files.Transport("app", factory=factory)
        self.authentication = AppAuthentication(self.auth)
        self.archive = archive.Transport(factory=factory)
        self.secrets = self.authentication.secrets
        self.upload_sent = False
        self.received_file_id = None
        self.ack_diagnostic = None

    def login(self, login, expected_admin):
        self.authentication.login(login, expected_admin)
        self.token, self.admin = self.authentication.token, self.authentication.admin

    def admin_now(self):
        return self.authentication.admin_now()

    def require_same_admin(self):
        self.authentication.require_same_admin()

    def listing(self, directory=None):
        path = "/api/v4/bestanden" + ("/" + str(directory) if directory is not None else "")
        value = self.archive.request("GET", path, token=self.token)
        result = archive.project_listing(value, self.secrets)
        if result["id"] != (0 if directory is None else directory):
            raise core.app.Stop("UPLOAD_DIRECTORY_IDENTITY_MISMATCH")
        return result

    def upload(self, item, content):
        if self.upload_sent:
            raise core.app.Stop("UPLOAD_ALREADY_ATTEMPTED_NO_RETRY")
        check_fresh_archive_name(item)
        self.upload_sent = True
        payload = {"fileName": item["uploadFileName"], "data": base64.b64encode(content).decode("ascii"),
                   "directoryId": 0, "scan": False}
        connection = live_connection(self.factory, "appapi.e-boekhouden.nl", timeout=20, context=files.ssl.create_default_context())
        try:
            connection.request("POST", "/api/v4/bestanden/upload", body=json.dumps(payload).encode("utf-8"),
                headers={"Authorization": "Bearer " + self.token, "Content-Type": "application/json", "Accept": "application/json"})
            response = connection.getresponse()
            content_type = response.getheader("Content-Type", "").split(";")[0].strip().lower()
            self.ack_diagnostic = {"httpStatus": response.status if type(response.status) is int else None,
                "contentType": "application/json" if content_type == "application/json" else "OTHER",
                "jsonParseCompleted": False}
            if response.status != 200:
                raise core.app.Stop("UPLOAD_HTTP_" + str(response.status))
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise core.app.Stop("UPLOAD_RESPONSE_NOT_JSON")
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise core.app.Stop("UPLOAD_RESPONSE_TOO_LARGE")
            result = json.loads(raw)
            self.ack_diagnostic.update({"jsonParseCompleted": True, **acknowledgement_diagnostic(result, item)})
            file = result.get("file") if isinstance(result, dict) else None
            if isinstance(file, dict) and core.app.positive_integer(file.get("id")):
                self.received_file_id = file["id"]
            if self.ack_diagnostic["failedPredicates"]:
                raise core.app.Stop("UPLOAD_SAVE_RESPONSE_UNKNOWN")
            return file["id"]
        except core.app.Stop:
            raise
        except Exception as exc:
            raise core.app.Stop("UPLOAD_OUTCOME_UNCERTAIN_" + type(exc).__name__) from exc
        finally:
            connection.close()

    def verify(self, identifier, item, expected_directory=0):
        if type(expected_directory) is not int or expected_directory < 0:
            raise core.app.Stop("UPLOAD_VERIFY_DIRECTORY_NOT_ADMITTED")
        transport = files.Transport("app", file_id=identifier, factory=self.factory)
        metadata = transport.request("GET", "/api/v4/bestanden/bestand/" + str(identifier), token=self.token)
        if (not isinstance(metadata, dict) or metadata.get("id") != identifier or metadata.get("naam") != item["uploadFileName"]
                or type(metadata.get("directoryId")) is not int or metadata.get("directoryId") != expected_directory):
            raise core.app.Stop("UPLOAD_READBACK_METADATA_MISMATCH")
        result = transport.request("GET", "/api/v4/bestanden/download/" + str(identifier), token=self.token)
        if (result["mime"] != "application/pdf" or len(result["bytes"]) != item["size"]
                or hashlib.sha256(result["bytes"]).hexdigest() != item["sha256"]):
            raise core.app.Stop("UPLOAD_DOWNLOAD_HASH_MISMATCH")
        return {key: metadata.get(key) for key in archive.FILE_FIELDS}


def candidate_listings(api, item):
    root = api.listing()
    if root.get("isMailEnHerkenInbox") is not True:
        raise core.app.Stop("UPLOAD_TARGET_ROOT_PROPERTIES_CHANGED")
    lists = [root]
    years = [d for d in root["directories"] if d["naam"] == item["invoiceDate"][:4]]
    if len(years) > 1:
        raise core.app.Stop("UPLOAD_DUPLICATE_YEAR_DIRECTORIES")
    if years:
        lists.append(api.listing(years[0]["id"]))
    return lists


def duplicate_check(api, item):
    lists = candidate_listings(api, item)
    number = item["sourceInvoiceNumber"].casefold()
    for listing in lists:
        for candidate in listing["files"] + listing["directories"]:
            if candidate["naam"].casefold() == item["uploadFileName"].casefold() or number in candidate["naam"].casefold():
                raise core.app.Stop("UPLOAD_EXISTING_FILENAME_OR_INVOICE_REFERENCE_STOP_REUSE_REVIEW")
    return {"directoriesChecked": [listing["id"] for listing in lists],
            "scope": "Root and existing invoice-year direct listing only; not global archive absence proof"}


def journal_state(path, fingerprint):
    if not path.exists():
        return None
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if not events or any(event.get("inputHash") != fingerprint for event in events):
        raise core.app.Stop("UPLOAD_JOURNAL_OTHER_INPUT_OR_INVALID")
    latest = events[-1]
    if latest.get("state") not in ("VERIFIED", "RECONCILED_VERIFIED") or not core.app.positive_integer(latest.get("fileId")):
        raise core.app.Stop("UPLOAD_PREVIOUS_OUTCOME_UNCERTAIN_NO_RETRY")
    return latest


def execute(api, login, admin, item, content, output, journal, fingerprint):
    previous = journal_state(journal, fingerprint)
    if previous is None:
        check_fresh_archive_name(item)
    api.login(login, admin)
    if previous:
        metadata = api.verify(previous["fileId"], item)
        api.require_same_admin()
        return {"state": "PREVIOUS_UPLOAD_VERIFIED_NO_NEW_WRITE", "fileId": previous["fileId"], "metadata": metadata}
    duplicate_scope = duplicate_check(api, item)
    api.require_same_admin()
    pending = {"state": "PENDING", "inputHash": fingerprint, "fileSha256": item["sha256"], "directoryId": 0}
    output.append(journal, pending)
    stage, identifier = "UPLOAD_REQUEST", None
    try:
        identifier = api.upload(item, content)
        stage = "READBACK_METADATA_AND_DOWNLOAD"
        metadata = api.verify(identifier, item)
        stage = "ADMINISTRATION_RECHECK"
        api.require_same_admin()
        verified = {**pending, "state": "VERIFIED", "fileId": identifier}
        output.append(journal, verified)
        return {**verified, "metadata": metadata, "downloadSha256Matches": True, "duplicateScope": duplicate_scope,
                "scanRequested": False, "noMutationBankOrArchiveLinkWrites": True,
                "acknowledgement": getattr(api, "ack_diagnostic", None)}
    except Exception as exc:
        cause = str(exc) if isinstance(exc, core.app.Stop) and core.re.fullmatch(r"[A-Z0-9_]{1,160}", str(exc)) else type(exc).__name__
        diagnostic = {"stage": stage, "cause": cause, "exceptionType": type(exc).__name__}
        received = identifier if core.app.positive_integer(identifier) else getattr(api, "received_file_id", None)
        if core.app.positive_integer(received):
            diagnostic["receivedFileId"] = received
        if type(getattr(exc, "errno", None)) is int:
            diagnostic["errno"] = exc.errno
        if isinstance(exc, core.RequestFailure):
            diagnostic["safeErrorFields"] = exc.fields
        if getattr(api, "ack_diagnostic", None) is not None:
            diagnostic["acknowledgement"] = api.ack_diagnostic
        if core.app.positive_integer(received):
            diagnostic["receivedFileIdVerification"] = "UNVERIFIED_RESPONSE_CANDIDATE_ONLY"
        output.append(journal, {**pending, "state": "UNCERTAIN", "diagnostic": diagnostic})
        raise core.app.Stop("UPLOAD_STOPPED_RECONCILE_JOURNAL_NO_RETRY_" + stage + "_" + cause) from exc


def relevant_legacy_journal(root, item):
    path = root / "upload-journal.jsonl"
    if not path.exists():
        return None
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if any(event.get("fileSha256") == item["sha256"] for event in events):
        if not events or any(event.get("fileSha256") != item["sha256"] for event in events):
            raise core.app.Stop("UPLOAD_LEGACY_MIXED_SOURCE_JOURNAL")
        return path, events
    return None


def require_source_not_uncertain(root, item):
    legacy = relevant_legacy_journal(root, item)
    if legacy and legacy[1][-1].get("state") not in ("VERIFIED", "RECONCILED_VERIFIED"):
        raise core.app.Stop("UPLOAD_PREVIOUS_OUTCOME_UNCERTAIN_SAME_BYTES_NO_RETRY")
    return legacy


def reconcile_readonly(api, login, admin, item, output, journal, fingerprint, legacy=None):
    """Read metadata and hash at most three exact-name/number candidates; never upload."""
    api.login(login, admin)
    lists = candidate_listings(api, item)
    number = item["sourceInvoiceNumber"].casefold()
    candidates = {f["id"]: f for listing in lists for f in listing["files"]
        if f["naam"].casefold() == item["uploadFileName"].casefold() or number in f["naam"].casefold()}
    result = {"state": "UNRESOLVED_NO_RETRY", "inputHash": fingerprint, "fileSha256": item["sha256"],
        "directoriesChecked": [listing["id"] for listing in lists], "candidateIds": list(candidates),
        "noUploadOrFinancialWrites": True, "absenceIsNotProofOfFailedUpload": True}
    if len(candidates) == 1:
        identifier = next(iter(candidates))
        try:
            metadata = api.verify(identifier, item)
        except core.app.Stop as exc:
            result["verificationFailure"] = str(exc) if core.re.fullmatch(r"[A-Z0-9_]{1,160}", str(exc)) else type(exc).__name__
        else:
            api.require_same_admin()
            event = {"state": "RECONCILED_VERIFIED", "inputHash": fingerprint, "fileSha256": item["sha256"],
                     "directoryId": 0, "fileId": identifier, "readOnlyReconciliation": True}
            output.append(journal, event)
            if legacy and legacy[0] != journal:
                output.append(legacy[0], {**event, "inputHash": legacy[1][0]["inputHash"]})
            return {**result, **event, "metadata": metadata, "downloadSha256Matches": True}
    elif len(candidates) > 3:
        result["verificationFailure"] = "TOO_MANY_CANDIDATES_STOP_NO_DOWNLOAD"
    api.require_same_admin()
    output.append(journal, {"state": "RECONCILIATION_UNRESOLVED", "inputHash": fingerprint,
        "fileSha256": item["sha256"], "candidateCount": len(candidates), "noRetry": True})
    return result


def hash_bound_json(path, expected, maximum=131072):
    if not isinstance(expected, str) or not core.re.fullmatch(r"[a-fA-F0-9]{64}", expected):
        raise core.app.Stop("UPLOAD_RECOVERY_HASH_REQUIRED")
    raw = path.read_bytes()
    if len(raw) > maximum or hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        raise core.app.Stop("UPLOAD_RECOVERY_BOUND_FILE_CHANGED")
    return json.loads(raw)


def private_path(root, relative):
    if not isinstance(relative, str):
        raise core.app.Stop("UPLOAD_RECOVERY_PRIVATE_PATH_REQUIRED")
    path = (root.parent / relative).resolve()
    if not path.is_relative_to(root.parent.resolve()) or path.is_symlink():
        raise core.app.Stop("UPLOAD_RECOVERY_PATH_OUTSIDE_PRIVATE_ROOT")
    return path


def validate_old_recovery_files(root, entry):
    old_input = private_path(root, entry.get("oldInput"))
    if old_input.name != "upload-input.json":
        raise core.app.Stop("UPLOAD_RECOVERY_OLD_INPUT_SCOPE")
    old, content = load_input(old_input.parent, entry["oldInputSha256"])
    if old["sha256"] != entry["sourceSha256"]:
        raise core.app.Stop("UPLOAD_RECOVERY_OLD_SOURCE_CHANGED")
    journal = private_path(root, entry.get("oldJournal"))
    if journal not in ((root / "upload-journal.jsonl").resolve(),
            (root / "pdf-cases" / entry["sourceSha256"] / "upload-journal.jsonl").resolve()):
        raise core.app.Stop("UPLOAD_RECOVERY_OLD_JOURNAL_SCOPE")
    raw = journal.read_bytes()
    if len(raw) > 131072 or hashlib.sha256(raw).hexdigest() != entry["oldJournalSha256"]:
        raise core.app.Stop("UPLOAD_RECOVERY_OLD_JOURNAL_CHANGED")
    events = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    if (not events or not any(e.get("state") == "UNCERTAIN" for e in events)
            or events[-1].get("state") not in ("UNCERTAIN", "RECONCILIATION_UNRESOLVED")
            or any(e.get("inputHash", "").lower() != entry["oldInputSha256"].lower()
                   or e.get("fileSha256") != entry["sourceSha256"] for e in events)):
        raise core.app.Stop("UPLOAD_RECOVERY_OLD_UNCERTAINTY_BINDING_CHANGED")
    return old


def load_recovery_authorization(root, auth_path, auth_hash, item, input_path, input_hash, admin):
    path = private_path(root, str(auth_path))
    document = hash_bound_json(path, auth_hash)
    decision = document.get("ownerDecision") if isinstance(document, dict) else None
    if (not isinstance(document, dict) or document.get("scope") != "EXACT_THREE_OWNER_AUTHORIZED_UPLOAD_RECOVERIES"
            or not isinstance(decision, dict) or decision.get("authority") != "OWNER_DIRECT"
            or decision.get("acceptedPossibleDuplicateArchiveFile") is not True):
        raise core.app.Stop("UPLOAD_RECOVERY_EXPLICIT_OWNER_AUTHORIZATION_REQUIRED")
    entries = document.get("entries")
    if (not isinstance(entries, list) or len(entries) != 3
            or any(not isinstance(e, dict) or not core.re.fullmatch(r"[a-f0-9]{64}", str(e.get("sourceSha256", ""))) for e in entries)
            or len({e["sourceSha256"] for e in entries}) != 3):
        raise core.app.Stop("UPLOAD_RECOVERY_EXACT_THREE_SOURCE_BINDINGS_REQUIRED")
    selected = [e for e in entries if e["sourceSha256"] == item["sha256"]]
    if len(selected) != 1:
        raise core.app.Stop("UPLOAD_RECOVERY_SOURCE_NOT_AUTHORIZED")
    entry = selected[0]
    if (type(entry.get("maximumAdditionalPosts")) is not int or entry["maximumAdditionalPosts"] != 1
            or type(entry.get("adminId")) is not int or entry["adminId"] != admin
            or type(entry.get("directoryId")) is not int or entry["directoryId"] != 0
            or entry.get("newInputSha256", "").lower() != input_hash.lower()
            or private_path(root, entry.get("newInput")) != input_path.resolve()):
        raise core.app.Stop("UPLOAD_RECOVERY_TARGET_INPUT_ADMIN_OR_ATTEMPT_BOUND_CHANGED")
    old = validate_old_recovery_files(root, entry)
    if (item.get("originalSourceFileName") != old["uploadFileName"]
            or item["sourceInvoiceNumber"] != old["sourceInvoiceNumber"]
            or item["invoiceDate"] != old["invoiceDate"] or item["size"] != old["size"]):
        raise core.app.Stop("UPLOAD_RECOVERY_SOURCE_IDENTITY_CHANGED")
    check_fresh_archive_name(item)
    return {"entry": entry, "authorizationSha256": auth_hash.lower()}


def recovery_state(path, source_sha, authorization_sha):
    if not path.exists():
        return None
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if (not events or any(e.get("fileSha256") != source_sha or e.get("authorizationSha256") != authorization_sha for e in events)):
        raise core.app.Stop("UPLOAD_RECOVERY_SOURCE_ALREADY_BOUND_NO_NEW_ATTEMPT")
    last = events[-1]
    if last.get("state") not in ("RECOVERY_UPLOAD_VERIFIED", "EXISTING_FILE_VERIFIED_NO_EXTRA_POST") or not core.app.positive_integer(last.get("fileId")):
        raise core.app.Stop("UPLOAD_RECOVERY_PREVIOUS_OUTCOME_NO_EXTRA_RETRY")
    return last


def recovery_candidates(api, item):
    lists = candidate_listings(api, item)
    names = {item["uploadFileName"].casefold(), item["originalSourceFileName"].casefold()}
    number = item["sourceInvoiceNumber"].casefold()
    candidates = {}
    for listing in lists:
        for candidate in listing["files"]:
            if candidate["naam"].casefold() in names or number in candidate["naam"].casefold():
                if candidate["id"] in candidates:
                    raise core.app.Stop("UPLOAD_RECOVERY_AMBIGUOUS_LISTED_ID")
                candidates[candidate["id"]] = {**candidate, "searchedDirectoryId": listing["id"]}
    return list(candidates.values()), {"directoriesChecked": [v["id"] for v in lists],
        "scope": "Root and existing exact invoice-year direct listings only; not global failure or absence proof",
        "possibleDuplicateArchiveFileRiskAcceptedByOwner": True}


def recover_once(api, login, admin, item, content, output, journal, fingerprint, spec, root):
    previous = recovery_state(journal, item["sha256"], spec["authorizationSha256"])
    validate_old_recovery_files(root, spec["entry"])
    check_fresh_archive_name(item)
    api.login(login, admin)
    candidates, scope = recovery_candidates(api, item)
    api.require_same_admin()
    facts = {"inputHash": fingerprint, "fileSha256": item["sha256"], "authorizationSha256": spec["authorizationSha256"],
        "oldInputSha256": spec["entry"]["oldInputSha256"], "oldJournalSha256": spec["entry"]["oldJournalSha256"],
        "oldJournal": spec["entry"]["oldJournal"], "archiveReadScope": scope, "postDirectoryId": 0}
    if len(candidates) > 1:
        raise core.app.Stop("UPLOAD_RECOVERY_MULTIPLE_CANDIDATES_NO_POST")
    if candidates:
        candidate = candidates[0]
        if previous and candidate["id"] != previous["fileId"]:
            raise core.app.Stop("UPLOAD_RECOVERY_PREVIOUS_FILE_ID_CHANGED")
        metadata = api.verify(candidate["id"], {**item, "uploadFileName": candidate["naam"]},
                              expected_directory=candidate["searchedDirectoryId"])
        api.require_same_admin()
        validate_old_recovery_files(root, spec["entry"])
        if previous:
            return {**previous, "metadata": metadata, "noNewPost": True, "extraPostAttemptCountThisRun": 0}
        event = {**facts, "state": "EXISTING_FILE_VERIFIED_NO_EXTRA_POST", "fileId": candidate["id"],
                 "extraPostAttemptCount": 0, "directoryId": candidate["searchedDirectoryId"], "downloadSha256Matches": True}
        output.append(journal, event)
        return {**event, "metadata": metadata, "noMutationBankOrArchiveLinkWrites": True}
    if previous:
        raise core.app.Stop("UPLOAD_RECOVERY_PREVIOUS_VERIFIED_FILE_NOT_IN_SCOPE_NO_POST")
    validate_old_recovery_files(root, spec["entry"])
    pending = {**facts, "state": "PENDING", "extraPostAttemptCount": 1, "directoryId": 0}
    output.append(journal, pending)
    stage, identifier = "RECOVERY_UPLOAD_REQUEST", None
    try:
        identifier = api.upload(item, content)
        stage = "RECOVERY_METADATA_DOWNLOAD_HASH"
        metadata = api.verify(identifier, item)
        api.require_same_admin()
        validate_old_recovery_files(root, spec["entry"])
        verified = {**pending, "state": "RECOVERY_UPLOAD_VERIFIED", "fileId": identifier,
                    "downloadSha256Matches": True}
        output.append(journal, verified)
        return {**verified, "metadata": metadata, "acknowledgement": getattr(api, "ack_diagnostic", None),
                "noMutationBankOrArchiveLinkWrites": True}
    except Exception as exc:
        cause = str(exc) if isinstance(exc, core.app.Stop) and core.re.fullmatch(r"[A-Z0-9_]{1,160}", str(exc)) else type(exc).__name__
        diagnostic = {"stage": stage, "cause": cause, "exceptionType": type(exc).__name__}
        candidate_id = identifier if core.app.positive_integer(identifier) else getattr(api, "received_file_id", None)
        if core.app.positive_integer(candidate_id):
            diagnostic["unverifiedCandidateFileId"] = candidate_id
        if getattr(api, "ack_diagnostic", None) is not None:
            diagnostic["acknowledgement"] = api.ack_diagnostic
        output.append(journal, {**pending, "state": "UNCERTAIN", "diagnostic": diagnostic})
        raise core.app.Stop("UPLOAD_RECOVERY_STOPPED_NO_FURTHER_POST_" + stage + "_" + cause) from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-sha256", required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--reconcile-readonly", action="store_true")
    parser.add_argument("--recover-once", action="store_true")
    parser.add_argument("--recovery-authorization", type=Path)
    parser.add_argument("--recovery-authorization-sha256")
    parser.add_argument("--admin-id", type=int)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    core.app.set_private_acl(ROOT, (core.owner_sid(),))
    input_path = runtime_private_path(args.input or ROOT / "upload-input.json")
    if not input_path.is_relative_to(ROOT.parent.resolve()) or input_path.is_symlink():
        raise core.app.Stop("UPLOAD_INPUT_OUTSIDE_PRIVATE_ROOT")
    if sum((args.apply, args.reconcile_readonly, args.recover_once)) > 1:
        raise core.app.Stop("UPLOAD_ACTION_MODES_CONFLICT")
    if args.recover_once != bool(args.recovery_authorization and args.recovery_authorization_sha256):
        raise core.app.Stop("UPLOAD_RECOVERY_AUTHORIZATION_ARGUMENTS_REQUIRED")
    if not args.recover_once and (args.recovery_authorization or args.recovery_authorization_sha256):
        raise core.app.Stop("UPLOAD_RECOVERY_AUTHORIZATION_OUTSIDE_RECOVERY_MODE")
    if input_path.name != "upload-input.json":
        raise core.app.Stop("UPLOAD_INPUT_BASENAME_REQUIRED")
    item, content = load_input(input_path.parent, args.input_sha256)
    output = PrivateOutput(ROOT)
    spec = None
    if args.recover_once:
        spec = load_recovery_authorization(ROOT, args.recovery_authorization,
            args.recovery_authorization_sha256, item, input_path, args.input_sha256, args.admin_id)
    if not args.apply and not args.reconcile_readonly and not args.recover_once:
        path = output.save("upload-dryrun", {"state": "LOCAL_DRYRUN_NO_API", "inputHash": args.input_sha256,
            "fileName": item["uploadFileName"], "size": len(content), "sha256": item["sha256"], "directoryId": 0, "scan": False})
        output.note("Lokale dry-run, geen API: " + str(path))
        return
    if not core.app.positive_integer(args.admin_id):
        raise core.app.Stop("UPLOAD_EXPECTED_ADMIN_REQUIRED")
    case_root = ROOT / "pdf-cases" / item["sha256"]
    case_root.mkdir(parents=True, exist_ok=True)
    core.app.set_private_acl(case_root, (core.owner_sid(),))
    journal = case_root / "controlled-recovery-journal.jsonl" if args.recover_once else (
        case_root / "upload-journal.jsonl" if args.input else ROOT / "upload-journal.jsonl")
    lock = case_root / "upload.lock"
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.input_sha256)
    try:
        # Reject uncertain historical attempts before accessing credentials.
        legacy = relevant_legacy_journal(ROOT, item)
        if args.recover_once:
            recovery_state(journal, item["sha256"], spec["authorizationSha256"])
        elif not args.reconcile_readonly:
            require_source_not_uncertain(ROOT, item)
            # Canonical byte identity applies even when the legacy/default CLI is used.
            canonical = case_root / "upload-journal.jsonl"
            if canonical != journal and canonical.exists():
                journal_state(canonical, args.input_sha256)
            if legacy and legacy[0] != journal and not journal.exists():
                raise core.app.Stop("UPLOAD_EXISTING_LEGACY_SAME_BYTES_RECONCILE_REUSE_NOT_REUPLOAD")
            prior = journal_state(journal, args.input_sha256)
            if prior is None:
                check_fresh_archive_name(item)
        login = core.load_login(core.WindowsBackend().api)
        api = UploadAPI()
        output = PrivateOutput(ROOT, api.secrets)
        if args.recover_once:
            result = recover_once(api, login, args.admin_id, item, content, output, journal,
                                  args.input_sha256, spec, ROOT)
        elif args.reconcile_readonly:
            result = reconcile_readonly(api, login, args.admin_id, item, output, journal, args.input_sha256, legacy)
        else:
            result = execute(api, login, args.admin_id, item, content, output, journal, args.input_sha256)
        path = output.save("upload-result", result)
        output.note("Upload gecontroleerd; privÃƒÆ’Ã‚Â©resultaat: " + str(path))
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except core.app.Stop as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: UPLOAD_LOCAL_FAILURE; inspecteer privÃƒÆ’Ã‚Â©journal, niet blind herhalen.", flush=True)
