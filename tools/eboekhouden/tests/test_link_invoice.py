from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import link_invoice as p


def item():
    raw=b'%PDF-synthetic'
    return {'restBefore':{'id':8,'type':1,'date':'2030-08-16','invoiceNumber':'SYNTH','relationId':20,'ledgerId':10,
             'inExVat':'IN','termOfPayment':0,'rows':[{'ledgerId':31,'amount':121,'vatCode':'HOOG_INK_21','vatAmount':21}],
             'vat':[{'vatCode':'HOOG_INK_21','amount':21}]},'payload':{'fileId':70,'soort':1,'koppelId':8},
            'fileId':70,'fileName':'Synthetic SYNTH.pdf','fileSize':len(raw),'fileSha256':hashlib.sha256(raw).hexdigest(),
            'positiveControlFileId':99,'expectedAppInternalId':1000},raw


class Client:
    def __init__(self,value):self.current=copy.deepcopy(value['restBefore']);self.secrets=[]
    def get(self,path):
        assert path=='/v1/mutation/8'
        return copy.deepcopy(self.current)


class Session:
    token='synthetic-token';secrets=['synthetic-token']
    def __init__(self):self.internal=1000
    def read_mutation(self,*args):return {'id':self.internal,'mutatieNummer':8,'factuurNummer':'SYNTH','datum':'2030-08-16T00:00:00'}
    def require_same_admin(self):pass


class Environment:
    def __init__(self,value,journal):self.value=value;self.journal=journal;self.linked=False;self.calls=0;self.unknown=False
    def query(self,session,value):
        rows=[{'fileId':70,'koppelId':9000,'naam':'Synthetic SYNTH.pdf'}] if self.linked else []
        return rows,p.links.matches_file(rows,70,8,{'soort':1,'koppelId':8})
    def file(self,*args):return {'id':70,'naam':'Synthetic SYNTH.pdf','directoryId':0}
    def send(self,payload,token):
        assert json.loads(self.journal.read_text().splitlines()[-1])['state']=='PENDING'
        assert payload=={'fileId':70,'soort':1,'koppelId':8}
        self.calls+=1;self.linked=True
        if self.unknown:raise TimeoutError('synthetic-token')
        return {'fileId':70,'koppelId':8,'naam':'Synthetic SYNTH.pdf'}


