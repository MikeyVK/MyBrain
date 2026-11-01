import copy
import json
from pathlib import Path
import tempfile
import unittest
import book_one_invoice as p
from private_output import PrivateOutput as _PrivateOutput

def PrivateOutput(root, secrets=()):
    return _PrivateOutput(root, secrets, path_validator=Path)


def item():
    return {"payload":{"type":1,"date":"2030-08-16","ledgerId":10,"invoiceNumber":"SYNTH-INVOICE",
            "termOfPayment":0,"inExVat":"IN","description":"Synthetic purchase","relationId":20,
            "rows":[{"ledgerId":30,"vatCode":"HOOG_INK_21","amount":121.0,"description":"Synthetic item"}]},
            "expectedMoney":{"gross":"121.00","net":"100.00","vat":"21.00"},
            "relationCode":"SYNTH01","headerLedgerCode":"1700","rowLedgerCode":"7020","archiveFileId":40}


def readback(value):
    result=copy.deepcopy(value['payload']);result['id']=50
    result['rows'][0]['vatAmount']=21.0
    result['vat']=[{'vatCode':'HOOG_INK_21','amount':21.0}]
    return result


class Client:
    def __init__(self, value):self.item=value;self.paths=set();self.secrets=[];self.existing=[]
    def get(self,path):
        if path.startswith('/v1/mutation?'):return {'items':self.existing,'count':len(self.existing)}
        if path=='/v1/ledger/10':return {'id':10,'code':'1700','category':'CRED'}
        if path=='/v1/ledger/30':return {'id':30,'code':'7020','category':'VW'}
        raise AssertionError('Unexpected request '+path)
    def detail(self,kind,identifier):
        if kind=='relation':return {'id':20,'code':'SYNTH01','inactive':False}
        if kind=='mutation':return readback(self.item)
        raise AssertionError('Use existing detail contract correctly')


