from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""Explicit nine-supplier creation, locally dry-run by default."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import uuid

import preflight as base
import catalogue_match as matching
from private_output import PrivateOutput


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


def read_manifest(path, fingerprint):
    manifest = matching.checked(path, fingerprint)
    rows = manifest.get("relations")
    if manifest.get("scope") != "OWNER_AUTHORIZED_NINE_SUPPLIERS_ONLY" or not isinstance(rows, list) or len(rows) != 9:
        raise base.app.app.Stop("CREATE_MANIFEST_SCOPE")
    codes = set()
    limits = {"code": 15, "name": 100, "type": 1, "address": 150, "address2": 150, "postalCode": 50,
              "city": 50, "country": 50, "phoneNumber": 50, "emailAddress": 150, "website": 50,
              "vatNumber": 50, "companyRegistrationNumber": 50}
    for row in rows:
        payload = row.get("payload", {})
        if set(payload) - set(limits) - {"termOfPayment"} or not all(payload.get(k) for k in ("name", "code", "type")):
            raise base.app.app.Stop("CREATE_PAYLOAD_FIELDS")
        if payload["type"] != "B" or payload["code"] in codes:
            raise base.app.app.Stop("CREATE_PAYLOAD_IDENTITY")
        codes.add(payload["code"])
        for key, value in payload.items():
            if key == "termOfPayment":
                if type(value) is not int or not 0 <= value <= 365:
                    raise base.app.app.Stop("CREATE_TERM_INVALID")
            elif not isinstance(value, str) or not value or len(value) > limits[key] or any(ord(c) < 32 for c in value):
                raise base.app.app.Stop("CREATE_FIELD_INVALID")
    return manifest


class RelationAPI:
    """Supplier-specific facade over the shared narrow REST create command."""
    def __init__(self, client, payloads):
        from rest_create_command import RestCreateCommand
        self.command = RestCreateCommand(client, "/v1/relation", payloads)
        self.client = client

    def create(self, payload):
        return self.command.create(payload)


def same_payload(payload, detail):
    return all((detail.get(key) == value if key == "termOfPayment" else
                base.normalize(detail.get(key, "")) == base.normalize(value)) for key, value in payload.items())


def previous_events(path, manifest_hash):
    if not path.exists():
        return {}
    latest = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        if event.get("manifestHash") != manifest_hash or event.get("state") not in ("PENDING", "VERIFIED", "UNCERTAIN"):
            raise base.app.app.Stop("CREATE_JOURNAL_UNKNOWN_OR_OTHER_MANIFEST")
        latest[event["code"]] = event
    if any(event["state"] != "VERIFIED" for event in latest.values()):
        raise base.app.app.Stop("CREATE_PRIOR_OUTCOME_UNCERTAIN_MANUAL_RECONCILIATION_REQUIRED")
    return latest


def precheck(client, manifest, snapshot, previous):
    # Existing complete identities are hash-bound evidence; current base list and
    # targeted names/codes/email are refreshed. This is not an atomic server lock.
    client.paths = {base.query("/v1/relation", limit=1000, offset=0)}
    catalogue, complete, reason = base.complete_pages(client.get,
        lambda offset: base.query("/v1/relation", limit=1000, offset=offset), 1000, 1)
    if not complete or len(catalogue) > 500:
        raise base.app.app.Stop("CREATE_CURRENT_CATALOGUE_INCOMPLETE")
    known = {r["id"]: r for r in snapshot["relations"]}
    by_id = {r["id"]: r for r in catalogue}
    # If names/identities may have changed under existing IDs, targeted filters
    # below help detect the relevant changes; unrelated identity rereads are avoided.
    new_ids = set(by_id) - set(known)
    if len(new_ids) > 30:
        raise base.app.app.Stop("CREATE_CATALOGUE_DRIFT_REVIEW_REQUIRED")
    fresh = {}
    for identifier in new_ids:
        fresh[identifier] = client.detail("relation", identifier)
    for row in manifest["relations"]:
        payload = row["payload"]
        candidates = {identifier for identifier, item in by_id.items() if item.get("code") == payload["code"]}
        for key, value in [("code", payload["code"])] + [("name", n) for n in row["searchNames"]] + ([("email", payload["emailAddress"])] if payload.get("emailAddress") else []):
            path = base.query("/v1/relation", **{key: value, "limit": 20, "offset": 0})
            client.paths.add(path)
            found, done, why = base.complete_pages(client.get, lambda offset, p=path: p, 20, 1)
            if not done:
                raise base.app.app.Stop("CREATE_IDENTITY_QUERY_INCOMPLETE")
            candidates.update(r["id"] for r in found)
        candidates.update(new_ids)
        for identifier in candidates:
            if identifier not in fresh:
                fresh[identifier] = client.detail("relation", identifier)
        combined = dict(known)
        combined.update(fresh)
        for detail in combined.values():
            if detail["id"] not in by_id:
                continue
            identity = (detail.get("code") == payload["code"] or
                any(payload.get(k) and detail.get(k) and base.normalize(payload[k]) == base.normalize(detail[k])
                    for k in ("name", "vatNumber", "companyRegistrationNumber")))
            if not identity:
                continue
            old = previous.get(payload["code"])
            if old and old.get("id") == detail["id"] and same_payload(payload, detail):
                continue
            raise base.app.app.Stop("CREATE_EXISTING_IDENTITY_OR_CODE_REQUIRES_REVIEW")
    for row in manifest["relations"]:
        old = previous.get(row["payload"]["code"])
        if old:
            detail = client.detail("relation", old["id"])
            if old.get("payloadHash") != digest(row["payload"]) or not same_payload(row["payload"], detail):
                raise base.app.app.Stop("CREATE_PREVIOUS_READBACK_CHANGED")