class Checks(unittest.TestCase):
    def run_case(self,value,env,client,session,d,readonly=False):
        return p.execute(client,session,env,None,value,env.journal,'hash',synthetic_output(d,session.secrets),
                         read_only=readonly,query=env.query,file_check=env.file)

    def test_single_link_strict_unchanged_rest_and_response_reference_namespaces(self):
        value,raw=item();client=Client(value);session=Session()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');result=self.run_case(value,env,client,session,d)
            self.assertEqual(result['state'],'VERIFIED');self.assertEqual(env.calls,1)
            self.assertEqual(result['afterQueryFiles'][0]['koppelId'],9000)
            self.assertTrue(result['officialRestUnchanged']);self.assertEqual(client.current,value['restBefore'])

    def test_readcheck_empty_never_writes_or_creates_pending(self):
        value,raw=item()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');result=self.run_case(value,env,Client(value),Session(),d,True)
            self.assertEqual(result['state'],'MAIN_TARGET_READ_CHECKED_EMPTY_NO_WRITE')
            self.assertEqual(env.calls,0);self.assertFalse(env.journal.exists())

    def test_already_linked_does_not_link_again(self):
        value,raw=item()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');env.linked=True
            result=self.run_case(value,env,Client(value),Session(),d)
            self.assertEqual(result['state'],'ALREADY_LINKED_VERIFIED_NO_WRITE');self.assertEqual(env.calls,0)

    def test_wrong_app_id_and_changed_rest_stop_before_link(self):
        value,raw=item()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');session=Session();session.internal=1001
            with self.assertRaisesRegex(p.core.app.Stop,'APP_INTERNAL_ID_CHANGED'):
                self.run_case(value,env,Client(value),session,d)
            client=Client(value);client.current['rows'][0]['amount']=122
            with self.assertRaisesRegex(p.core.app.Stop,'BASELINE_CHANGED'):
                self.run_case(value,env,client,Session(),d)
            self.assertEqual(env.calls,0)

    def test_uncertain_response_still_reads_and_can_reconcile_without_retry(self):
        value,raw=item()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');env.unknown=True
            result=self.run_case(value,env,Client(value),Session(),d)
            self.assertEqual(result['state'],'RECONCILED_VERIFIED_AFTER_UNKNOWN_RESPONSE');self.assertEqual(env.calls,1)
            self.assertNotIn('synthetic-token',env.journal.read_text())
            self.assertEqual(result['attemptDiagnostic']['cause'],'TimeoutError')

    def test_missing_after_membership_stops_and_never_reposts(self):
        value,raw=item()
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');env.query=lambda *args:([],[])
            with self.assertRaisesRegex(p.core.app.Stop,'NO_RETRY'):
                self.run_case(value,env,Client(value),Session(),d)
            with self.assertRaisesRegex(p.core.app.Stop,'PREVIOUS_ATTEMPT'):
                self.run_case(value,env,Client(value),Session(),d)
            self.assertEqual(env.calls,1)

    def test_post_financial_change_stops_even_with_successful_link(self):
        value,raw=item();client=Client(value)
        with tempfile.TemporaryDirectory() as d:
            env=Environment(value,Path(d)/'journal');send=env.send
            def changed(payload,token):
                response=send(payload,token);client.current['vat'][0]['amount']=0;return response
            env.send=changed
            with self.assertRaisesRegex(p.core.app.Stop,'NO_RETRY'):
                self.run_case(value,env,client,Session(),d)
            last=json.loads(env.journal.read_text().splitlines()[-1])
            self.assertEqual(last['state'],'UNCERTAIN')
            self.assertEqual(last['verificationDiagnostic']['stage'],'REST_AFTER_READ')
            self.assertEqual(env.calls,1)

    def test_negative_control_file_rejects_global_or_wrong_scope_query(self):
        value,raw=item()
        class Query:
            def request(self,*args,**kwargs):return {'files':[{'fileId':99,'koppelId':888}]}
        with patch.object(p.links,'linked_query',return_value=(Query(),{'soort':1,'koppelId':8})):
            with self.assertRaisesRegex(p.core.app.Stop,'OTHER_MUTATION_CONTROL_FILE'):p.linked_read(Session(),value)

    def test_download_hash_and_only_fixed_link_post(self):
        value,raw=item()
        class Reader:
            def request(self,method,path,**kwargs):
                return {'id':70,'naam':value['fileName']} if '/bestand/' in path else {'mime':'application/pdf','bytes':raw+b'wrong'}
        with self.assertRaisesRegex(p.core.app.Stop,'PDF_HASH'):p.verify_file(Reader(),'synthetic-token',value)
        sent=[]
        class Connection:
            status=200
            def request(self,method,path,**kwargs):sent.append((method,path,json.loads(kwargs['body'])))
            def getresponse(self):return self
            def getheader(self,*args):return 'application/json'
            def read(self,*args):return b'{"fileId":70,"koppelId":8}'
            def close(self):pass
        cmd=p.LinkCommand(value['payload'],factory=lambda *a,**kw:Connection())
        self.assertFalse(cmd.allowed('PUT','/api/v4/mutaties',value['payload']))
        self.assertFalse(cmd.allowed('POST','/api/v4/bestanden/upload',value['payload']))
        cmd.send(value['payload'],'synthetic-token')
        with self.assertRaisesRegex(p.core.app.Stop,'NO_RETRY'):cmd.send(value['payload'],'synthetic-token')
        self.assertEqual(sent,[('POST','/api/v4/bestanden/koppel',value['payload'])])


if __name__=='__main__':unittest.main()
