from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import copy
import json
from pathlib import Path
import tempfile
import unittest
import change_ledger as p


def fixture():
    before={'id':8,'type':1,'date':'2030-08-16','invoiceNumber':'SYNTH','entryNumber':'','description':'Synthetic',
            'relationId':20,'ledgerId':10,'inExVat':'IN','termOfPayment':0,
            'rows':[{'ledgerId':30,'vatCode':'HOOG_INK_21','amount':121,'vatAmount':21,'description':'Synthetic',
                     'invoiceNumber':'SYNTH','relationId':20,'costCenterId':40}],
            'vat':[{'vatCode':'HOOG_INK_21','amount':21}]}
    after=copy.deepcopy(before);after['rows'][0]['ledgerId']=31
    payload={'id':123456,'mutatieNummer':8,'factuurNummer':'SYNTH','datum':'2030-08-16T00:00:00','boekstuk':'',
             'omschrijving':'Synthetic','soort':1,'grootboekRekeningId':10,'isInclusiefBtw':True,'termijnInDagen':0,
             'relatieId':20,'mutatieRegels':[{'index':0,'tegenRekeningId':31,'btwCode':'HOOG_INK_21','bedrag':121,'omschrijving':'Synthetic'}]}
    return {'restBefore':before,'restAfter':after,'payloadA':payload,'oldLedgerId':30,'newLedgerId':31,'newLedgerCode':'7000'}


class Client:
    def __init__(self,item):self.item=item;self.current=copy.deepcopy(item['restBefore']);self.secrets=[]
    def get(self,path):
        if path=='/v1/mutation/8':return copy.deepcopy(self.current)
        if path=='/v1/ledger/31':return {'id':31,'code':'7000','category':'VW'}
        raise AssertionError('Unexpected read '+path)


class Session:
    token='synthetic-session'
    def __init__(self,client):self.client=client;self.wrong_id=False
    def read_mutation(self,transport,number,day):
        changed=self.client.current['rows'][0]['ledgerId']==31
        record=copy.deepcopy(self.client.item['payloadA'])
        record['id']=999 if changed else 123456
        if self.wrong_id and not changed:record['id']=123457
        record['bedrag']=0
        record['mutatieRegels'][0]['tegenRekeningId']=31 if changed else 30
        record['mutatieRegels'][0].update({'btw':0,'bedragInclusief':100,'bedragExclusief':100})
        return record
    def require_same_admin(self):pass


class Command:
    def __init__(self,client,journal):self.client=client;self.journal=journal;self.calls=0;self.sent=None
    def send(self,payload,token):
        assert json.loads(self.journal.read_text().splitlines()[-1])['state']=='PENDING'
        self.calls+=1;self.sent=copy.deepcopy(payload);self.client.current=copy.deepcopy(self.client.item['restAfter'])
        return {'id':999,'mutatieNummer':8}