class Checks(unittest.TestCase):
    def test_success_one_purchase_no_payment_vat_override_or_archive_link(self):
        value=item();client=Client(value)
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';out=PrivateOutput(d);sent=[]
            class Command:
                def create(self,payload):
                    self_outer.assertEqual(json.loads(journal.read_text().splitlines()[-1])['state'],'PENDING')
                    sent.append(copy.deepcopy(payload));return 50
            self_outer=self
            result=p.execute(client,Command(),value,journal,'hash',out)
            self.assertEqual(result['mutationId'],50)
            self.assertEqual(result['amounts']['netVerifiedBySubtraction'],'100.00')
            self.assertEqual(sent,[value['payload']]);self.assertEqual(sent[0]['termOfPayment'],0)
            self.assertNotIn('vatAmount',sent[0]['rows'][0]);self.assertNotIn('archiveFileId',sent[0])

    def test_other_mutation_type_invoice_reference_prevents_duplicate_booking(self):
        value=item();client=Client(value);client.existing=[{'id':60,'type':6,'invoiceNumber':'SYNTH-INVOICE'}]
        with self.assertRaisesRegex(p.base.app.app.Stop,'EXISTING_INVOICE_NUMBER'):
            p.precheck(client,value,None)

    def test_nonmatching_filter_result_is_not_empty_success(self):
        value=item();client=Client(value);client.existing=[{'id':60,'type':1,'invoiceNumber':'OTHER'}]
        with self.assertRaisesRegex(p.base.app.app.Stop,'NOT_EXACT'):p.precheck(client,value,None)

    def test_readback_wrong_vat_or_term_zero_changed_stops(self):
        value=item();detail=readback(value);detail['vat'][0]['amount']=20
        with self.assertRaisesRegex(p.base.app.app.Stop,'VAT_MISMATCH'):p.verify_readback(detail,value,50)
        detail=readback(value);detail['termOfPayment']=14
        with self.assertRaisesRegex(p.base.app.app.Stop,'HEADER_MISMATCH'):p.verify_readback(detail,value,50)

    def test_wrong_relation_identity_blocks_before_post(self):
        value=item();client=Client(value)
        client.detail=lambda kind,identifier:{'id':20,'code':'OTHER','inactive':False}
        with self.assertRaisesRegex(p.base.app.app.Stop,'RELATION_ID_CODE'):p.precheck(client,value,None)

    def test_lost_response_persisted_and_replay_blocked(self):
        value=item();client=Client(value)
        class Command:
            def create(self,payload):raise TimeoutError()
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal'
            with self.assertRaisesRegex(p.base.app.app.Stop,'NO_RETRY'):
                p.execute(client,Command(),value,journal,'hash',PrivateOutput(d))
            with self.assertRaisesRegex(p.base.app.app.Stop,'PREVIOUS_OUTCOME_UNCERTAIN'):
                p.journal_state(journal,'hash')

    def test_shared_command_denies_payment_and_second_purchase(self):
        client=p.base.Client([],{'acceptedAmazonCentralCode':'unused'},lambda *a,**kw:self.fail('Network'))
        with self.assertRaisesRegex(p.base.app.app.Stop,'ONLY_PURCHASE_INVOICE'):
            p.RestCreateCommand(client,'/v1/mutation',[{'type':4}])
        with self.assertRaisesRegex(p.base.app.app.Stop,'SCOPE_INVALID'):
            p.RestCreateCommand(client,'/v1/mutation',[item()['payload'],item()['payload']])

    def test_only_exact_header_projection_allowed_finances_still_strict(self):
        value=item();detail=readback(value);detail['rows'][0]['description']=value['payload']['description']
        result=p.verify_readback(detail,value,50)
        self.assertEqual(result['rowDescriptionEvidence']['status'],'EXACT_HEADER_PROJECTION_OBSERVED_NOT_VENDOR_GUARANTEE')
        detail['rows'][0]['description']='Unrelated description'
        with self.assertRaisesRegex(p.base.app.app.Stop,'DESCRIPTION_UNKNOWN'):p.verify_readback(detail,value,50)
        detail['rows'][0]['description']=value['payload']['description'];detail['rows'][0]['amount']=122
        with self.assertRaisesRegex(p.base.app.app.Stop,'ROW_MISMATCH'):p.verify_readback(detail,value,50)

    def test_failure_retains_stage_cause_received_id(self):
        value=item();client=Client(value)
        original=client.detail
        def detail(kind,identifier):
            result=original(kind,identifier)
            if kind=='mutation':result['rows'][0]['amount']=122
            return result
        client.detail=detail
        class Command:
            def create(self,payload):return 50
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal'
            with self.assertRaises(p.base.app.app.Stop) as caught:
                p.execute(client,Command(),value,journal,'hash',PrivateOutput(d))
            self.assertIsNotNone(caught.exception.__cause__)
            diagnostic=json.loads(journal.read_text().splitlines()[-1])['diagnostic']
            self.assertEqual(diagnostic['stage'],'READBACK_VERIFY')
            self.assertEqual(diagnostic['receivedMutationId'],50)
            self.assertEqual(diagnostic['cause'],'BOOK_ONE_READBACK_ROW_MISMATCH')

    def test_offline_reconcile_retains_old_journal_and_blocks_new_post_path(self):
        import reconcile_one_invoice as r
        value=item();detail=readback(value);detail['rows'][0]['description']=value['payload']['description']
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';old=json.dumps({'state':'UNCERTAIN','inputHash':'hash'})+'\n';journal.write_text(old)
            result=r.reconcile(value,{'mutation':detail},50,'receipt-hash','hash',journal,PrivateOutput(d))
            self.assertEqual(result['state'],'RECONCILED_VERIFIED')
            self.assertTrue(result['noApiCallsOrNewPosting'])
            self.assertTrue(journal.read_text().startswith(old))
            self.assertEqual(p.journal_state(journal,'hash')['mutationId'],50)