def apply(api, rows, previous, journal, manifest_hash, output):
    results = []
    for row in rows:
        payload = row["payload"]
        if payload["code"] in previous:
            results.append({"code": payload["code"], "id": previous[payload["code"]]["id"], "status": "PREVIOUSLY_VERIFIED"})
            continue
        event = {"time": datetime.now(timezone.utc).isoformat(), "manifestHash": manifest_hash,
                 "code": payload["code"], "payloadHash": digest(payload), "state": "PENDING"}
        output.append(journal, event)
        try:
            identifier = api.create(payload)
            detail = api.client.detail("relation", identifier)
            if not same_payload(payload, detail):
                raise base.app.app.Stop("CREATE_READBACK_MISMATCH")
            output.append(journal, {**event, "state": "VERIFIED", "id": identifier})
            results.append({"code": payload["code"], "id": identifier, "status": "CREATED_AND_READBACK_VERIFIED"})
            output.note("Relatie aangemaakt en teruggelezen: " + payload["code"])
        except Exception:
            output.append(journal, {**event, "state": "UNCERTAIN"})
            raise base.app.app.Stop("CREATE_STOPPED_RECONCILE_JOURNAL_NO_BLIND_RETRY") from None
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = runtime_area("prebooking")
    base.app.app.set_private_acl(root, (base.app.owner_sid(),))
    manifest = read_manifest(root / "supplier-create-manifest.json", args.manifest_sha256)
    output = PrivateOutput(root)
    if not args.apply:
        path = output.save("supplier-create-dryrun", {"mode": "LOCAL_DRY_RUN_NO_API", "manifestHash": args.manifest_sha256, "relations": manifest["relations"]})
        output.note("Lokale dry-run, geen API: " + str(path))
        return
    snapshot = matching.checked(root / manifest["identitySnapshotFile"], manifest["identitySnapshotSha256"])
    if snapshot.get("allReturnedRelationNamesCovered") is not True:
        raise base.app.app.Stop("CREATE_BASE_IDENTITY_EVIDENCE_INCOMPLETE")
    journal = root / "supplier-create-journal.jsonl"
    lock = root / "supplier-create.lock"
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.manifest_sha256)
        stream.flush()
    try:
        previous = previous_events(journal, args.manifest_sha256)
        client = base.Client([], {"acceptedAmazonCentralCode": "unused"})
        # Total cap remains narrower than the shared reviewed read client.
        base.MAX_CALLS = 200
        output = PrivateOutput(root, client.secrets)
        access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
        session = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
        if not isinstance(session, dict) or not isinstance(session.get("token"), str) or not session["token"]:
            raise base.app.app.Stop("CREATE_SESSION_UNKNOWN")
        client.token = session["token"]
        client.secrets.append(client.token)
        try:
            precheck(client, manifest, snapshot, previous)
            if client.calls > 180:
                raise base.app.app.Stop("CREATE_INSUFFICIENT_BUDGET_BEFORE_WRITES")
            api = RelationAPI(client, [row["payload"] for row in manifest["relations"]])
            results = apply(api, manifest["relations"], previous, journal, args.manifest_sha256, output)
            path = output.save("supplier-create-result", {"manifestHash": args.manifest_sha256, "results": results,
                "noInvoiceBankOrArchiveWrites": True, "identityRaceCaveat": "No server transaction or idempotency guarantee; journal blocks uncertain replay"})
            output.note("PrivÃ© resultaat: " + str(path))
        finally:
            try:
                client.request("DELETE", "/v1/session")
                output.note("Tijdelijke REST-sessie ingetrokken.")
            except base.app.app.Stop:
                output.note("REST-sessiebeÃ«indiging niet bevestigd.")
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except (base.app.app.Stop, base.CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: CREATE_LOCAL_FAILURE; inspecteer privÃ©journal, niet blind herhalen.", flush=True)
