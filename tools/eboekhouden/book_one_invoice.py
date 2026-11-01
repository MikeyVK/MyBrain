from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""One manifest-authorized purchase invoice; dry-run by default."""
import argparse
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys
import preflight as base
import catalogue_match as checked
from rest_create_command import RestCreateCommand, payload_hash
from private_output import PrivateOutput


def cents(value):
    if type(value) not in (int, float, str, Decimal):
        raise base.app.app.Stop("BOOK_ONE_MONEY_INVALID")
    number = Decimal(str(value))
    if not number.is_finite() or number != number.quantize(Decimal("0.01")):
        raise base.app.app.Stop("BOOK_ONE_MONEY_NOT_EXACT_CENTS")
    return number.quantize(Decimal("0.01"))


def expected_rows(item):
    payload = item["payload"]
    values = item.get("expectedRows")
    if values is None:
        if len(payload["rows"]) != 1 or payload["inExVat"] != "IN" or payload["rows"][0]["vatCode"] != "HOOG_INK_21":
            raise base.app.app.Stop("BOOK_ONE_EXPLICIT_ROW_EXPECTATIONS_REQUIRED")
        values = [{**item["expectedMoney"], "ledgerCode": item["rowLedgerCode"]}]
    if not isinstance(values, list) or len(values) != len(payload["rows"]):
        raise base.app.app.Stop("BOOK_ONE_ROW_EXPECTATION_COUNT")
    return values


def group_vat_decision(item):
    policy = item.get("groupVatPolicy")
    if policy is None:
        return None
    payload = item["payload"]
    decision = policy.get("ownerDecision") if isinstance(policy, dict) else None
    if (not isinstance(decision, dict)
            or policy.get("mode") != "OWNER_APPROVED_LOWER_GROUP_VAT_NO_ROW_ALLOCATION"
            or policy.get("ownerDecisionSha256") != payload_hash(decision)
            or decision.get("authority") != "OWNER_DIRECT"
            or decision.get("noRowAllocation") is not True):
        raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_EXPLICIT_OWNER_DECISION_REQUIRED")
    rows = payload["rows"]
    if (payload["inExVat"] != "IN" or not rows or "expectedRows" not in item
            or any(row["vatCode"] != "HOOG_INK_21" or cents(row["amount"]) <= 0 for row in rows)
            or decision.get("vatCode") != "HOOG_INK_21"):
        raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_SCOPE_NOT_POSITIVE_IN_SINGLE_HOOG_GROUP")
    pdf_hash = item.get("provenance", {}).get("currentSourceSha256")
    if (not isinstance(pdf_hash, str) or not base.re.fullmatch(r"[a-fA-F0-9]{64}", pdf_hash)
            or decision.get("sourcePdfSha256") != pdf_hash
            or not item.get("sourceInvoiceId") or decision.get("sourceInvoiceId") != item["sourceInvoiceId"]
            or decision.get("sourceRowsHash") != payload_hash(item["expectedRows"])
            or decision.get("payloadHash") != payload_hash(payload)):
        raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_OWNER_SOURCE_BINDING_MISMATCH")
    source, booked = decision.get("sourceMoney", {}), decision.get("bookingMoney", {})
    sums = {key: sum((cents(row[key]) for row in item["expectedRows"]), Decimal("0")) for key in ("net", "vat", "gross")}
    if (set(source) != set(sums) or set(booked) != set(sums)
            or any(cents(source[key]) != sums[key] or cents(booked[key]) != cents(item["expectedMoney"][key]) for key in sums)):
        raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_SOURCE_OR_BOOKING_TOTALS_MISMATCH")
    if (cents(booked["gross"]) != cents(source["gross"])
            or cents(booked["vat"]) != cents(source["vat"]) - Decimal("0.01")
            or cents(booked["net"]) != cents(source["net"]) + Decimal("0.01")
            or cents(booked["net"]) + cents(booked["vat"]) != cents(booked["gross"])
            or cents(booked["vat"]) < 0):
        raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_NOT_EXACT_OWNER_APPROVED_LOWER_ONE_CENT")
    return decision


def validate_item(item):
    payload = item.get("payload", {})
    expected_keys = {"type", "date", "ledgerId", "invoiceNumber", "termOfPayment", "inExVat", "description", "relationId", "rows"}
    if item.get("scope") != "ONE_OWNER_AUTHORIZED_PURCHASE_INVOICE_ONLY" or set(payload) != expected_keys:
        raise base.app.app.Stop("BOOK_ONE_INPUT_SCOPE")
    if (type(payload["type"]) not in (int, str) or payload["type"] not in (1, "1") or payload["inExVat"] not in ("IN", "EX")
            or not isinstance(payload["rows"], list) or not 1 <= len(payload["rows"]) <= 4
            or type(payload["termOfPayment"]) is not int or payload["termOfPayment"] not in (0, 8, 10, 14)):
        raise base.app.app.Stop("BOOK_ONE_TYPE_MODE_ROWS_TERM_OUTSIDE_SUPPORTED_SCOPE")
    if not isinstance(payload["description"], str) or not 1 <= len(payload["description"]) <= 50:
        raise base.app.app.Stop("BOOK_ONE_HEADER_DESCRIPTION_INVALID")
    totals = {key: Decimal("0.00") for key in ("gross", "net", "vat")}
    for row, expected in zip(payload["rows"], expected_rows(item)):
        if set(row) not in ({"ledgerId", "vatCode", "amount", "description"}, {"ledgerId", "vatCode", "amount", "description", "costCenterId"}) or row["vatCode"] not in ("HOOG_INK_21", "BI_EU_INK", "GEEN"):
            raise base.app.app.Stop("BOOK_ONE_ROW_FIELDS_CHANGED")
        if not isinstance(row["description"], str) or not 1 <= len(row["description"]) <= 100:
            raise base.app.app.Stop("BOOK_ONE_ROW_DESCRIPTION_INVALID")
        if not base.app.app.positive_integer(row["ledgerId"]) or ("costCenterId" in row and not base.app.app.positive_integer(row["costCenterId"])):
            raise base.app.app.Stop("BOOK_ONE_IDENTIFIER_INVALID")
        amounts = {key: cents(expected[key]) for key in totals}
        if amounts["net"] + amounts["vat"] != amounts["gross"] or cents(row["amount"]) != amounts["gross" if payload["inExVat"] == "IN" else "net"]:
            raise base.app.app.Stop("BOOK_ONE_SOURCE_MONEY_CONFLICT")
        if row["vatCode"] in ("BI_EU_INK", "GEEN") and amounts["vat"] != 0:
            raise base.app.app.Stop("BOOK_ONE_ZERO_VAT_EXPECTATION_REQUIRED")
        if str(expected["ledgerCode"]) == "1410":
            if row["vatCode"] != "GEEN" or expected.get("treatment") != "OWNER_ACCEPTED_PRIVATE_GROSS_NO_INPUT_VAT" or not isinstance(expected.get("sourceAmounts"), dict):
                raise base.app.app.Stop("BOOK_ONE_PRIVATE_SOURCE_POLICY_REQUIRED")
            source = expected["sourceAmounts"]
            if cents(source["gross"]) != amounts["gross"] or cents(source["net"]) + cents(source["vat"]) != cents(source["gross"]):
                raise base.app.app.Stop("BOOK_ONE_PRIVATE_SOURCE_MONEY_CONFLICT")
        for key in totals:
            totals[key] += amounts[key]
    if group_vat_decision(item) is None and any(totals[key] != cents(item["expectedMoney"][key]) for key in totals):
        raise base.app.app.Stop("BOOK_ONE_SOURCE_MONEY_CONFLICT")
    base.iso_date(payload["date"])
    if any(not base.app.app.positive_integer(payload[key]) for key in ("ledgerId", "relationId")):
        raise base.app.app.Stop("BOOK_ONE_IDENTIFIER_INVALID")
    if not isinstance(payload["invoiceNumber"], str) or not 1 <= len(payload["invoiceNumber"]) <= 50:
        raise base.app.app.Stop("BOOK_ONE_INVOICE_NUMBER_INVALID")
    return item


def load_input(path, fingerprint):
    return validate_item(checked.checked(path, fingerprint))


def journal_state(path, fingerprint):
    if not path.exists():
        return None
    events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if not events or any(event.get("inputHash") != fingerprint for event in events):
        raise base.app.app.Stop("BOOK_ONE_JOURNAL_INPUT_CHANGED")
    last = events[-1]
    if last.get("state") not in ("VERIFIED", "RECONCILED_VERIFIED") or not base.app.app.positive_integer(last.get("mutationId")):
        raise base.app.app.Stop("BOOK_ONE_PREVIOUS_OUTCOME_UNCERTAIN_NO_RETRY")
    return last


def precheck(client, item, previous):
    payload = item["payload"]
    rows, complete, reason = base.complete_pages(client.get,
        lambda offset: base.mutation_query(payload["invoiceNumber"], offset), 20, 3)
    if not complete or any(r.get("invoiceNumber") != payload["invoiceNumber"] for r in rows):
        raise base.app.app.Stop("BOOK_ONE_DUPLICATE_QUERY_INCOMPLETE_OR_NOT_EXACT")
    if rows and not (previous and len(rows) == 1 and rows[0]["id"] == previous["mutationId"]):
        raise base.app.app.Stop("BOOK_ONE_EXISTING_INVOICE_NUMBER_STOP_REVIEW")
    if previous and not rows:
        raise base.app.app.Stop("BOOK_ONE_PREVIOUS_MUTATION_NOT_IN_EXACT_LOOKUP")
    relation = client.detail("relation", payload["relationId"])
    if relation.get("code") != item["relationCode"] or relation.get("inactive") is not False:
        raise base.app.app.Stop("BOOK_ONE_RELATION_ID_CODE_OR_ACTIVE_MISMATCH")
    for identifier, code, category in ((payload["ledgerId"], item["headerLedgerCode"], "CRED"),
            *[(row["ledgerId"], str(expected["ledgerCode"]), None) for row, expected in zip(payload["rows"], expected_rows(item))]):
        path = "/v1/ledger/" + str(identifier)
        client.paths.add(path)
        ledger = client.get(path)
        if not isinstance(ledger, dict) or ledger.get("id") != identifier:
            raise base.app.app.Stop("BOOK_ONE_LEDGER_IDENTITY_MISMATCH")
        if str(ledger.get("code")) != code or (category and ledger.get("category") != category) or (
                not category and ledger.get("category") not in ("BAL", "VW")):
            raise base.app.app.Stop("BOOK_ONE_LEDGER_ID_CODE_CATEGORY_MISMATCH")


def verify_readback(detail, item, identifier):
    payload = item["payload"]
    if detail.get("id") != identifier:
        raise base.app.app.Stop("BOOK_ONE_READBACK_ID_MISMATCH")
    for key in ("type", "date", "ledgerId", "invoiceNumber", "termOfPayment", "inExVat", "description", "relationId"):
        equal = detail.get(key) == payload[key]
        if key == "type":
            equal = type(detail.get(key)) is int and detail[key] == 1 and payload[key] in (1, "1")
        if not equal:
            raise base.app.app.Stop("BOOK_ONE_READBACK_HEADER_MISMATCH")
    rows = detail.get("rows")
    if not isinstance(rows, list) or len(rows) != len(payload["rows"]):
        raise base.app.app.Stop("BOOK_ONE_READBACK_ROW_COUNT")
    decision = group_vat_decision(item)
    groups, descriptions, row_vat_evidence = {}, [], []
    for row, wanted, money in zip(rows, payload["rows"], expected_rows(item)):
        if any(row.get(k) != wanted[k] for k in ("ledgerId", "vatCode")) or cents(row.get("amount")) != cents(wanted["amount"]):
            raise base.app.app.Stop("BOOK_ONE_READBACK_ROW_MISMATCH")
        if row.get("costCenterId") != wanted.get("costCenterId"):
            raise base.app.app.Stop("BOOK_ONE_READBACK_COST_CENTER_MISMATCH")
        actual_description = row.get("description")
        if actual_description not in (wanted["description"], payload["description"]):
            raise base.app.app.Stop("BOOK_ONE_READBACK_ROW_DESCRIPTION_UNKNOWN")
        descriptions.append({"requested": wanted["description"], "returned": actual_description,
            "status": "EXACT_REQUESTED_ROW" if actual_description == wanted["description"] else "EXACT_HEADER_PROJECTION_OBSERVED_NOT_VENDOR_GUARANTEE"})
        # Official GET contract: only returned when VAT is calculated per row.
        # Missing is not zero and is never represented as observed source VAT.
        if decision is not None and "vatAmount" in row:
            raise base.app.app.Stop("BOOK_ONE_GROUP_VAT_UNALLOCATED_ROW_VAT_REPRESENTATION_UNKNOWN")
        if "vatAmount" in row:
            if row["vatAmount"] is None or cents(row["vatAmount"]) != cents(money["vat"]):
                raise base.app.app.Stop("BOOK_ONE_READBACK_ROW_VAT_MISMATCH")
            row_vat_evidence.append({"rowIndex": len(row_vat_evidence), "status": "RETURNED_EXACT_MATCH",
                                     "returnedVatAmount": str(cents(row["vatAmount"]))})
        else:
            row_vat_evidence.append({"rowIndex": len(row_vat_evidence), "status": "NOT_RETURNED_BY_API",
                                     "perRowVatIndependentlyVerified": False})
        groups[wanted["vatCode"]] = groups.get(wanted["vatCode"], Decimal("0")) + cents(money["vat"])
    if decision is not None:
        groups = {decision["vatCode"]: cents(decision["bookingMoney"]["vat"])}
    vats = detail.get("vat")
    if not isinstance(vats, list) or len(vats) != len(groups) or len({v.get("vatCode") for v in vats}) != len(vats):
        raise base.app.app.Stop("BOOK_ONE_READBACK_VAT_MISMATCH")
    if any(v.get("vatCode") not in groups or cents(v.get("amount")) != groups[v["vatCode"]] for v in vats):
        raise base.app.app.Stop("BOOK_ONE_READBACK_VAT_MISMATCH")
    actual_vat = sum((cents(group["amount"]) for group in vats), Decimal("0"))
    basis = sum((cents(row["amount"]) for row in rows), Decimal("0"))
    net = basis - actual_vat if payload["inExVat"] == "IN" else basis
    gross = basis if payload["inExVat"] == "IN" else basis + actual_vat
    if any(cents(actual) != cents(item["expectedMoney"][key]) for key, actual in (("gross", gross), ("net", net), ("vat", actual_vat))):
        raise base.app.app.Stop("BOOK_ONE_READBACK_NET_MISMATCH")
    return {"gross": str(cents(gross)), "vat": str(cents(actual_vat)), "netVerifiedBySubtraction": str(cents(net)),
            "rowDescriptionEvidence": descriptions[0] if len(descriptions) == 1 else descriptions,
            "sourceAmountsKeptSeparateFromBookingTreatment": True, "rowVatEvidence": row_vat_evidence,
            "vatVerificationBasis": "EXACT_RETURNED_VAT_CODE_GROUP_TOTALS",
            "netVerificationBasis": "IN_ROWS_MINUS_RETURNED_GROUP_VAT" if payload["inExVat"] == "IN" else "EX_ROWS_BASIS",
            "sourceVsBookingGroupVat": None if decision is None else {
                "sourceMoney": decision["sourceMoney"], "bookingMoney": decision["bookingMoney"],
                "ownerDecisionSha256": item["groupVatPolicy"]["ownerDecisionSha256"],
                "differenceAllocatedToIndividualRows": False,
                "sourceValuesAreDocumentEvidenceNotApiObservedAmounts": True}}


def execute(client, command, item, journal, fingerprint, output):
    previous = journal_state(journal, fingerprint)
    precheck(client, item, previous)
    payload = item["payload"]
    if previous:
        detail = client.detail("mutation", previous["mutationId"])
        amounts = verify_readback(detail, item, previous["mutationId"])
        return {"state": "PREVIOUSLY_VERIFIED_NO_NEW_BOOKING", "mutationId": previous["mutationId"], "amounts": amounts}
    pending = {"state": "PENDING", "inputHash": fingerprint, "payloadHash": payload_hash(payload), "invoiceNumber": payload["invoiceNumber"]}
    output.append(journal, pending)
    stage, identifier = "CREATE_REQUEST", None
    try:
        identifier = command.create(payload)
        stage = "READBACK_GET"
        detail = client.detail("mutation", identifier)
        stage = "READBACK_VERIFY"
        amounts = verify_readback(detail, item, identifier)
        stage = "JOURNAL_VERIFIED"
        output.append(journal, {**pending, "state": "VERIFIED", "mutationId": identifier})
        return {"state": "CREATED_AND_READBACK_VERIFIED", "mutationId": identifier, "amounts": amounts,
                "mutation": base.rest.project(detail, identifier, client.secrets),
                "noPaymentSettlementOrArchiveLinkWrites": True, "sourceRegisterUnchanged": True,
                "archiveFileIdReferenceOnlyNotLinked": item["archiveFileId"]}
    except Exception as exc:
        cause = str(exc) if isinstance(exc, base.app.app.Stop) and base.re.fullmatch(r"[A-Z0-9_]{1,160}", str(exc)) else type(exc).__name__
        diagnostic = {"stage": stage, "cause": cause, "exceptionType": type(exc).__name__}
        if isinstance(exc, base.app.RequestFailure):
            diagnostic["safeErrorFields"] = exc.fields
        if base.app.app.positive_integer(identifier):
            diagnostic["receivedMutationId"] = identifier
        output.append(journal, {**pending, "state": "UNCERTAIN", "diagnostic": diagnostic})
        raise base.app.app.Stop("BOOK_ONE_STOPPED_RECONCILE_JOURNAL_NO_RETRY_" + stage + "_" + cause) from exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-sha256", required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = runtime_area("prebooking")
    base.app.app.set_private_acl(root, (base.app.owner_sid(),))
    input_path = private_path(args.input or root / "purchase-one-input.json")
    if not input_path.is_relative_to(root.parent.resolve()) or input_path.is_symlink():
        raise base.app.app.Stop("BOOK_ONE_INPUT_OUTSIDE_PRIVATE_ROOT")
    item = load_input(input_path, args.input_sha256)
    from booking_source_guard import admit
    try:
        admit(item, root.parent)
    except ValueError as exc:
        code = str(exc) if str(exc).startswith("BOOK_") and str(exc).replace("_", "").isalnum() else "BOOK_SOURCE_DESCRIPTION_INVALID"
        raise base.app.app.Stop(code) from exc
    output = PrivateOutput(root)
    if not args.apply:
        output.note("Lokale dry-run, geen API: " + str(output.save("purchase-one-dryrun", item)))
        return
    case_root = input_path.parent if args.input else root
    journal, lock = case_root / "purchase-one-journal.jsonl", case_root / "purchase-one.lock"
    if not base.app.app.positive_integer(item.get("archiveFileId")):
        raise base.app.app.Stop("BOOK_ONE_VERIFIED_ARCHIVE_FILE_REQUIRED")
    with lock.open("x", encoding="ascii") as stream:
        stream.write(args.input_sha256)
    try:
        journal_state(journal, args.input_sha256)
        payload = item["payload"]
        client = base.Client([{"factuurnummer": payload["invoiceNumber"], "leverancier_naam": item["relationCode"]}],
                             {"acceptedAmazonCentralCode": item["relationCode"]})
        client.paths = {base.mutation_query(payload["invoiceNumber"], offset) for offset in (0, 20, 40)}
        base.MAX_CALLS = 50
        access = base.rest.normalize_access_token(base.CredentialStore(base.WindowsBackend()).load())
        session = client.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
        if not isinstance(session, dict) or not isinstance(session.get("token"), str) or not session["token"]:
            raise base.app.app.Stop("BOOK_ONE_SESSION_UNKNOWN")
        client.token = session["token"]
        client.secrets.append(client.token)
        output = PrivateOutput(root, client.secrets)
        try:
            command = RestCreateCommand(client, "/v1/mutation", [payload])
            result = execute(client, command, item, journal, args.input_sha256, output)
            output.note("EÃƒÂ©n inkoopfactuur gecontroleerd; privÃƒÂ©resultaat: " + str(output.save("purchase-one-result", result)))
        finally:
            try:
                client.request("DELETE", "/v1/session")
                output.note("Tijdelijke REST-sessie ingetrokken.")
            except base.app.app.Stop:
                output.note("REST-sessiebeÃƒÂ«indiging niet bevestigd.")
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except (base.app.app.Stop, base.CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except Exception:
        print("Gestopt: BOOK_ONE_LOCAL_FAILURE; inspecteer privÃƒÂ©journal, niet blind herhalen.", flush=True)