class Variants(unittest.TestCase):
    def variant(self, mode="IN", vat="HOOG_INK_21", count=1, term=14, sign=1):
        value=item();value["scope"]="ONE_OWNER_AUTHORIZED_PURCHASE_INVOICE_ONLY"
        value["payload"].update(type="1",inExVat=mode,termOfPayment=term)
        net=100*sign;tax=21*sign if vat=="HOOG_INK_21" else 0;gross=net+tax
        value["payload"]["rows"]=[{"ledgerId":30+i,"vatCode":vat,"amount":gross if mode=="IN" else net,"description":"Synthetic row"} for i in range(count)]
        value["expectedRows"]=[{"net":net,"vat":tax,"gross":gross,"ledgerCode":"7020"} for _ in range(count)]
        value["expectedMoney"]={"net":net*count,"vat":tax*count,"gross":gross*count}
        return value

    def detail(self,value):
        result=copy.deepcopy(value["payload"]);result.update(id=50,type=1)
        groups={}
        for row,money in zip(result["rows"],value["expectedRows"]):
            row["vatAmount"]=money["vat"]
            groups[row["vatCode"]]=groups.get(row["vatCode"],p.Decimal("0"))+p.cents(money["vat"])
        result["vat"]=[{"vatCode":k,"amount":v} for k,v in groups.items()]
        return result

    def test_all_actual_terms_multirow_modes_and_credit_strict(self):
        for term in (0,8,10,14):
            for mode,vat,count,sign in (("IN","HOOG_INK_21",4,1),("EX","BI_EU_INK",1,1),("IN","HOOG_INK_21",1,-1)):
                with self.subTest(term=term,mode=mode,count=count,sign=sign):
                    value=self.variant(mode,vat,count,term,sign)
                    p.validate_item(value)
                    verified=p.verify_readback(self.detail(value),value,50)
                    self.assertEqual(p.cents(verified["gross"]),p.cents(value["expectedMoney"]["gross"]))
                    self.assertNotIn("vatAmount",value["payload"]["rows"][0])

    def test_private_original_source_vat_retained_but_not_claimed(self):
        value=self.variant(count=2,term=0)
        value["payload"]["rows"][0].update(ledgerId=31,vatCode="GEEN",amount=6.05)
        value["expectedRows"][0]={"ledgerCode":"1410","gross":"6.05","net":"6.05","vat":"0",
            "sourceAmounts":{"gross":"6.05","net":"5.00","vat":"1.05"},
            "treatment":"OWNER_ACCEPTED_PRIVATE_GROSS_NO_INPUT_VAT"}
        value["expectedMoney"]={"gross":"127.05","net":"106.05","vat":"21"}
        p.validate_item(value);p.verify_readback(self.detail(value),value,50)
        self.assertEqual(value["expectedRows"][0]["sourceAmounts"]["vat"],"1.05")
        value["expectedRows"][0]["vat"]="1.05"
        with self.assertRaises(p.base.app.app.Stop):p.validate_item(value)

    def test_later_row_ledger_money_costcenter_vat_group_and_order_tampering(self):
        value=self.variant(count=2)
        for field,replacement in (("ledgerId",999),("amount",122),("costCenterId",9),("vatAmount",20)):
            detail=self.detail(value);detail["rows"][1][field]=replacement
            with self.subTest(field=field),self.assertRaises(p.base.app.app.Stop):p.verify_readback(detail,value,50)
        detail=self.detail(value);detail["vat"][0]["amount"]=21
        with self.assertRaises(p.base.app.app.Stop):p.verify_readback(detail,value,50)
        detail=self.detail(value);detail["rows"].reverse()
        with self.assertRaises(p.base.app.app.Stop):p.verify_readback(detail,value,50)

    def test_unsupported_values_and_missing_expectations_fail_before_network(self):
        for key,replacement in (("type",True),("type",4),("termOfPayment",15),("description","X"*51),("inExVat","OTHER")):
            value=self.variant();value["payload"][key]=replacement
            with self.subTest(key=key),self.assertRaises(p.base.app.app.Stop):p.validate_item(value)
        value=self.variant(mode="EX",vat="BI_EU_INK");del value["expectedRows"]
        with self.assertRaisesRegex(p.base.app.app.Stop,"EXPECTATIONS_REQUIRED"):p.validate_item(value)
        value=self.variant();value["payload"]["rows"][0]["vatAmount"]=21
        with self.assertRaises(p.base.app.app.Stop):p.validate_item(value)
        with self.assertRaises(p.base.app.app.Stop):p.cents("1.001")

    def test_all_expense_ledgers_are_prechecked_not_only_first(self):
        value=self.variant(count=2);client=Client(value);seen=[];old=client.get
        def get(path):
            seen.append(path)
            if path=="/v1/ledger/31":return {"id":31,"code":"7020","category":"FIN"}
            return old(path)
        client.get=get
        with self.assertRaisesRegex(p.base.app.app.Stop,"CATEGORY_MISMATCH"):p.precheck(client,value,None)
        self.assertIn("/v1/ledger/31",seen)


