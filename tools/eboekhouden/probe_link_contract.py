from toolkit_runtime import WORKROOT, runtime_area
"""One read-only linked-file hypothesis probe; no link/write endpoint allowed."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = runtime_area("links")
import prepare_edit as prep
import processed_invoice_probe as files
import archive_read as archive
from app_session import AppAuthentication
from private_output import PrivateOutput

core = prep.app


class LinkShapeFailure(core.app.Stop):
    def __init__(self, value, secrets):
        super().__init__("LINK_READ_ITEM_OR_LIST_SHAPE_UNKNOWN")
        self.shape = archive.shape_only(value, tuple(secrets))


def linked_query(visible_number, factory=core.tls_connection):
    if not core.app.positive_integer(visible_number):
        raise core.app.Stop("LINK_READ_VISIBLE_NUMBER_INVALID")
    body = {"soort": 1, "koppelId": visible_number}
    def allowed(method, path, candidate):
        return method == "POST" and path == "/api/v4/bestanden/gekoppeld" and candidate == body
    return files.Transport("app", factory=factory, command_policy=allowed), body


def project_files(value, secrets):
    rows = value.get("files") if isinstance(value, dict) else None
    if not isinstance(rows, list) or len(rows) > 100:
        raise LinkShapeFailure(value, secrets)
    result = []
    for row in rows:
        if not isinstance(row, dict) or not any(core.app.positive_integer(row.get(k)) for k in ("fileId", "id")):
            raise LinkShapeFailure(value, secrets)
        selected = {}
        for key in ("fileId", "id", "koppelId", "naam", "datum", "directoryId", "scanStatus"):
            if key in row:
                field = row[key]
                if field is not None and ((key in ("naam", "datum") and not isinstance(field, str))
                        or (key not in ("naam", "datum") and type(field) is not int)):
                    raise LinkShapeFailure(value, secrets)
                selected[key] = prep.base.redact(row[key], secrets)
        result.append(selected)
    return result


def matches_file(rows, expected_file, expected_visible, query_body):
    # Actual read evidence established that item.koppelId differs from request
    # target. Its namespace remains unknown. Scope comes from the exact request
    # plus verified mutation/admin context, not that response reference field.
    if query_body != {"soort": 1, "koppelId": expected_visible}:
        raise core.app.Stop("LINK_READ_REQUEST_TARGET_SCOPE_MISMATCH")
    return [r for r in rows if r.get("fileId") == expected_file]


def run(session, item, query_factory=linked_query, metadata_factory=None, diagnostic_output=None):
    raw = session.read_mutation_raw(core.Transport(), item["visibleMutationNumber"], item["knownDate"])
    if raw.get("mutatieNummer") != item["visibleMutationNumber"] or raw.get("factuurNummer") != item["invoiceNumber"]:
        raise core.app.Stop("LINK_PROBE_MUTATION_IDENTITY_MISMATCH")
    selected = core.app.project_record(raw, tuple(session.secrets))
    reader = metadata_factory(item["knownFileId"]) if metadata_factory else files.Transport("app", file_id=item["knownFileId"], factory=core.tls_connection)
    metadata = reader.request("GET", "/api/v4/bestanden/bestand/" + str(item["knownFileId"]), token=session.token)
    if (not isinstance(metadata, dict) or metadata.get("id") != item["knownFileId"]
            or not isinstance(metadata.get("naam"), str) or item["invoiceNumber"] not in metadata["naam"]):
        raise core.app.Stop("LINK_PROBE_ARCHIVE_FILE_IDENTITY_MISMATCH")
    query, body = query_factory(item["visibleMutationNumber"])
    rows = project_files(query.request("POST", "/api/v4/bestanden/gekoppeld", body, token=session.token), session.secrets)
    session.require_same_admin()
    if diagnostic_output is not None:
        # Preserve observed values before interpreting the undocumented item-level
        # koppelId. A same-file hit alone is explicitly not target-contract proof.
        diagnostic = {"state": "READ_ONLY_LINK_QUERY_DIAGNOSTIC_BEFORE_TARGET_INTERPRETATION", "queryBody": body,
                      "visibleMutationNumber": item["visibleMutationNumber"], "actualAppInternalId": raw["id"],
                      "knownFileId": item["knownFileId"], "projectedLinkedFilesMetadata": rows,
                      "sameFileIdCandidatesWithoutTargetClaim": [r for r in rows if r.get("fileId", r.get("id")) == item["knownFileId"]],
                      "targetContractProven": False, "itemKoppelIdMeaning": "UNKNOWN_NOT_ASSUMED_IDENTICAL_TO_REQUEST_TARGET",
                      "noLinkUploadMutationBankOrSheetWrites": True}
        path = diagnostic_output.save("link-read-diagnostic", diagnostic)
        diagnostic_output.note("Privé read-querydiagnostiek vóór interpretatie: " + str(path))
    matched = matches_file(rows, item["knownFileId"], item["visibleMutationNumber"], body)
    extras = {k:v for k,v in raw.items() if k not in selected}
    return {"state": "READ_ONLY_LINK_CONTRACT_PROBE", "hypothesis": body,
            "visibleMutationNumber": item["visibleMutationNumber"], "actualAppInternalId": raw["id"],
            "knownFileId": item["knownFileId"], "knownFileFoundInLinkedQuery": len(matched) == 1,
            "matchedFileRows": matched, "linkedFilesMetadata": rows,
            "itemKoppelIdMeaning": "UNKNOWN_RESPONSE_REFERENCE_NOT_REQUEST_TARGET_OR_PROVEN_UNLINK_ID",
            "archiveMetadata": {k: metadata.get(k) for k in archive.FILE_FIELDS},
            "mutationExtraFieldShapes": archive.shape_only(extras, tuple(session.secrets)),
            "noLinkUploadMutationBankOrSheetWrites": True,
            "findingScope": "Positive exact known-file membership supports this one soort1/visible-number hypothesis; empty results do not prove other enums/namespaces wrong or link absent"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-sha256", required=True)
    args = parser.parse_args()
    core.app.set_private_acl(ROOT, (core.owner_sid(),))
    item = prep.checked(ROOT / "probe-input.json", args.input_sha256)
    if item.get("scope") != "ONE_READ_ONLY_KNOWN_MUTATION_FILE_LINK_HYPOTHESIS":
        raise core.app.Stop("LINK_PROBE_SCOPE")
    login = core.load_login(core.WindowsBackend().api)
    session = AppAuthentication(files.Transport("app", factory=core.tls_connection))
    session.login(login, item["expectedAppAdminId"])
    output = PrivateOutput(ROOT, session.secrets)
    result = run(session, item, diagnostic_output=output)
    output.note("Alleen-lezen koppelcontractproef: " + str(output.save("link-contract-read", result)))


if __name__ == "__main__":
    try:
        main()
    except LinkShapeFailure as exc:
        print("Gestopt:", str(exc), "alleen structuur:", json.dumps(exc.shape, ensure_ascii=True), flush=True)
    except core.RequestFailure as exc:
        print("Gestopt:", exc.label, str(exc), flush=True)
    except core.app.Stop as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: LINK_PROBE_LOCAL_FAILURE; geen alternatieve enum/ID-probes uitvoeren.", flush=True)
