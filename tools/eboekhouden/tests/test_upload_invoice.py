from types import SimpleNamespace
from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import base64
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import upload_invoice as p


def item():
    raw = b"%PDF-synthetic"
    return {"uploadFileName": "Synthetic INVOICE-1.pdf", "sourceInvoiceNumber": "INVOICE-1", "invoiceDate": "2030-08-16",
            "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}, raw


class FakeAPI:
    def __init__(self, journal): self.journal = journal; self.uploads = 0
    def login(self, login, admin): pass
    def listing(self, directory=None):
        return {"id": 0, "isMailEnHerkenInbox": True, "directories": [], "files": []}
    def require_same_admin(self): pass
    def upload(self, value, raw):
        assert json.loads(self.journal.read_text().splitlines()[-1])["state"] == "PENDING"
        self.uploads += 1
        return 7
    def verify(self, identifier, value): return {"id": identifier, "naam": value["uploadFileName"], "directoryId": 0}


class Checks(unittest.TestCase):
    def test_success_pending_then_hash_verified_and_no_second_upload(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/'journal';api=FakeAPI(journal);value,raw=item();out=synthetic_output(root)
            result=p.execute(api,None,1,value,raw,out,journal,'hash')
            self.assertTrue(result['downloadSha256Matches'])
            p.execute(api,None,1,value,raw,out,journal,'hash')
            self.assertEqual(api.uploads,1)
            self.assertEqual([json.loads(x)['state'] for x in journal.read_text().splitlines()],['PENDING','VERIFIED'])

    def test_duplicate_invoice_reference_stops_before_journal_or_upload(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/'journal';api=FakeAPI(journal);value,raw=item()
            api.listing=lambda directory=None:{'id':0,'isMailEnHerkenInbox':True,'directories':[],
                'files':[{'id':9,'naam':'Other INVOICE-1 original.pdf'}]}
            with self.assertRaisesRegex(p.core.app.Stop,'EXISTING_FILENAME'):
                p.execute(api,None,1,value,raw,synthetic_output(root),journal,'hash')
            self.assertFalse(journal.exists());self.assertEqual(api.uploads,0)

    def test_wrong_admin_stops_before_read_or_upload(self):
        with tempfile.TemporaryDirectory() as d:
            api=FakeAPI(Path(d)/'journal');value,raw=item()
            def stop(*args):raise p.core.app.Stop('UPLOAD_ADMINISTRATION_MISMATCH')
            api.login=stop
            with self.assertRaisesRegex(p.core.app.Stop,'ADMINISTRATION_MISMATCH'):
                p.execute(api,None,1,value,raw,synthetic_output(d),api.journal,'hash')
            self.assertEqual(api.uploads,0)

    def test_lost_response_blocks_future_login_and_replay(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);api=FakeAPI(root/'journal');value,raw=item()
            def lost(*args):raise TimeoutError()
            api.upload=lost
            with self.assertRaisesRegex(p.core.app.Stop,'NO_RETRY'):
                p.execute(api,None,1,value,raw,synthetic_output(root),api.journal,'hash')
            api.login=lambda *args:self.fail('No login after uncertain attempt')
            with self.assertRaisesRegex(p.core.app.Stop,'PREVIOUS_OUTCOME_UNCERTAIN'):
                p.execute(api,None,1,value,raw,synthetic_output(root),api.journal,'hash')

    def test_download_wrong_hash_rejected(self):
        value,raw=item();api=p.UploadAPI();api.token='synthetic'
        class Reader:
            def __init__(self,*args,**kwargs):pass
            def request(self,method,path,**kwargs):
                if '/bestand/' in path:return {'id':7,'naam':value['uploadFileName'],'directoryId':0}
                return {'mime':'application/pdf','bytes':b'%PDF-wrong'}
        with patch.object(p.files,'Transport',Reader):
            with self.assertRaisesRegex(p.core.app.Stop,'DOWNLOAD_HASH_MISMATCH'):api.verify(7,value)

    def test_exact_upload_route_json_base64_scanfalse_one_attempt(self):
        value,raw=item();sent=[]
        response={'saved':True,'scanned':False,'originalFileName':value['uploadFileName'],
                  'file':{'id':7,'naam':value['uploadFileName'],'directoryId':0}}
        class Connection:
            def request(self,method,path,**kwargs):sent.append((method,path,json.loads(kwargs['body'])))
            def getresponse(self):return self
            status=200
            def getheader(self,*args):return 'application/json'
            def read(self,*args):return json.dumps(response).encode()
            def close(self):pass
        api=p.UploadAPI(factory=lambda *args,**kwargs:Connection());api.token='synthetic'
        self.assertEqual(api.upload(value,raw),7)
        self.assertEqual(sent[0][0:2],('POST','/api/v4/bestanden/upload'))
        self.assertEqual(base64.b64decode(sent[0][2]['data']),raw)
        self.assertFalse(sent[0][2]['scan']);self.assertEqual(sent[0][2]['directoryId'],0)
        with self.assertRaisesRegex(p.core.app.Stop,'ALREADY_ATTEMPTED'):api.upload(value,raw)

    def test_changed_source_pdf_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);value,raw=item()
            value.update({'scope':'ONE_ARCHIVE_UPLOAD_ONLY_NO_MUTATION_OR_LINK','localCopy':'source-invoice.pdf',
                          'targetDirectoryId':0,'scan':False,'mime':'application/pdf'})
            encoded=json.dumps(value).encode();(root/'upload-input.json').write_bytes(encoded)
            (root/'source-invoice.pdf').write_bytes(raw+b'changed')
            with self.assertRaisesRegex(p.core.app.Stop,'PDF_FINGERPRINT_CHANGED'):
                p.load_input(root,hashlib.sha256(encoded).hexdigest())


class Recovery(unittest.TestCase):
    def test_failed_verify_retains_stage_received_id_without_sensitive_message(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/"journal";api=FakeAPI(journal);value,raw=item()
            def fail(*args):raise RuntimeError("SYNTHETIC_SECRET_DO_NOT_LOG")
            api.verify=fail
            with self.assertRaises(p.core.app.Stop):p.execute(api,None,1,value,raw,synthetic_output(root),journal,"hash")
            event=json.loads(journal.read_text().splitlines()[-1])
            self.assertEqual(event["diagnostic"]["stage"],"READBACK_METADATA_AND_DOWNLOAD")
            self.assertEqual(event["diagnostic"]["receivedFileId"],7)
            self.assertNotIn("SYNTHETIC_SECRET",journal.read_text())

    def test_legacy_uncertain_same_bytes_blocks_renamed_input_but_not_other_source(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);value,raw=item()
            old=json.dumps({"state":"UNCERTAIN","inputHash":"old","fileSha256":value["sha256"]})+"\n"
            (root/"upload-journal.jsonl").write_text(old)
            value["uploadFileName"]="Renamed.pdf"
            with self.assertRaisesRegex(p.core.app.Stop,"SAME_BYTES_NO_RETRY"):p.require_source_not_uncertain(root,value)
            value["sha256"]="b"*64
            self.assertIsNone(p.require_source_not_uncertain(root,value))
            self.assertEqual((root/"upload-journal.jsonl").read_text(),old)

    def test_readonly_found_sha_verifies_without_upload_and_preserves_uncertain_history(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/"journal";value,raw=item();api=FakeAPI(journal)
            old=json.dumps({"state":"UNCERTAIN","inputHash":"hash","fileSha256":value["sha256"]})+"\n";journal.write_text(old)
            api.listing=lambda directory=None:{"id":0,"isMailEnHerkenInbox":True,"directories":[],"files":[{"id":7,"naam":value["uploadFileName"]}]}
            result=p.reconcile_readonly(api,None,1,value,synthetic_output(root),journal,"hash")
            self.assertEqual(result["state"],"RECONCILED_VERIFIED");self.assertEqual(api.uploads,0)
            self.assertTrue(journal.read_text().startswith(old))
            self.assertEqual(p.journal_state(journal,"hash")["fileId"],7)

    def test_no_match_multiple_and_hash_failure_remain_unresolved_no_retry(self):
        for kind in ("none","multiple","wronghash"):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                root=Path(d);journal=root/"journal";value,raw=item();api=FakeAPI(journal)
                entries=[] if kind=="none" else [{"id":7,"naam":value["uploadFileName"]}]
                if kind=="multiple":entries.append({"id":8,"naam":value["uploadFileName"]})
                api.listing=lambda directory=None:{"id":0,"isMailEnHerkenInbox":True,"directories":[],"files":entries}
                if kind=="wronghash":
                    def fail(*args):raise p.core.app.Stop("UPLOAD_DOWNLOAD_HASH_MISMATCH")
                    api.verify=fail
                result=p.reconcile_readonly(api,None,1,value,synthetic_output(root),journal,"hash")
                self.assertEqual(result["state"],"UNRESOLVED_NO_RETRY");self.assertEqual(api.uploads,0)
                with self.assertRaisesRegex(p.core.app.Stop,"PREVIOUS_OUTCOME_UNCERTAIN"):p.journal_state(journal,"hash")


class CanonicalEntrypoint(unittest.TestCase):
    def test_default_and_explicit_input_reject_canonical_uncertainty_before_credentials(self):
        for state in ("PENDING","UNCERTAIN"):
            for explicit in (False,True):
                with self.subTest(state=state,explicit=explicit),tempfile.TemporaryDirectory() as d:
                    root=Path(d);value,raw=item()
                    value.update(scope="ONE_ARCHIVE_UPLOAD_ONLY_NO_MUTATION_OR_LINK",localCopy="source-invoice.pdf",
                        targetDirectoryId=0,scan=False,mime="application/pdf")
                    # Different manifest bytes/name retain the same source PDF identity.
                    value["uploadFileName"]="Renamed INVOICE-1.pdf"
                    case=root/"renamed" if explicit else root
                    case.mkdir(exist_ok=True)
                    encoded=json.dumps(value).encode();source=case/"upload-input.json";source.write_bytes(encoded)
                    (case/"source-invoice.pdf").write_bytes(raw)
                    canonical=root/"pdf-cases"/value["sha256"];canonical.mkdir(parents=True)
                    history=json.dumps({"state":state,"inputHash":hashlib.sha256(encoded).hexdigest(),"fileSha256":value["sha256"]})+"\n"
                    (canonical/"upload-journal.jsonl").write_text(history)
                    args=["upload_invoice.py","--input-sha256",hashlib.sha256(encoded).hexdigest(),"--admin-id","1","--apply"]
                    if explicit:args.extend(["--input",str(source)])
                    with patch.object(p,"ROOT",root),patch.object(p,"runtime_private_path",side_effect=lambda v: Path(v).resolve()),patch.object(p,"PrivateOutput",synthetic_output),patch.object(p.sys,"argv",args),patch.object(p.core.app,"set_private_acl"),patch.object(p.core,"owner_sid",return_value="SYNTHETIC"),patch.object(p.core,"load_login",side_effect=AssertionError("Credential boundary reached")):
                        with self.assertRaisesRegex(p.core.app.Stop,"PREVIOUS_OUTCOME_UNCERTAIN"):p.main()
                    self.assertEqual((canonical/"upload-journal.jsonl").read_text(),history)
                    self.assertFalse((canonical/"upload.lock").exists())


class AcknowledgementEvidence(unittest.TestCase):
    def connection(self, reply, status=200, content_type="application/json"):
        class Connection:
            def request(self,*args,**kwargs):pass
            def getresponse(self):return self
            def getheader(self,*args):return content_type
            def read(self,*args):return json.dumps(reply).encode()
            def close(self):pass
        connection=Connection();connection.status=status
        return lambda *args,**kwargs:connection

    def reply(self,value):
        return {"saved":True,"scanned":False,"originalFileName":value["uploadFileName"],
            "file":{"id":7,"naam":value["uploadFileName"],"directoryId":0}}

    def test_success_evidence_contains_only_safe_shape_and_predicate_facts(self):
        value,raw=item();api=p.UploadAPI(factory=self.connection(self.reply(value)));api.token="SYNTHETIC_SECRET"
        self.assertEqual(api.upload(value,raw),7)
        self.assertEqual(api.ack_diagnostic["failedPredicates"],[])
        self.assertTrue(api.ack_diagnostic["jsonParseCompleted"])
        self.assertEqual(api.ack_diagnostic["httpStatus"],200)
        self.assertFalse(api.ack_diagnostic["candidateIsVerified"])
        self.assertEqual(api.ack_diagnostic["unverifiedCandidateFileId"],7)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/"journal";second=p.UploadAPI(factory=self.connection(self.reply(value)));second.token="SYNTHETIC_SECRET"
            second.login=lambda *args:None;second.require_same_admin=lambda:None
            second.listing=lambda directory=None:{"id":0,"isMailEnHerkenInbox":True,"directories":[],"files":[]}
            second.verify=lambda identifier,item:{"id":identifier,"naam":item["uploadFileName"],"directoryId":0}
            result=p.execute(second,None,1,value,raw,synthetic_output(root),journal,"hash")
            self.assertEqual(result["state"],"VERIFIED")
            self.assertEqual(result["acknowledgement"]["failedPredicates"],[])
            self.assertEqual(result["acknowledgement"]["httpStatus"],200)

    def test_flag_false_missing_shapes_or_wrong_directory_remain_unknown(self):
        value,raw=item()
        for kind in ("false","scanned","noFile","badId","boolDirectory","array","null"):
            reply=self.reply(value)
            if kind=="false":reply["saved"]=False
            if kind=="scanned":reply["scanned"]=True
            if kind=="noFile":reply.pop("file")
            if kind=="badId":reply["file"]["id"]="7"
            if kind=="boolDirectory":reply["file"]["directoryId"]=False
            if kind=="array":reply=[]
            if kind=="null":reply=None
            api=p.UploadAPI(factory=self.connection(reply));api.token="SYNTHETIC_SECRET"
            with self.subTest(kind=kind),self.assertRaisesRegex(p.core.app.Stop,"SAVE_RESPONSE_UNKNOWN"):api.upload(value,raw)
            self.assertTrue(api.ack_diagnostic["failedPredicates"])
            self.assertTrue(api.ack_diagnostic["unknownResponseNeverProvesFailedUploadOrRetrySafe"])

    def test_name_mismatch_still_preserves_unverified_id_and_no_secret_values_in_journal(self):
        value,raw=item();reply=self.reply(value);secret="SYNTHETIC_SECRET_DO_NOT_LOG";reply.update(originalFileName=secret,message=secret,unknownPrivateField=secret);reply["file"].update(naam=secret,private=secret)
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);journal=root/"journal";api=p.UploadAPI(factory=self.connection(reply));api.token=secret
            api.login=lambda *args:None;api.require_same_admin=lambda:None
            api.listing=lambda directory=None:{"id":0,"isMailEnHerkenInbox":True,"directories":[],"files":[]}
            with self.assertRaisesRegex(p.core.app.Stop,"NO_RETRY"):p.execute(api,None,1,value,raw,synthetic_output(root,[secret]),journal,"hash")
            record=json.loads(journal.read_text().splitlines()[-1]);diag=record["diagnostic"]
            self.assertEqual(diag["receivedFileId"],7)
            self.assertEqual(diag["receivedFileIdVerification"],"UNVERIFIED_RESPONSE_CANDIDATE_ONLY")
            self.assertIn("originalFileNameMatches",diag["acknowledgement"]["failedPredicates"])
            self.assertEqual(diag["acknowledgement"]["knownKeys"]["originalFileName"]["type"],"string")
            self.assertNotIn(secret,journal.read_text());self.assertNotIn("unknownPrivateField",journal.read_text())
            self.assertNotIn("message",diag["acknowledgement"])
            with self.assertRaisesRegex(p.core.app.Stop,"PREVIOUS_OUTCOME_UNCERTAIN"):p.journal_state(journal,"hash")

    def test_non_json_or_http_error_keeps_status_only_without_raw_headers_body(self):
        value,raw=item()
        for status,ctype in ((400,"application/json"),(200,"text/html; SYNTHETIC_SECRET")):
            api=p.UploadAPI(factory=self.connection({"message":"SYNTHETIC_SECRET"},status,ctype));api.token="synthetic"
            with self.assertRaises(p.core.app.Stop):api.upload(value,raw)
            self.assertEqual(api.ack_diagnostic["httpStatus"],status)
            self.assertFalse(api.ack_diagnostic["jsonParseCompleted"])
            self.assertNotIn("SYNTHETIC_SECRET",json.dumps(api.ack_diagnostic))


def recovery_fixture(parent):
    root=parent/"upload-trial";root.mkdir();entries=[];selected=None;old_bytes={}
    for n in range(3):
        raw=("%PDF-synthetic-recovery-"+str(n)).encode();sha=hashlib.sha256(raw).hexdigest();old=parent/"old"/str(n);old.mkdir(parents=True)
        value={"scope":"ONE_ARCHIVE_UPLOAD_ONLY_NO_MUTATION_OR_LINK","localCopy":"source-invoice.pdf","uploadFileName":"Long original source invoice "+str(n)+" "+"x"*30+".pdf","sourceInvoiceNumber":"SYNTH-"+str(n),"invoiceDate":"2030-01-01","size":len(raw),"sha256":sha,"mime":"application/pdf","targetDirectoryId":0,"scan":False}
        op=old/"upload-input.json";op.write_text(json.dumps(value)+"\n",encoding="utf-8");(old/"source-invoice.pdf").write_bytes(raw);oh=hashlib.sha256(op.read_bytes()).hexdigest()
        jr=root/"pdf-cases"/sha; jr.mkdir(parents=True);journal=jr/"upload-journal.jsonl";journal.write_text("\n".join(json.dumps({"state":state,"inputHash":oh,"fileSha256":sha,"directoryId":0}) for state in ("PENDING","UNCERTAIN"))+"\n",encoding="utf-8")
        new=parent/"new"/str(n);new.mkdir(parents=True);nv={**value,"originalSourceFileName":value["uploadFileName"],"uploadFileName":"260101_S"+str(n)+"_"+sha[:8]+".pdf"};np=new/"upload-input.json";np.write_text(json.dumps(nv)+"\n",encoding="utf-8");(new/"source-invoice.pdf").write_bytes(raw);nh=hashlib.sha256(np.read_bytes()).hexdigest()
        entry={"sourceSha256":sha,"oldInput":str(op.relative_to(parent)),"oldInputSha256":oh,"oldJournal":str(journal.relative_to(parent)),"oldJournalSha256":hashlib.sha256(journal.read_bytes()).hexdigest(),"newInput":str(np.relative_to(parent)),"newInputSha256":nh,"adminId":1,"directoryId":0,"maximumAdditionalPosts":1};entries.append(entry)
        for path in (op,old/"source-invoice.pdf",journal):old_bytes[path]=path.read_bytes()
        if n==0:selected=(nv,raw,np,nh,jr/"controlled-recovery-journal.jsonl")
    doc={"scope":"EXACT_THREE_OWNER_AUTHORIZED_UPLOAD_RECOVERIES","ownerDecision":{"authority":"OWNER_DIRECT","acceptedPossibleDuplicateArchiveFile":True},"entries":entries};auth=parent/"recovery-auth.json";auth.write_text(json.dumps(doc)+"\n",encoding="utf-8");ah=hashlib.sha256(auth.read_bytes()).hexdigest();value,raw,inp,ih,journal=selected
    spec=p.load_recovery_authorization(root,auth,ah,value,inp,ih,1)
    return root,value,raw,inp,ih,journal,spec,auth,ah,old_bytes


class RecoveryAPI(FakeAPI):
    def __init__(self,journal):super().__init__(journal);self.entries=[];self.logins=0;self.directory=0;self.verified_directory=None
    def login(self,*args):self.logins+=1
    def listing(self,directory=None):
        if directory is None:return {"id":0,"isMailEnHerkenInbox":True,"directories":[] if not self.directory else [{"id":self.directory,"naam":"2030"}],"files":self.entries if not self.directory else []}
        return {"id":self.directory,"files":self.entries,"directories":[]}
    def verify(self,identifier,value,expected_directory=0):
        self.verified_directory=expected_directory
        return {"id":identifier,"naam":value["uploadFileName"],"directoryId":expected_directory}


class ControlledRecovery(unittest.TestCase):
    def test_exactly_one_extra_post_pending_before_write_and_old_bytes_unchanged(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal)
            result=p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            self.assertEqual(result["state"],"RECOVERY_UPLOAD_VERIFIED");self.assertEqual(api.uploads,1)
            self.assertEqual([json.loads(x)["state"] for x in journal.read_text().splitlines()],["PENDING","RECOVERY_UPLOAD_VERIFIED"])
            for path,content in old.items():self.assertEqual(path.read_bytes(),content)
            api.entries=[{"id":7,"naam":value["uploadFileName"]}]
            again=p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            self.assertEqual(again["extraPostAttemptCountThisRun"],0);self.assertEqual(api.uploads,1)

    def test_found_original_in_searched_year_reuses_verified_bytes_without_post(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal);api.directory=42;api.entries=[{"id":9,"naam":value["originalSourceFileName"]}]
            result=p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            self.assertEqual(result["state"],"EXISTING_FILE_VERIFIED_NO_EXTRA_POST");self.assertEqual(api.uploads,0);self.assertEqual(api.verified_directory,42)
            self.assertEqual(result["archiveReadScope"]["directoriesChecked"],[0,42]);self.assertEqual(result["directoryId"],42);self.assertEqual(result["postDirectoryId"],0)
            for path,content in old.items():self.assertEqual(path.read_bytes(),content)

    def test_multiple_or_byte_mismatch_never_posts(self):
        for kind in ("multiple","mismatch"):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal);api.entries=[{"id":9,"naam":value["originalSourceFileName"]}]
                if kind=="multiple":api.entries.append({"id":10,"naam":value["uploadFileName"]})
                else:
                    def fail(*args,**kwargs):raise p.core.app.Stop("UPLOAD_DOWNLOAD_HASH_MISMATCH")
                    api.verify=fail
                with self.assertRaises(p.core.app.Stop):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
                self.assertEqual(api.uploads,0);self.assertFalse(journal.exists())
                for path,content in old.items():self.assertEqual(path.read_bytes(),content)

    def test_unknown_post_keeps_candidate_and_blocks_new_alias_or_authorization(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal);api.received_file_id=77;api.ack_diagnostic={"candidateIsVerified":False,"unverifiedCandidateFileId":77}
            def lost(*args):api.uploads+=1;raise p.core.app.Stop("UPLOAD_SAVE_RESPONSE_UNKNOWN")
            api.upload=lost
            with self.assertRaisesRegex(p.core.app.Stop,"NO_FURTHER_POST"):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            event=json.loads(journal.read_text().splitlines()[-1]);self.assertEqual(event["diagnostic"]["unverifiedCandidateFileId"],77)
            api.login=lambda *args:self.fail("No credential/session after uncertain recovery")
            with self.assertRaisesRegex(p.core.app.Stop,"NO_EXTRA_RETRY"):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,"different-alias-hash",spec,root)
            other={**spec,"authorizationSha256":"b"*64}
            with self.assertRaisesRegex(p.core.app.Stop,"SOURCE_ALREADY_BOUND"):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,other,root)
            self.assertEqual(api.uploads,1)
            for path,content in old.items():self.assertEqual(path.read_bytes(),content)

    def test_unsafe_missing_or_changed_admission_bindings_fail_before_credentials(self):
        for kind in ("owner","missingOwner","admin","oldJournal","oldInput","newInput","newPath","source","maxPosts","booleanPosts"):
            with self.subTest(kind=kind),tempfile.TemporaryDirectory() as d:
                root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));doc=json.loads(auth.read_text());entry=doc["entries"][0]
                if kind=="owner":doc["ownerDecision"]["authority"]="MISSING"
                if kind=="missingOwner":doc.pop("ownerDecision")
                if kind=="admin":entry["adminId"]=2
                if kind=="oldJournal":entry["oldJournalSha256"]="a"*64
                if kind=="oldInput":entry["oldInputSha256"]="a"*64
                if kind=="newInput":entry["newInputSha256"]="a"*64
                if kind=="newPath":entry["newInput"]="another/upload-input.json"
                if kind=="source":entry["sourceSha256"]="b"*64
                if kind=="maxPosts":entry["maximumAdditionalPosts"]=2
                if kind=="booleanPosts":entry["maximumAdditionalPosts"]=True
                auth.write_text(json.dumps(doc),encoding="utf-8");ah=hashlib.sha256(auth.read_bytes()).hexdigest()
                args=["upload_invoice.py","--input",str(inp),"--input-sha256",ih,"--admin-id","1","--recover-once","--recovery-authorization",str(auth),"--recovery-authorization-sha256",ah]
                with patch.object(p,"ROOT",root),patch.object(p,"runtime_private_path",side_effect=lambda v: Path(v).resolve()),patch.object(p,"PrivateOutput",synthetic_output),patch.object(p.sys,"argv",args),patch.object(p.core.app,"set_private_acl"),patch.object(p.core,"owner_sid",return_value="SYNTHETIC"),patch.object(p.core,"load_login",side_effect=AssertionError("Credential boundary reached")):
                    with self.assertRaises(p.core.app.Stop):p.main()
                self.assertFalse(journal.exists())

    def test_new_post_name_guard_max48_and_legacy_verified_longname_read_compatible(self):
        p.check_fresh_archive_name({"uploadFileName":"A"*44+".pdf"})
        for name in ("A"*45+".pdf","caf"+chr(233)+".pdf","bad\t.pdf","bad"+chr(127)+".pdf"):
            with self.assertRaises(p.core.app.Stop):p.check_fresh_archive_name({"uploadFileName":name})
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);value,raw=item();value["uploadFileName"]="Old "+"A"*60+chr(233)+".pdf";journal=root/"journal";journal.write_text(json.dumps({"state":"VERIFIED","inputHash":"hash","fileId":7})+"\n");api=FakeAPI(journal)
            result=p.execute(api,None,1,value,raw,synthetic_output(root),journal,"hash")
            self.assertEqual(result["state"],"PREVIOUS_UPLOAD_VERIFIED_NO_NEW_WRITE");self.assertEqual(api.uploads,0)