class GroupVatContract(unittest.TestCase):
    variant = Variants.variant
    detail = Variants.detail
    def test_missing_optional_row_vat_accepts_only_exact_group_totals(self):
        value=self.variant(count=2);detail=self.detail(value)
        for row in detail["rows"]:del row["vatAmount"]
        result=p.verify_readback(detail,value,50)
        self.assertEqual(result["vat"],"42.00")
        self.assertEqual([e["status"] for e in result["rowVatEvidence"]],["NOT_RETURNED_BY_API"]*2)
        self.assertTrue(all("returnedVatAmount" not in e for e in result["rowVatEvidence"]))
        for changed in ([],[{"vatCode":"GEEN","amount":42}],[{"vatCode":"HOOG_INK_21","amount":41.99}]):
            broken=copy.deepcopy(detail);broken["vat"]=changed
            with self.assertRaises(p.base.app.app.Stop):p.verify_readback(broken,value,50)

    def test_present_wrong_or_null_vat_rejected_despite_correct_group(self):
        value=self.variant(count=2)
        for amount in (20,None):
            detail=self.detail(value);detail["rows"][0]["vatAmount"]=amount
            with self.assertRaisesRegex(p.base.app.app.Stop,"ROW_VAT_MISMATCH"):p.verify_readback(detail,value,50)

    def test_synthetic_two_rows_absent_vat_exact_group_total(self):
        value=self.variant(count=2,term=0)
        value["payload"]["rows"][0]["amount"]=60.50;value["payload"]["rows"][1]["amount"]=12.10
        value["expectedRows"]=[{"net":"50.00","vat":"10.50","gross":"60.50","ledgerCode":"4700"},
            {"net":"10.00","vat":"2.10","gross":"12.10","ledgerCode":"4560"}]
        value["expectedMoney"]={"net":"60.00","vat":"12.60","gross":"72.60"}
        p.validate_item(value);detail=self.detail(value)
        for row in detail["rows"]:del row["vatAmount"]
        result=p.verify_readback(detail,value,50)
        self.assertEqual((result["gross"],result["vat"],result["netVerifiedBySubtraction"]),("72.60","12.60","60.00"))
        detail["rows"][1]["amount"]=12.11
        with self.assertRaises(p.base.app.app.Stop):p.verify_readback(detail,value,50)

    def test_offline_reconciliation_received_id_conflict_cannot_clear_journal(self):
        import reconcile_one_invoice as reconcile
        value=item();detail=readback(value)
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/"journal";old=json.dumps({"state":"UNCERTAIN","inputHash":"hash","diagnostic":{"receivedMutationId":51}})+"\n";journal.write_text(old)
            with self.assertRaisesRegex(p.base.app.app.Stop,"RECEIVED_ID_CONFLICT"):
                reconcile.reconcile(value,{"mutation":detail},50,"receipt","hash",journal,PrivateOutput(d))
            self.assertEqual(journal.read_text(),old)


class OfflineCaseEntrypoint(unittest.TestCase):
    def test_explicit_private_case_and_original_selected_receipt_append_only(self):
        from unittest.mock import patch
        import hashlib
        import reconcile_one_invoice as reconcile
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);code=root/"prebooking";code.mkdir();case=root/"case";case.mkdir();official=root/"rest";official.mkdir()
            value=item();value["scope"]="ONE_OWNER_AUTHORIZED_PURCHASE_INVOICE_ONLY"
            inp=case/"purchase-one-input.json";raw=json.dumps(value).encode();inp.write_bytes(raw);ih=hashlib.sha256(raw).hexdigest()
            receipt=official/"selected-mutation-synthetic.json";rr=json.dumps({"mutation":readback(value)}).encode();receipt.write_bytes(rr)
            journal=case/"purchase-one-journal.jsonl";old=json.dumps({"state":"UNCERTAIN","inputHash":ih,"diagnostic":{"receivedMutationId":50}})+"\n";journal.write_text(old)
            args=["reconcile_one_invoice.py","--input",str(inp),"--input-sha256",ih,"--receipt",str(receipt),"--receipt-sha256",hashlib.sha256(rr).hexdigest(),"--mutation-id","50"]
            with patch.object(reconcile,"runtime_area",return_value=code),patch.object(reconcile,"private_path",side_effect=lambda v:Path(v).resolve()),patch.object(reconcile.book,"PrivateOutput",PrivateOutput),patch.object(p.sys,"argv",args),patch.object(p.base,"Client",side_effect=AssertionError("Network forbidden")):
                reconcile.main()
            self.assertTrue(journal.read_text().startswith(old));self.assertEqual(json.loads(journal.read_text().splitlines()[-1])["state"],"RECONCILED_VERIFIED")
            self.assertFalse((case/"purchase-one.lock").exists())


