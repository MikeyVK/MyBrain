from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""Offline reconciliation from a hash-bound fresh official REST read receipt.

No credential reader, session, HTTP client or create command is invoked.
"""
import argparse
import hashlib
import json
from pathlib import Path
import book_one_invoice as book


def reconcile(item, receipt, identifier, receipt_hash, input_hash, journal, output):
    detail = receipt.get("mutation") if isinstance(receipt, dict) else None
    if not isinstance(detail, dict) or detail.get("id") != identifier:
        raise book.base.app.app.Stop("RECONCILE_RECEIPT_IDENTITY_MISMATCH")
    amounts = book.verify_readback(detail, item, identifier)
    if not journal.exists():
        raise book.base.app.app.Stop("RECONCILE_ORIGINAL_JOURNAL_REQUIRED")
    events = [json.loads(line) for line in journal.read_text(encoding="utf-8").splitlines()]
    if not events or any(e.get("inputHash") != input_hash for e in events):
        raise book.base.app.app.Stop("RECONCILE_ORIGINAL_INPUT_HASH_CHANGED")
    prior = events[-1]
    if prior.get("state") not in ("PENDING", "UNCERTAIN", "VERIFIED", "RECONCILED_VERIFIED"):
        raise book.base.app.app.Stop("RECONCILE_PRIOR_STATE_UNKNOWN")
    received = prior.get("diagnostic", {}).get("receivedMutationId")
    if received is not None and received != identifier:
        raise book.base.app.app.Stop("RECONCILE_RECEIVED_ID_CONFLICT")
    if prior.get("mutationId") is not None and prior["mutationId"] != identifier:
        raise book.base.app.app.Stop("RECONCILE_PREVIOUS_ID_CONFLICT")
    evidence = {"state": "RECONCILED_VERIFIED", "mutationId": identifier, "inputHash": input_hash,
                "payloadHash": book.payload_hash(item["payload"]), "receiptSha256": receipt_hash,
                "method": "OFFLINE_VERIFICATION_OF_FRESH_OFFICIAL_REST_READ_RECEIPT", "amounts": amounts,
                "noApiCallsOrNewPosting": True, "noPaymentSettlementOrArchiveLinkWrites": True}
    if prior.get("state") != "RECONCILED_VERIFIED":
        output.append(journal, evidence)
    return evidence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-sha256", required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--receipt-sha256", required=True)
    parser.add_argument("--mutation-id", required=True, type=int)
    args = parser.parse_args()
    root = runtime_area("prebooking")
    input_path = private_path(args.input or root / "purchase-one-input.json")
    if not input_path.is_relative_to(root.parent.resolve()) or input_path.is_symlink():
        raise book.base.app.app.Stop("RECONCILE_INPUT_PATH_SCOPE")
    receipt_path = Path(args.receipt)
    if receipt_path.name == args.receipt:
        receipt_path = root.parent / "app" / receipt_path
    receipt_path = private_path(receipt_path)
    receipt_path = receipt_path.resolve()
    admitted = ((receipt_path.parent == (root.parent / "app").resolve() and receipt_path.name.startswith("processed-invoice-"))
        or (receipt_path.parent == (root.parent / "rest").resolve() and receipt_path.name.startswith("selected-mutation-")))
    if not admitted or receipt_path.suffix != ".json" or receipt_path.is_symlink():
        raise book.base.app.app.Stop("RECONCILE_RECEIPT_PATH_SCOPE")
    item = book.load_input(input_path, args.input_sha256)
    raw = receipt_path.read_bytes()
    if len(raw) > 1024 * 1024 or hashlib.sha256(raw).hexdigest().lower() != args.receipt_sha256.lower():
        raise book.base.app.app.Stop("RECONCILE_RECEIPT_HASH_CHANGED")
    case_root = input_path.parent if args.input else root
    lock = case_root / "purchase-one.lock"
    with lock.open("x", encoding="ascii") as stream:
        stream.write("OFFLINE_RECONCILIATION")
    try:
        output = book.PrivateOutput(root)
        result = reconcile(item, json.loads(raw), args.mutation_id, args.receipt_sha256,
                           args.input_sha256, case_root / "purchase-one-journal.jsonl", output)
        output.note("Bestaande mutatie offline gereconcilieerd, geen API: " + str(output.save("purchase-one-reconciled", result)))
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except book.base.app.app.Stop as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: RECONCILE_LOCAL_FAILURE; geen nieuwe boeking uitvoeren.", flush=True)
