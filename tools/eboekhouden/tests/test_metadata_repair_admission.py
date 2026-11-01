import copy, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from test_metadata_repair import fixture, after_header, Reads, Command
import metadata_repair as engine
import repair_contract as c
from repair_io import RepairReads
from private_output import PrivateOutput as _PrivateOutput

def PrivateOutput(root, secrets=()):
    return _PrivateOutput(root, secrets, path_validator=Path)


class VerticalAndAdmission(unittest.TestCase):
    def test_rename_vertical_and_duplicate_write_stop(self):
        e,f,b=fixture();a=copy.deepcopy(b);a["metadata"].update(naam=f["newName"],datum="2030-02-01")
        plan={"action":"rename","target":301,"entry":f,"fileEntry":f,"before":b,
              "payload":{"id":301,"naam":f["newName"]},"catalogReference":{"sha256":"catalog"}}
        plan["payloadHash"]=engine.prep.fingerprint(plan["payload"])
        with tempfile.TemporaryDirectory() as tmp:
            journal=Path(tmp)/"attempt.jsonl";command=Command(journal)
            result=engine.execute(Reads([b,a]),command,plan,"plan",journal,PrivateOutput(tmp))
            self.assertTrue(result["filenameRestored"])
            with self.assertRaises(ValueError):engine.execute(Reads([a]),command,plan,"changedhash",journal,PrivateOutput(tmp))
            self.assertEqual(command.calls,1)

    def test_actual_reader_shape_shared_targets_and_byte_hash(self):
        e,f,b=fixture();other=copy.deepcopy(b["rests"]["101"]);other["id"]=102;other["invoiceNumber"]="INV2"
        f["coveredMutationNumbers"]=[101,102];f["historicalRests"]["102"]=other
        states={"101":copy.deepcopy(b["rests"]["101"]),"102":copy.deepcopy(other)};calls=[]
        def rest(path):
            calls.append(path);return copy.deepcopy(states[path.split("/")[-1]])
        def file(kind,identifier):
            calls.append(kind)
            return copy.deepcopy(b["metadata"]) if kind=="metadata" else {"mime":"application/pdf","bytes":b"%PDF-one"}
        reader=RepairReads(rest,lambda *args:b["appTarget"],file,
                           lambda n:[{"fileId":301,"koppelId":900+n}],lambda:calls.append("admin"),
                           lambda path:{"items":[{"mutationId":102 if "INV2" in path else 101,"invoiceNumber":"INV2" if "INV2" in path else "INV1","relationId":2,"totalAmount":121,"paidAmount":0,"outstandingAmount":121}],"count":1})
        value=reader.capture(f,e)
        self.assertEqual(set(value["rests"]),{"101","102"})
        self.assertEqual(set(value["linkedFiles"]),{"101","102"})
        self.assertEqual(calls.count("admin"),2)
        states["101"]["relationId"]=99
        with self.assertRaises(ValueError):reader.capture(f,e)

    def test_wrong_after_app_relation_and_manual_row_stop(self):
        e,f,b=fixture();a=after_header(b,e);a["appTarget"]["relatieId"]=99
        with self.assertRaises(ValueError):c.verify_description(b["rests"]["101"],a["rests"]["101"],a["appTarget"],e)
        b["appTarget"]["mutatieRegels"][0]["omschrijving"]="Unexpected manual text"
        with self.assertRaises(ValueError):c.build_description_payload(b["rests"]["101"],b["appTarget"],e)

    def test_fresh_book_cli_blocks_legacy_payload_before_credentials(self):
        import book_one_invoice as book
        with patch.object(sys,"argv",["book","--input-sha256","fake"]), \
             patch.object(book,"load_input",return_value={"sourceInvoiceId":"F1","payload":{}}), \
             patch.object(book.base.app.app,"set_private_acl"),patch.object(book.base.app,"owner_sid",return_value="synthetic"), \
             patch.object(book.base,"CredentialStore") as vault:
            with self.assertRaisesRegex(Exception,"BOOK_SOURCE_DESCRIPTION_REQUIRED"):book.main()
            vault.assert_not_called()

    def test_metadata_cli_prior_attempt_blocks_before_credentials(self):
        e,f,b=fixture();catalog={"headers":[e],"files":[f]};entry,file_entry=engine.select(catalog,"header",101)
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cat=root/"catalog.json";cat.write_text("{}")
            case=root/"cases/header-101";case.mkdir(parents=True);(case/"attempt.jsonl").write_text('{"state":"UNCERTAIN"}\n')
            reference={"path":"catalog.json","sha256":"hash"}
            plan={"scope":"ONE_METADATA_REPAIR_ONLY","action":"header","target":101,"entry":entry,
                  "fileEntry":file_entry,"catalogReference":reference}
            with patch.object(engine,"ROOT",root),patch.object(engine,"HOME",root), \
                 patch.object(engine,"load_catalog",return_value=catalog), \
                 patch.object(engine.prep,"checked",return_value=plan),patch.object(engine.prep.base,"CredentialStore") as vault:
                with self.assertRaisesRegex(ValueError,"REPAIR_PRIOR_ATTEMPT_NO_RETRY"):
                    engine.main(["header","--target","101","--catalog",str(cat),"--catalog-sha256","hash",
                                 "--apply","--plan",str(root/"plan.json"),"--plan-sha256","phash"])
                vault.assert_not_called()

    def test_secret_redaction_in_uncertain_journal(self):
        e,f,b=fixture();a=after_header(b,e);a["rests"]["101"]["rows"][0]["amount"]=122
        plan={"action":"header","target":101,"entry":e,"fileEntry":f,"before":b,
              "payload":engine.payload_for("header",b,e),"catalogReference":{"sha256":"catalog"}}
        plan["payloadHash"]=engine.prep.fingerprint(plan["payload"])
        class Bad(Command):
            def send(self,payload):
                self.calls+=1;raise ValueError("SYNTHETIC_SECRET")
        with tempfile.TemporaryDirectory() as tmp:
            journal=Path(tmp)/"attempt.jsonl";command=Bad(journal)
            with self.assertRaises(ValueError):
                engine.execute(Reads([b,a]),command,plan,"plan",journal,PrivateOutput(tmp,("SYNTHETIC_SECRET",)))
            self.assertNotIn("SYNTHETIC_SECRET",journal.read_text())