class RecoveryFailureBoundaries(unittest.TestCase):
    def test_posted_but_download_failure_blocks_another_extra_post(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal)
            def fail(*args,**kwargs):raise p.core.app.Stop("UPLOAD_DOWNLOAD_HASH_MISMATCH")
            api.verify=fail
            with self.assertRaisesRegex(p.core.app.Stop,"NO_FURTHER_POST"):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            self.assertEqual(api.uploads,1)
            with self.assertRaisesRegex(p.core.app.Stop,"NO_EXTRA_RETRY"):p.recover_once(api,None,1,value,raw,synthetic_output(root),journal,ih,spec,root)
            self.assertEqual(api.uploads,1)
            for path,content in old.items():self.assertEqual(path.read_bytes(),content)

    def test_missing_authorization_arguments_never_load_credentials(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));args=["upload_invoice.py","--input",str(inp),"--input-sha256",ih,"--admin-id","1","--recover-once"]
            with patch.object(p,"ROOT",root),patch.object(p,"runtime_private_path",side_effect=lambda v: Path(v).resolve()),patch.object(p,"PrivateOutput",synthetic_output),patch.object(p.sys,"argv",args),patch.object(p.core.app,"set_private_acl"),patch.object(p.core,"owner_sid",return_value="SYNTHETIC"),patch.object(p.core,"load_login",side_effect=AssertionError("Credentials forbidden")):
                with self.assertRaisesRegex(p.core.app.Stop,"AUTHORIZATION_ARGUMENTS_REQUIRED"):p.main()

    def test_download_requires_exact_searched_directory_not_arbitrary_metadata(self):
        value,raw=item();api=p.UploadAPI();api.token="synthetic"
        class Reader:
            def __init__(self,*args,**kwargs):pass
            def request(self,method,path,**kwargs):
                if "/bestand/" in path:return {"id":7,"naam":value["uploadFileName"],"directoryId":42}
                return {"mime":"application/pdf","bytes":raw}
        with patch.object(p.files,"Transport",Reader):
            self.assertEqual(api.verify(7,value,expected_directory=42)["directoryId"],42)
            with self.assertRaisesRegex(p.core.app.Stop,"METADATA_MISMATCH"):api.verify(7,value)