class Checks(unittest.TestCase):
    def test_success_exact_a_finances_references_costcenter_and_new_internal_id(self):
        value=fixture();client=Client(value)
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';command=Command(client,journal)
            result=p.execute(client,lambda:Session(client),command,value,journal,'hash',synthetic_output(d))
            self.assertEqual(result['state'],'VERIFIED');self.assertEqual(result['appInternalIdAfter'],999)
            self.assertEqual(command.sent,value['payloadA']);self.assertEqual(command.calls,1)
            self.assertNotIn('bedrag',command.sent);self.assertNotIn('btw',command.sent['mutatieRegels'][0])
            self.assertEqual(client.current['rows'][0]['costCenterId'],40)

    def test_rest_baseline_change_stops_before_session_or_put(self):
        value=fixture();client=Client(value);client.current['description']='External change'
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';command=Command(client,journal)
            with self.assertRaisesRegex(p.core.app.Stop,'BASELINE_CHANGED'):
                p.execute(client,lambda:self.fail('No App login'),command,value,journal,'hash',synthetic_output(d))
            self.assertEqual(command.calls,0);self.assertFalse(journal.exists())

    def test_fresh_internal_id_mismatch_stops_before_pending(self):
        value=fixture();client=Client(value);session=Session(client);session.wrong_id=True
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';command=Command(client,journal)
            with self.assertRaisesRegex(p.core.app.Stop,'INTERNAL_ID_CHANGED'):
                p.execute(client,lambda:session,command,value,journal,'hash',synthetic_output(d))
            self.assertEqual(command.calls,0);self.assertFalse(journal.exists())

    def test_unexpected_post_vat_or_relation_change_is_uncertain_not_hidden(self):
        for mutate in [lambda c:c.current['vat'][0].update(amount=0),lambda c:c.current.update(relationId=21)]:
            value=fixture();client=Client(value)
            with tempfile.TemporaryDirectory() as d:
                journal=Path(d)/'journal';command=Command(client,journal);send=command.send
                def wrong(payload,token):
                    response=send(payload,token);mutate(client);return response
                command.send=wrong
                with self.assertRaisesRegex(p.core.app.Stop,'NO_RETRY'):
                    p.execute(client,lambda:Session(client),command,value,journal,'hash',synthetic_output(d))
                last=json.loads(journal.read_text().splitlines()[-1]);self.assertEqual(last['state'],'UNCERTAIN')
                self.assertEqual(last['diagnostic']['receivedAppInternalId'],999)
                self.assertEqual(command.calls,1)

    def test_lost_response_blocks_second_put_and_preserves_safe_cause(self):
        value=fixture();client=Client(value)
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';command=Command(client,journal)
            def lost(payload,token):command.calls+=1;raise TimeoutError('synthetic-session')
            command.send=lost
            with self.assertRaises(p.core.app.Stop):p.execute(client,lambda:Session(client),command,value,journal,'hash',synthetic_output(d,['synthetic-session']))
            with self.assertRaisesRegex(p.core.app.Stop,'PRIOR_ATTEMPT'):
                p.execute(client,lambda:self.fail('No relogin'),command,value,journal,'hash',synthetic_output(d))
            self.assertEqual(command.calls,1);self.assertNotIn('synthetic-session',journal.read_text())
            self.assertIn('TimeoutError',journal.read_text())

    def test_already_target_checks_ledger_but_no_app_login_or_put(self):
        value=fixture();client=Client(value);client.current=copy.deepcopy(value['restAfter'])
        with tempfile.TemporaryDirectory() as d:
            journal=Path(d)/'journal';command=Command(client,journal)
            result=p.execute(client,lambda:self.fail('No App login'),command,value,journal,'hash',synthetic_output(d))
            self.assertEqual(result['state'],'ALREADY_TARGET_VERIFIED_NO_PUT');self.assertEqual(command.calls,0)

    def test_command_only_exact_put_once_over_existing_transport(self):
        value=fixture();sent=[]
        class Connection:
            status=200
            def request(self,method,path,**kw):sent.append((method,path,json.loads(kw['body'])))
            def getresponse(self):return self
            def getheader(self,*args):return 'application/json'
            def read(self,*args):return b'{"id":999,"mutatieNummer":8}'
            def close(self):pass
        command=p.AppMutationCommand(value['payloadA'],factory=lambda *a,**kw:Connection())
        for method,path,body in [('POST','/api/v4/mutaties',{}),('PUT','/api/v4/bestanden/koppel',{}),('DELETE','/api/v4/mutaties/8',None)]:
            self.assertFalse(command.allowed(method,path,body))
        command.send(value['payloadA'],'synthetic-session')
        with self.assertRaisesRegex(p.core.app.Stop,'NO_SECOND_PUT'):command.send(value['payloadA'],'synthetic-session')
        self.assertEqual(sent, [('PUT','/api/v4/mutaties',value['payloadA'])])


if __name__=='__main__':unittest.main()