class PaymentAndAck(unittest.TestCase):
    def test_outstanding_identity_empty_multi_filter_and_amounts_stop(self):
        from repair_io import RepairReads
        e,f,b=fixture()
        valid={"mutationId":101,"invoiceNumber":"INV1","relationId":2,"totalAmount":121,"paidAmount":0,"outstandingAmount":121}
        good={"items":[valid],"count":1}
        reader=RepairReads(None,None,None,None,None,lambda path:good)
        self.assertEqual(reader.payment_status(b["rests"]["101"]),valid)
        bads=[{"items":[],"count":0},{"items":[valid,valid],"count":2},
              {"items":[dict(valid,invoiceNumber="OTHER")],"count":1},
              {"items":[dict(valid,mutationId=102)],"count":1},
              {"items":[dict(valid,relationId=3)],"count":1},
              {"items":[dict(valid,paidAmount=None)],"count":1}]
        for value in bads:
            reader=RepairReads(None,None,None,None,None,lambda path:value)
            with self.assertRaises(ValueError):reader.payment_status(b["rests"]["101"])

    def test_unrecognized_ack_read_reconciles_or_remains_uncertain_no_retry(self):
        e,f,b=fixture()
        for achieved in (True,False):
            a=after_header(b,e) if achieved else copy.deepcopy(b)
            plan={"action":"header","target":101,"entry":e,"fileEntry":f,"before":b,
                  "payload":engine.payload_for("header",b,e),"catalogReference":{"sha256":"catalog"}}
            plan["payloadHash"]=engine.prep.fingerprint(plan["payload"])
            class Unknown(Command):
                def send(self,payload):
                    assert json.loads(self.journal.read_text().splitlines()[-1])["state"]=="PENDING"
                    self.calls+=1;return {"unexpected":True}
            with tempfile.TemporaryDirectory() as tmp:
                journal=Path(tmp)/"attempt.jsonl";command=Unknown(journal)
                if achieved:
                    result=engine.execute(Reads([b,a]),command,plan,"hash",journal,PrivateOutput(tmp))
                    self.assertEqual(result["state"],"RECONCILED_VERIFIED_AFTER_UNKNOWN_RESPONSE")
                    self.assertFalse(result["acknowledgement"]["identityShapeUnderstood"])
                else:
                    with self.assertRaises(ValueError):engine.execute(Reads([b,a]),command,plan,"hash",journal,PrivateOutput(tmp))
                    last=json.loads(journal.read_text().splitlines()[-1])
                    self.assertEqual(last["state"],"UNCERTAIN")
                    self.assertIn("afterEvidence",last)
                    self.assertIn("acknowledgement",last)
                self.assertEqual(command.calls,1)

    def test_source_guard_hash_binding_and_valid_input(self):
        from booking_source_guard import admit
        snapshot={"ranges":{"Facturen":{"values":[["factuur_id","omschrijving","factuurnummer"],["F1","Useful product","INV1"]]},
                            "Factuurregels":{"values":[["factuur_id","regel_nr","omschrijving"],["F1",1,"Row source"]]}}}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/"source.json";source.write_text(json.dumps(snapshot))
            item={"sourceInvoiceId":"F1","payload":{"description":"Useful product","invoiceNumber":"INV1","rows":[{"description":"Row source"}]},
                  "sourceDescriptionContract":{"fullSourceDescription":"Useful product","header":"Useful product","rowDescriptions":["Row source"],
                    "sourceSnapshot":{"path":"source.json","sha256":engine.digest(source)}}}
            admit(item,root)
            source.write_text("{}")
            with self.assertRaises(ValueError):admit(item,root)

    def test_fresh_payment_status_drift_stops(self):
        e,f,b=fixture()
        before={"paidAmount":0,"outstandingAmount":121}
        captured={"rests":b["rests"],"paymentFields":{"outstandingInvoices":{"101":before}}}
        reader=RepairReads(lambda path:b["rests"]["101"],None,None,None,None,
                          lambda path:{"items":[{"mutationId":101,"invoiceNumber":"INV1","relationId":2,
                                                "totalAmount":121,"paidAmount":1,"outstandingAmount":120}],"count":1})
        with self.assertRaises(ValueError):reader.optimistic(captured)