class RecoveryMainWiring(unittest.TestCase):
    def test_valid_authorization_selects_new_source_journal_and_preserves_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            root,value,raw,inp,ih,journal,spec,auth,ah,old=recovery_fixture(Path(d));api=RecoveryAPI(journal);api.secrets=[]
            args=["upload_invoice.py","--input",str(inp),"--input-sha256",ih,"--admin-id","1","--recover-once","--recovery-authorization",str(auth),"--recovery-authorization-sha256",ah]
            with patch.object(p,"ROOT",root),patch.object(p,"runtime_private_path",side_effect=lambda v: Path(v).resolve()),patch.object(p,"PrivateOutput",synthetic_output),patch.object(p.sys,"argv",args),patch.object(p.core.app,"set_private_acl"),patch.object(p.core,"owner_sid",return_value="SYNTHETIC"),patch.object(p.core,"WindowsBackend",return_value=SimpleNamespace(api=None)),patch.object(p.core,"load_login",return_value=None),patch.object(p,"UploadAPI",return_value=api):
                p.main()
            self.assertEqual(api.uploads,1);self.assertEqual(json.loads(journal.read_text().splitlines()[-1])["state"],"RECOVERY_UPLOAD_VERIFIED")
            self.assertFalse((journal.parent/"upload.lock").exists())
            for path,content in old.items():self.assertEqual(path.read_bytes(),content)


if __name__=='__main__':unittest.main()

