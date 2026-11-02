"""Offline synthetic contract/once-only/retention tests; no credential or API calls."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import metadata_repair as engine
import repair_contract as c
from repair_io import RepairReads, same_file_retention
from private_output import PrivateOutput as _PrivateOutput

def PrivateOutput(root, secrets=()):
    return _PrivateOutput(root, secrets, path_validator=Path)

import change_ledger

def fixture(rows=1, mode="IN", amount=121.0, vat=21.0):
    old, new = "CODE - INV1", "Useful source product"
    rest = {"id": 101, "type": 1, "date": "2030-01-01", "description": old, "relationId": 2,
            "ledgerId": 1700, "inExVat": mode, "termOfPayment": 14, "invoiceNumber": "INV1", "entryNumber": "",
            "rows": [{"ledgerId": 3 + i, "vatCode": "HOOG_INK_21", "amount": amount, "description": old}
                     for i in range(rows)], "vat": [{"vatCode": "HOOG_INK_21", "amount": vat}],
            "paymentStatus": {"paid": 0, "open": 121}}
    app = {"id": 201, "mutatieNummer": 101, "factuurNummer": "INV1", "datum": rest["date"],
           "soort": 1, "relatieId": 2, "grootboekRekeningId": 1700, "isInclusiefBtw": mode == "IN",
           "termijnInDagen": 14, "boekstuk": "", "omschrijving": old, "bedrag": 0,
           "mutatieRegels": [{"index": i, "tegenRekeningId": 3 + i, "btwCode": "HOOG_INK_21",
                             "bedrag": amount, "btw": 0, "omschrijving": old} for i in range(rows)]}
    entry = {"mutationNumber": 101, "invoiceNumber": "INV1", "oldHeader": old, "newHeader": new,
             "sourceFullDescription": new, "sourceRowDescriptions": ["Source row " + str(i) for i in range(rows)],
             "historicalRest": rest, "shorteningReason": None, "fileId": 301}
    file = {"fileId": 301, "oldName": "old.pdf", "newName": "260101_Product.pdf", "action": "RENAME",
            "directoryId": 0, "size": 8, "sourceSha256": hashlib.sha256(b"%PDF-one").hexdigest(),
            "coveredMutationNumbers": [101], "historicalRests": {"101": rest}}
    before = {"rests": {"101": rest}, "appTarget": app, "metadata": {"id": 301, "naam": "old.pdf",
              "directoryId": 0, "datum": "2030-01-01", "scanStatus": 3},
              "linkedFiles": {"101": [{"fileId": 301, "koppelId": 999}]},
              "pdf": {"sha256": file["sourceSha256"], "size": 8, "verified": True},
              "paymentFields": {"paid": 0, "open": 121}}
    return entry, file, before

def after_header(before, entry, independent=False):
    after = copy.deepcopy(before)
    after["rests"]["101"]["description"] = entry["newHeader"]
    after["appTarget"]["omschrijving"] = entry["newHeader"]
    after["appTarget"]["id"] = 202
    for i, (row, app) in enumerate(zip(after["rests"]["101"]["rows"], after["appTarget"]["mutatieRegels"])):
        text = entry["sourceRowDescriptions"][i] if independent else entry["newHeader"]
        row["description"] = app["omschrijving"] = text
    return after

class Reads:
    def __init__(self, states):
        self.states = states
        self.calls = 0
    def capture(self, *args):
        value = self.states[min(self.calls, len(self.states) - 1)]
        self.calls += 1
        return copy.deepcopy(value)
    def optimistic(self, value):
        pass

class Command:
    def __init__(self, journal, error=False):
        self.journal, self.error, self.calls = journal, error, 0
    def send(self, payload):
        assert json.loads(self.journal.read_text().splitlines()[-1])["state"] == "PENDING"
        self.calls += 1
        if self.error:
            raise ValueError("SYNTHETIC_UNCERTAIN")
        return {"id": 202}

class Contracts(unittest.TestCase):
    def test_all_current_money_variants_keep_basis_and_drop_computed_zeroes(self):
        for count, mode, amount, vat in [(1, "IN", 121, 21), (2, "IN", -121.00, -21.00),
                                         (1, "EX", 12.10, 0), (4, "IN", 72.6, 12.60)]:
            with self.subTest(count=count, mode=mode, amount=amount):
                e, f, b = fixture(count, mode, amount, vat)
                body = c.build_description_payload(b["rests"]["101"], b["appTarget"], e)
                self.assertNotIn("bedrag", body)
                self.assertTrue(all("btw" not in row for row in body["mutatieRegels"]))
                self.assertEqual([v["bedrag"] for v in body["mutatieRegels"]], [amount] * count)
                self.assertEqual(body["relatieId"], 2)
                self.assertEqual(body["isInclusiefBtw"], mode == "IN")

    def test_mixed_private_basis_preserved(self):
        e, f, b = fixture(2)
        b["rests"]["101"]["rows"][0].update(ledgerId=1410, vatCode="GEEN", amount=6.05)
        b["appTarget"]["mutatieRegels"][0].update(tegenRekeningId=1410, btwCode="GEEN", bedrag=6.05)
        v = c.build_description_payload(b["rests"]["101"], b["appTarget"], e)
        self.assertEqual((v["mutatieRegels"][0]["tegenRekeningId"], v["mutatieRegels"][0]["bedrag"]), (1410, 6.05))

    def test_wrong_app_identity_basis_and_costcenter_stop(self):
        for mutate in [lambda b: b["appTarget"].update(mutatieNummer=102),
                       lambda b: b["appTarget"]["mutatieRegels"][0].update(bedrag=0),
                       lambda b: b["rests"]["101"]["rows"][0].update(costCenterId=7)]:
            e, f, b = fixture()
            mutate(b)
            with self.assertRaises(ValueError):
                c.build_description_payload(b["rests"]["101"], b["appTarget"], e)

    def test_header_projection_reported_without_independent_row_claim(self):
        e, f, b = fixture(2)
        after = after_header(b, e)
        v = c.verify_description(b["rests"]["101"], after["rests"]["101"], after["appTarget"], e)
        self.assertFalse(any(z["independentSourceTextConfirmed"] for z in v))
        after = after_header(b, e, True)
        self.assertTrue(all(z["independentSourceTextConfirmed"] for z in c.verify_description(
            b["rests"]["101"], after["rests"]["101"], after["appTarget"], e)))

    def test_every_non_description_field_stays_exact(self):
        e, f, b = fixture()
        for key, value in [("termOfPayment", 0), ("relationId", 9), ("ledgerId", 8),
                           ("date", "2030-02-01"), ("paymentStatus", {"paid": 1})]:
            a = after_header(b, e);a["rests"]["101"][key] = value
            with self.assertRaises(ValueError):
                c.verify_description(b["rests"]["101"], a["rests"]["101"], a["appTarget"], e)
        for key, value in [("amount", 121.01), ("vatCode", "GEEN"), ("ledgerId", 8), ("costCenterId", 6)]:
            a = after_header(b, e);a["rests"]["101"]["rows"][0][key] = value
            with self.assertRaises(ValueError):
                c.verify_description(b["rests"]["101"], a["rests"]["101"], a["appTarget"], e)
        a = after_header(b, e);a["rests"]["101"]["vat"][0]["amount"] = 20.99
        with self.assertRaises(ValueError):
            c.verify_description(b["rests"]["101"], a["rests"]["101"], a["appTarget"], e)

    def test_rename_only_name_and_timestamp_may_change(self):
        e, f, b = fixture()
        a = dict(b["metadata"], naam=f["newName"], datum="2030-02-01")
        c.verify_rename(b["metadata"], a, f)
        for field, value in [("id", 302), ("directoryId", 4), ("scanStatus", 7)]:
            bad = dict(a);bad[field] = value
            with self.assertRaises(ValueError):
                c.verify_rename(b["metadata"], bad, f)

    def test_utf8_exact_header_and_legacy_keep_names(self):
        e, f, b = fixture();e["newHeader"] = e["sourceFullDescription"] = "Privé – materiaal"
        f["action"] = "KEEP";f["oldName"] = f["newName"] = "Een bestaande lange privé-bestandsnaam " * 3 + ".pdf"
        c.validate_catalog({"scope": "OWNER_CONTENT_DESCRIPTION_AND_ARCHIVE_NAME_REPAIR_ONLY", "headers": [e], "files": [f]})
        for name in ["x" * 45 + ".pdf", "privé.pdf"]:
            f["action"] = "RENAME";f["newName"] = name
            with self.assertRaises(ValueError):
                c.validate_catalog({"scope": "OWNER_CONTENT_DESCRIPTION_AND_ARCHIVE_NAME_REPAIR_ONLY", "headers": [e], "files": [f]})

    def test_source_header_cannot_be_replaced_by_code_number(self):
        e, f, b = fixture();e["newHeader"] = "CODE - INV1"
        with self.assertRaises(ValueError):
            c.validate_catalog({"scope": "OWNER_CONTENT_DESCRIPTION_AND_ARCHIVE_NAME_REPAIR_ONLY", "headers": [e], "files": [f]})

    def test_shared_retention_and_payment_fields(self):
        e, f, b = fixture()
        b["linkedFiles"]["102"] = [{"fileId": 301}]
        for field in ["linkedFiles", "pdf", "paymentFields"]:
            a = copy.deepcopy(b);a[field] = {}
            with self.assertRaises(ValueError):
                same_file_retention(b, a)

    def test_existing_command_only_fixed_endpoints_once(self):
        e, f, b = fixture();payload={"id": 301, "naam": "new.pdf"}
        command = change_ledger.AppMutationCommand(payload, endpoint="/api/v4/bestanden")
        self.assertTrue(command.allowed("PUT", "/api/v4/bestanden", payload))
        self.assertFalse(command.allowed("POST", "/api/v4/bestanden/upload", payload))
        command.transport = type("Fake", (), {"request": lambda *a, **k: {"id": 301}})()
        command.send(payload, "synthetic")
        with self.assertRaises(Exception):command.send(payload, "synthetic")
        with self.assertRaises(Exception):change_ledger.AppMutationCommand(payload, endpoint="/evil")

class Lifecycle(unittest.TestCase):
    def run_case(self, error=False, mismatch=False):
        e, f, b = fixture(2);after = after_header(b, e)
        if mismatch:after["rests"]["101"]["rows"][0]["amount"] += .01
        plan = {"action": "header", "target": 101, "entry": e, "fileEntry": f, "before": b,
                "payload": engine.payload_for("header", b, e), "catalogReference": {"sha256": "catalog"}}
        plan["payloadHash"] = engine.prep.fingerprint(plan["payload"])
        with tempfile.TemporaryDirectory() as tmp:
            journal = Path(tmp)/"attempt.jsonl";command=Command(journal,error)
            reader=Reads([b,after]);output=PrivateOutput(tmp)
            if mismatch:
                with self.assertRaises(ValueError):engine.execute(reader,command,plan,"plan",journal,output)
                self.assertEqual(json.loads(journal.read_text().splitlines()[-1])["state"],"UNCERTAIN")
                with self.assertRaises(ValueError):engine.execute(reader,command,plan,"plan",journal,output)
            else:
                result=engine.execute(reader,command,plan,"plan",journal,output)
                self.assertEqual(result["state"],"RECONCILED_VERIFIED_AFTER_UNKNOWN_RESPONSE" if error else "VERIFIED")
            self.assertEqual(command.calls,1)

    def test_pending_before_exactly_one_put(self):self.run_case()
    def test_unknown_response_can_only_be_read_reconciled(self):self.run_case(True)
    def test_after_money_drift_uncertain_and_no_retry(self):self.run_case(False,True)
    def test_prepared_baseline_drift_before_command(self):
        e,f,b=fixture();plan={"action":"header","entry":e,"fileEntry":f,"before":b}
        changed=copy.deepcopy(b);changed["rests"]["101"]["termOfPayment"]=0
        with tempfile.TemporaryDirectory() as tmp:
            command=Command(Path(tmp)/"journal")
            with self.assertRaises(ValueError):engine.execute(Reads([changed]),command,plan,"hash",Path(tmp)/"journal",PrivateOutput(tmp))
            self.assertEqual(command.calls,0)

    def test_already_desired_is_zero_put(self):
        e,f,b=fixture();b=after_header(b,e);payload=engine.payload_for("header",b,e)
        plan={"action":"header","target":101,"entry":e,"fileEntry":f,"before":b,"payload":payload,
              "payloadHash":engine.prep.fingerprint(payload),"catalogReference":{"sha256":"catalog"}}
        with tempfile.TemporaryDirectory() as tmp:
            journal=Path(tmp)/"journal";command=Command(journal)
            self.assertEqual(engine.execute(Reads([b]),command,plan,"hash",journal,PrivateOutput(tmp))["putAttemptCount"],0)

class SourceRegression(unittest.TestCase):
    def test_source_binding_checks_header_rows_and_utf8(self):
        snapshot={"ranges":{"Facturen":{"values":[["factuur_id","omschrijving","factuurnummer"],["F1","Privé – materiaal","INV1"]]},
                            "Factuurregels":{"values":[["factuur_id","regel_nr","omschrijving"],["F1",1,"Bronregel"]]}}}
        item={"sourceInvoiceId":"F1","payload":{"description":"Privé – materiaal","invoiceNumber":"INV1","rows":[{"description":"Bronregel"}]},
              "sourceDescriptionContract":{"fullSourceDescription":"Privé – materiaal","header":"Privé – materiaal","rowDescriptions":["Bronregel"]}}
        c.validate_source_contract(item,snapshot)
        for key,value in [("description","CODE - INV1")]:
            bad=copy.deepcopy(item);bad["payload"][key]=value
            with self.assertRaises(ValueError):c.validate_source_contract(bad,snapshot)
        bad=copy.deepcopy(item);bad.pop("sourceDescriptionContract")
        with self.assertRaises(ValueError):c.validate_source_contract(bad,snapshot)
        bad=copy.deepcopy(item);bad["payload"]["rows"][0]["description"]="Other";bad["sourceDescriptionContract"]["rowDescriptions"]=["Other"]
        with self.assertRaises(ValueError):c.validate_source_contract(bad,snapshot)

if __name__ == "__main__":
    unittest.main()