class OwnerGroupVatPolicy(unittest.TestCase):
    variant = Variants.variant
    detail = Variants.detail

    def approved(self):
        value=self.variant(count=4,term=0)
        value["sourceInvoiceId"]="SYNTH-GROUP-POLICY"
        value["provenance"]={"currentSourceSha256":"a"*64}
        source=copy.deepcopy(value["expectedMoney"])
        value["expectedMoney"]={"gross":"484.00","net":"400.01","vat":"83.99"}
        decision={"authority":"OWNER_DIRECT","decidedAt":"2030-10-31","sourceInvoiceId":value["sourceInvoiceId"],
            "sourcePdfSha256":"a"*64,"sourceRowsHash":p.payload_hash(value["expectedRows"]),
            "payloadHash":p.payload_hash(value["payload"]),"sourceMoney":source,"bookingMoney":copy.deepcopy(value["expectedMoney"]),
            "vatCode":"HOOG_INK_21","noRowAllocation":True}
        value["groupVatPolicy"]={"mode":"OWNER_APPROVED_LOWER_GROUP_VAT_NO_ROW_ALLOCATION","ownerDecision":decision,"ownerDecisionSha256":p.payload_hash(decision)}
        return value

    def policy_detail(self,value):
        detail=self.detail(value)
        for row in detail["rows"]:del row["vatAmount"]
        detail["vat"][0]["amount"]=83.99
        return detail

    def resign(self,value):
        value["groupVatPolicy"]["ownerDecisionSha256"]=p.payload_hash(value["groupVatPolicy"]["ownerDecision"])

    def test_source_preserved_owner_group_exact_no_individual_allocation(self):
        value=self.approved();original=copy.deepcopy(value["expectedRows"])
        p.validate_item(value);result=p.verify_readback(self.policy_detail(value),value,50)
        self.assertEqual(value["expectedRows"],original)
        self.assertEqual(result["vat"],"83.99");self.assertEqual(result["netVerifiedBySubtraction"],"400.01")
        self.assertEqual(result["sourceVsBookingGroupVat"]["sourceMoney"]["vat"],84)
        self.assertFalse(result["sourceVsBookingGroupVat"]["differenceAllocatedToIndividualRows"])
        self.assertTrue(all(v["status"]=="NOT_RETURNED_BY_API" and "returnedVatAmount" not in v for v in result["rowVatEvidence"]))
        self.assertTrue(all("vatAmount" not in row for row in value["payload"]["rows"]))

    def test_increased_vat_larger_difference_or_gross_change_rejected(self):
        for changes in ({"vat":"84.01","net":"399.99"},{"vat":"83.98","net":"400.02"},{"gross":"484.01","net":"400.02"}):
            value=self.approved();value["expectedMoney"].update(changes);value["groupVatPolicy"]["ownerDecision"]["bookingMoney"]=copy.deepcopy(value["expectedMoney"]);self.resign(value)
            with self.subTest(changes=changes),self.assertRaises(p.base.app.app.Stop):p.validate_item(value)

    def test_missing_authority_stale_hash_or_source_binding_cannot_activate(self):
        for changed in ("authority","hash","pdf","sourceRows","payload"):
            value=self.approved();decision=value["groupVatPolicy"]["ownerDecision"]
            if changed=="authority":decision.pop("authority");self.resign(value)
            if changed=="hash":value["groupVatPolicy"]["ownerDecisionSha256"]="b"*64
            if changed=="pdf":value["provenance"]["currentSourceSha256"]="b"*64
            if changed=="sourceRows":value["expectedRows"][0]["net"]="99.99"
            if changed=="payload":value["payload"]["rows"][0]["description"]="Altered source"
            with self.subTest(changed=changed),self.assertRaises(p.base.app.app.Stop):p.validate_item(value)
        value=self.approved();value.pop("groupVatPolicy")
        with self.assertRaisesRegex(p.base.app.app.Stop,"SOURCE_MONEY_CONFLICT"):p.validate_item(value)

    def test_group_policy_rejects_ex_credits_mixed_and_any_returned_row_vat(self):
        for kind in ("EX","credit","mixed"):
            value=self.approved()
            if kind=="EX":value["payload"]["inExVat"]="EX"
            if kind=="credit":value["payload"]["rows"][0]["amount"]=-121
            if kind=="mixed":value["payload"]["rows"][0]["vatCode"]="GEEN"
            value["groupVatPolicy"]["ownerDecision"]["payloadHash"]=p.payload_hash(value["payload"]);self.resign(value)
            with self.subTest(kind=kind),self.assertRaises(p.base.app.app.Stop):p.validate_item(value)
        value=self.approved();detail=self.policy_detail(value);detail["rows"][0]["vatAmount"]=21
        with self.assertRaisesRegex(p.base.app.app.Stop,"UNALLOCATED_ROW_VAT_REPRESENTATION_UNKNOWN"):p.verify_readback(detail,value,50)

    def test_group_source_amount_or_actual_group_mismatch_still_rejected(self):
        value=self.approved();value["groupVatPolicy"]["ownerDecision"]["sourceMoney"]["vat"]=83;self.resign(value)
        with self.assertRaises(p.base.app.app.Stop):p.validate_item(value)
        value=self.approved();detail=self.policy_detail(value);detail["vat"][0]["amount"]=84
        with self.assertRaisesRegex(p.base.app.app.Stop,"VAT_MISMATCH"):p.verify_readback(detail,value,50)


if __name__=='__main__':unittest.main()