class ObservationAndRenameAbsence(unittest.TestCase):
    def reader(self, outstanding, observe=None):
        e,f,b=fixture()
        rest=copy.deepcopy(b["rests"]["101"])
        metadata=copy.deepcopy(b["metadata"])
        reader=RepairReads(lambda path:copy.deepcopy(rest),lambda *args:copy.deepcopy(b["appTarget"]),
            lambda kind,n:copy.deepcopy(metadata) if kind=="metadata" else {"mime":"application/pdf","bytes":b"%PDF-one"},
            lambda n:copy.deepcopy(b["linkedFiles"]["101"]),lambda:None,
            lambda path:copy.deepcopy(outstanding),observe)
        return e,f,b,rest,metadata,reader

    def test_rename_empty_is_explicit_unknown_without_invented_amounts(self):
        e,f,b,rest,meta,reader=self.reader({"items":[],"count":0})
        captured=reader.capture(f)
        marker=captured["paymentFields"]["outstandingInvoices"]["101"]
        self.assertEqual(marker,{"observation":"NOT_RETURNED_BY_API","mutationId":101,"relationId":2,"invoiceNumber":"INV1"})
        self.assertFalse(captured["outstandingPresenceRequired"])
        self.assertNotIn("paidAmount",marker)
        self.assertNotIn("outstandingAmount",marker)
        reader.optimistic(captured)
        with self.assertRaisesRegex(ValueError,"REPAIR_OUTSTANDING_SCOPE_UNKNOWN"):
            reader.capture(f,e)

    def test_rename_unknown_multiple_mismatch_and_error_still_stop(self):
        valid={"mutationId":101,"invoiceNumber":"INV1","relationId":2,"totalAmount":121,"paidAmount":0,"outstandingAmount":121}
        for result in ({"items":[]}, {"items":[],"count":True}, {"items":[],"count":1},
                       {"items":[valid,valid],"count":2},
                       {"items":[dict(valid,mutationId=102)],"count":1},
                       {"items":[dict(valid,relationId=9)],"count":1},
                       {"items":[dict(valid,invoiceNumber="OTHER")],"count":1}):
            with self.subTest(result=result):
                e,f,b,rest,meta,reader=self.reader(result)
                with self.assertRaises(ValueError):reader.capture(f)
        e,f,b,rest,meta,reader=self.reader({"items":[],"count":0})
        def failing(path):raise RuntimeError("SYNTHETIC_READ_ERROR")
        reader.outstanding_get=failing
        with self.assertRaisesRegex(RuntimeError,"SYNTHETIC_READ_ERROR"):reader.capture(f)

    def test_raw_rest_saved_before_identity_or_historical_assert_redacted(self):
        for identity_error in (True,False):
            with tempfile.TemporaryDirectory() as tmp:
                output=PrivateOutput(tmp,("SYNTHETIC_SECRET",))
                observe=lambda kind,value:output.save("observed-"+kind,value)
                e,f,b,rest,meta,reader=self.reader({"items":[],"count":0},observe)
                rest["note"]="SYNTHETIC_SECRET"
                if identity_error:rest["id"]=999
                else:rest["rows"][0]["amount"]+=1
                with self.assertRaises(ValueError):reader.capture(f)
                receipts=list(Path(tmp).glob("observed-rest-*.json"))
                self.assertEqual(len(receipts),1)
                saved=json.loads(receipts[0].read_text(encoding="utf-8"))
                self.assertEqual(saved["response"]["id"],999 if identity_error else 101)
                self.assertNotIn("SYNTHETIC_SECRET",receipts[0].read_text(encoding="utf-8"))
                self.assertIn("rawObservations",reader.last_observation)

    def test_raw_outstanding_saved_before_shape_assert(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=PrivateOutput(tmp)
            e,f,b,rest,meta,reader=self.reader({"items":"unexpected","count":9},
                lambda kind,value:output.save("observed-"+kind,value))
            with self.assertRaises(ValueError):reader.capture(f)
            receipt=next(Path(tmp).glob("observed-outstanding-*.json"))
            self.assertEqual(json.loads(receipt.read_text())["response"]["items"],"unexpected")

    def test_app_detail_saved_before_existing_identity_assert_auth_not_logged(self):
        from repair_io import ObservedAppReadTransport, core
        observations=[]
        detail={"id":999,"mutatieNummer":101,"datum":"2030-01-01"}
        class Transport:
            def request(self,method,path,*args,**kwargs):
                if path=="/api/v4/mutaties/filter":
                    return {"currentPage":1,"pageSize":20,"hasMoreRows":False,
                            "items":[{"id":201,"mutatieNummer":101,"datum":"2030-01-01"}]}
                if path=="/api/v4/auth/userinfo":return {"credential":"MUST_NOT_LOG"}
                return detail
        transport=ObservedAppReadTransport(Transport(),lambda kind,value:observations.append((kind,copy.deepcopy(value))))
        with patch.object(core.app,"active_administration",return_value=(1,"synthetic")):
            with self.assertRaises(Exception):
                core.read_filtered_one(transport,core.app.SessionReader(transport,"SECRET"),"SECRET",101,"2030-01-01",(1,"synthetic"))
        self.assertEqual(len(observations),1)
        self.assertEqual(observations[0][1]["response"],detail)
        self.assertNotIn("MUST_NOT_LOG",json.dumps(observations))
        self.assertNotIn("SECRET",json.dumps(observations))

    def test_rename_empty_vertical_one_put_and_full_rest_preserved(self):
        e,f,b,rest,meta,reader=self.reader({"items":[],"count":0})
        before=reader.capture(f)
        plan={"action":"rename","target":301,"entry":f,"fileEntry":f,"before":before,
              "payload":{"id":301,"naam":f["newName"]},"catalogReference":{"sha256":"catalog"}}
        plan["payloadHash"]=engine.prep.fingerprint(plan["payload"])
        class Rename(Command):
            def send(self,payload):
                self.calls+=1
                self.assert_pending=json.loads(self.journal.read_text().splitlines()[-1])["state"]=="PENDING"
                meta["naam"]=payload["naam"]
                return {"id":301,"naam":payload["naam"]}
        with tempfile.TemporaryDirectory() as tmp:
            journal=Path(tmp)/"attempt.jsonl";command=Rename(journal)
            value=engine.execute(reader,command,plan,"hash",journal,PrivateOutput(tmp))
            self.assertEqual(value["state"],"VERIFIED")
            self.assertEqual(command.calls,1)
            self.assertTrue(command.assert_pending)
            with self.assertRaisesRegex(ValueError,"REPAIR_PRIOR_ATTEMPT_NO_RETRY"):
                engine.execute(reader,command,plan,"other",journal,PrivateOutput(tmp))

    def test_rename_empty_still_rejects_any_full_rest_change_and_presence_drift(self):
        e,f,b,rest,meta,reader=self.reader({"items":[],"count":0})
        rest["extraProtectedField"]="before"
        before=reader.capture(f)
        plan={"action":"rename","target":301,"entry":f,"fileEntry":f,"before":before,
              "payload":{"id":301,"naam":f["newName"]},"catalogReference":{"sha256":"catalog"}}
        plan["payloadHash"]=engine.prep.fingerprint(plan["payload"])
        class Rename(Command):
            def send(self,payload):
                self.calls+=1;meta["naam"]=payload["naam"];rest["extraProtectedField"]="after"
                return {"id":301,"naam":payload["naam"]}
        with tempfile.TemporaryDirectory() as tmp:
            journal=Path(tmp)/"attempt.jsonl";command=Rename(journal)
            with self.assertRaisesRegex(ValueError,"REPAIR_RENAME_CHANGED_BOOKKEEPING"):
                engine.execute(reader,command,plan,"hash",journal,PrivateOutput(tmp))
            self.assertEqual(json.loads(journal.read_text().splitlines()[-1])["state"],"UNCERTAIN")
            self.assertEqual(command.calls,1)
        e,f,b,rest,meta,reader=self.reader({"items":[],"count":0})
        before=reader.capture(f)
        reader.outstanding_get=lambda path:{"items":[{"mutationId":101,"invoiceNumber":"INV1","relationId":2,
            "totalAmount":121,"paidAmount":0,"outstandingAmount":121}],"count":1}
        with self.assertRaisesRegex(ValueError,"REPAIR_FRESH_PAYMENT_STATUS_CHANGED"):
            reader.optimistic(before)

    def test_whitespace_header_stops_before_credentials_and_read_or_put(self):
        for number in ("INV 1","INV\t1","INV\u00a01"):
            e,f,b=fixture();e["invoiceNumber"]=number
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp);cat=root/"catalog.json";cat.write_text("{}")
                with patch.object(engine,"ROOT",root),patch.object(engine,"HOME",root), \
                     patch.object(engine,"load_catalog",return_value={"headers":[e],"files":[f]}), \
                     patch.object(engine.prep.base,"CredentialStore") as vault:
                    with self.assertRaisesRegex(ValueError,"REPAIR_HEADER_INVOICE_WHITESPACE_WRITE_UNPROVED"):
                        engine.main(["header","--target","101","--catalog",str(cat),"--catalog-sha256","hash",
                                     "--apply","--plan",str(root/"plan.json"),"--plan-sha256","phash"])
                    vault.assert_not_called()
                command=Command(root/"journal");reads=Reads([b])
                with self.assertRaisesRegex(ValueError,"REPAIR_HEADER_INVOICE_WHITESPACE_WRITE_UNPROVED"):
                    engine.execute(reads,command,{"action":"header","entry":e,"fileEntry":f},"hash",root/"journal",PrivateOutput(root))
                self.assertEqual(command.calls,0);self.assertEqual(reads.calls,0)
