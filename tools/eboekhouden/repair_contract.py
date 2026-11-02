"""Content provenance and exact metadata-only change contracts."""
import copy
import re

def require(test, code):
    if not test:
        raise ValueError(code)

def valid_text(value, maximum, ascii_only=False):
    return (isinstance(value, str) and 0 < len(value) <= maximum
            and not any(ord(c) < 32 or ord(c) == 127 for c in value)
            and (not ascii_only or value.isascii()))

def without_descriptions(value):
    result = copy.deepcopy(value)
    result.pop("description", None)
    for row in result.get("rows", []):
        row.pop("description", None)
    return result

def payment_fields(value):
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            if re.search(r"betal|paid|outstanding|openstaand|saldo|settled", key, re.I):
                result[key] = copy.deepcopy(item)
            elif isinstance(item, (dict, list)):
                nested = payment_fields(item)
                if nested:
                    result[key] = nested
        return result
    if isinstance(value, list):
        return [payment_fields(item) for item in value]
    return {}

def validate_catalog(value):
    require(value.get("scope") == "OWNER_CONTENT_DESCRIPTION_AND_ARCHIVE_NAME_REPAIR_ONLY", "REPAIR_CATALOG_SCOPE")
    headers, files = value["headers"], value["files"]
    require(len({v["mutationNumber"] for v in headers}) == len(headers), "REPAIR_DUPLICATE_MUTATION")
    require(len({v["fileId"] for v in files}) == len(files), "REPAIR_DUPLICATE_FILE")
    for entry in headers:
        full, new = entry["sourceFullDescription"], entry["newHeader"]
        require(valid_text(full, 2000) and valid_text(new, 50), "REPAIR_HEADER_TEXT")
        require(new == full if len(full) <= 50 else bool(entry["shorteningReason"]), "REPAIR_SOURCE_HEADER_NOT_PRESERVED")
        require(not re.fullmatch(r"[A-Z0-9_]+ - " + re.escape(entry["invoiceNumber"]), new), "REPAIR_GENERIC_HEADER_FORBIDDEN")
        require(len(entry["sourceRowDescriptions"]) == len(entry["historicalRest"]["rows"])
                and all(valid_text(v, 100) for v in entry["sourceRowDescriptions"]), "REPAIR_SOURCE_ROWS")
    for entry in files:
        require(entry["action"] in ("KEEP", "RENAME") and valid_text(entry["oldName"], 1000), "REPAIR_FILE_ACTION")
        require(entry["newName"] == entry["oldName"] if entry["action"] == "KEEP"
                else valid_text(entry["newName"], 48, True) and entry["newName"].endswith(".pdf"), "REPAIR_ARCHIVE_NAME")
        require(set(map(str, entry["coveredMutationNumbers"])) == set(entry["historicalRests"]), "REPAIR_SHARED_SCOPE")

def validate_source_contract(item, snapshot):
    binding = item.get("sourceDescriptionContract")
    require(isinstance(binding, dict), "BOOK_SOURCE_DESCRIPTION_REQUIRED")
    rows = snapshot["ranges"]["Facturen"]["values"]
    source = [dict(zip(rows[0], row)) for row in rows[1:] if row and row[0] == item["sourceInvoiceId"]]
    require(len(source) == 1, "BOOK_SOURCE_DESCRIPTION_IDENTITY")
    require(str(source[0].get("factuurnummer")) == item["payload"]["invoiceNumber"], "BOOK_SOURCE_INVOICE_NUMBER_MISMATCH")
    full, header = source[0]["omschrijving"], item["payload"]["description"]
    require(binding.get("fullSourceDescription") == full and binding.get("header") == header, "BOOK_SOURCE_DESCRIPTION_MISMATCH")
    require(header == full if len(full) <= 50 else bool(binding.get("shorteningReason")), "BOOK_SOURCE_HEADER_NOT_PRESERVED")
    require(not re.fullmatch(r"[A-Z0-9_]+ - " + re.escape(item["payload"]["invoiceNumber"]), header), "BOOK_GENERIC_HEADER_FORBIDDEN")
    source_rows = snapshot["ranges"]["Factuurregels"]["values"]
    source_lines = [dict(zip(source_rows[0], row)) for row in source_rows[1:] if row and row[0] == item["sourceInvoiceId"]]
    expected_rows = [row["omschrijving"] for row in sorted(source_lines, key=lambda row: row["regel_nr"])]
    require(binding.get("rowDescriptions") == expected_rows == [v["description"] for v in item["payload"]["rows"]], "BOOK_SOURCE_ROWS_MISMATCH")

def build_description_payload(rest, observed, entry):
    require(rest["type"] == 1 and rest["id"] == entry["mutationNumber"]
            and rest["invoiceNumber"] == entry["invoiceNumber"], "REPAIR_MUTATION_IDENTITY")
    require(observed.get("mutatieNummer") == rest["id"] and observed.get("factuurNummer") == rest["invoiceNumber"]
            and str(observed.get("datum", ""))[:10] == rest["date"]
            and type(observed.get("id")) is int and observed["id"] > 0, "REPAIR_APP_IDENTITY")
    headers = {"soort": 1, "relatieId": rest["relationId"], "grootboekRekeningId": rest["ledgerId"],
               "isInclusiefBtw": rest["inExVat"] == "IN", "termijnInDagen": rest["termOfPayment"],
               "boekstuk": rest.get("entryNumber", ""), "omschrijving": rest["description"]}
    require(all(observed.get(k) == v for k, v in headers.items()), "REPAIR_APP_HEADER_DRIFT")
    app_rows = observed.get("mutatieRegels")
    require(isinstance(app_rows, list) and len(app_rows) == len(rest["rows"]) == len(entry["sourceRowDescriptions"]), "REPAIR_APP_ROW_COUNT")
    result_rows = []
    for index, (row, app_row, description) in enumerate(zip(rest["rows"], app_rows, entry["sourceRowDescriptions"])):
        require(row.get("costCenterId") is None, "REPAIR_NONEMPTY_COSTCENTER_WRITE_CONTRACT_UNPROVED")
        expected = {"index": index, "tegenRekeningId": row["ledgerId"], "btwCode": row["vatCode"], "bedrag": row["amount"]}
        require(all(app_row.get(k) == v for k, v in expected.items()), "REPAIR_APP_ROW_BASIS_DRIFT")
        require(app_row.get("omschrijving") in {row.get("description"), entry["oldHeader"], entry["newHeader"], description}, "REPAIR_MANUAL_APP_ROW_DESCRIPTION_CHANGE_STOP")
        result_rows.append({**expected, "omschrijving": description})
    return {"id": observed["id"], "mutatieNummer": rest["id"], "factuurNummer": rest["invoiceNumber"],
            "datum": rest["date"], "boekstuk": headers["boekstuk"], "omschrijving": entry["newHeader"],
            "soort": 1, "grootboekRekeningId": rest["ledgerId"], "relatieId": rest["relationId"],
            "isInclusiefBtw": headers["isInclusiefBtw"], "termijnInDagen": rest["termOfPayment"], "mutatieRegels": result_rows}

def verify_description(before, after, app_after, entry):
    require(without_descriptions(before) == without_descriptions(after), "REPAIR_NON_DESCRIPTION_REST_CHANGED")
    require(after["description"] == app_after.get("omschrijving") == entry["newHeader"], "REPAIR_HEADER_NOT_RESTORED")
    require(app_after.get("mutatieNummer") == before["id"], "REPAIR_AFTER_APP_IDENTITY")
    app_rows = app_after.get("mutatieRegels")
    require(isinstance(app_rows, list) and len(app_rows) == len(after["rows"]), "REPAIR_AFTER_ROW_COUNT")
    evidence = []
    for old, row, app_row, wanted in zip(before["rows"], after["rows"], app_rows, entry["sourceRowDescriptions"]):
        allowed = {old.get("description"), wanted, entry["newHeader"]}
        require(row.get("description") in allowed and app_row.get("omschrijving") in allowed, "REPAIR_UNEXPECTED_ROW_DESCRIPTION")
        evidence.append({"requestedSource": wanted, "restReturned": row.get("description"),
                         "appReturned": app_row.get("omschrijving"),
                         "independentSourceTextConfirmed": row.get("description") == app_row.get("omschrijving") == wanted})
    build_description_payload(after, app_after, entry)
    return evidence

def verify_rename(before, after, entry):
    require(after.get("id") == entry["fileId"] and after.get("naam") == entry["newName"], "REPAIR_RENAME_NOT_CONFIRMED")
    stable = lambda value: {k: v for k, v in value.items() if k not in ("naam", "datum")}
    require(stable(before) == stable(after), "REPAIR_RENAME_OTHER_METADATA_CHANGED")
