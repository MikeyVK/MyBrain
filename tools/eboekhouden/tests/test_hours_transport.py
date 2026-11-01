"""Offline shared-transport compatibility and narrow adapter tests."""
from pathlib import Path
import io
import json
import sys
from types import SimpleNamespace
import unittest
from hours_domain import HoursError, canonical
from hours_io import AppContext, AppHoursReader, SharedWire

import app_probe as app
import processed_invoice_probe as shared

class Response:
    def __init__(self,status=200,value=None):
        self.status=status;self.content=io.BytesIO(json.dumps(value).encode('utf-8'));self.reads=0
    def getheader(self,name,default=None):
        return 'application/json' if name=='Content-Type' else default
    def read(self,size=-1):self.reads+=1;return self.content.read(size)

class Connection:
    def __init__(self,network):self.network=network
    def request(self,method,path,**kwargs):self.network.requests.append((method,path,kwargs))
    def getresponse(self):return self.network.response
    def close(self):pass

class Network:
    def __init__(self,status=200,value=None):self.response=Response(status,value);self.requests=[];self.created=0
    def factory(self,*args,**kwargs):self.created+=1;return Connection(self)

class SharedStatus(unittest.TestCase):
    def transport(self,network,**kwargs):
        return shared.Transport('app',factory=network.factory,command_policy=lambda m,p,b:True,**kwargs)
    def test_default_still_accepts_200(self):
        n=Network(200,{'ok':True});self.assertEqual(self.transport(n).request('PUT','/api/v4/uren',{}),{'ok':True})
    def test_default_still_rejects_201_and_nondelete_204(self):
        for status in [201,204]:
            with self.subTest(status=status),self.assertRaisesRegex(app.RequestFailure,'HTTP_'+str(status)):
                self.transport(Network(status)).request('PUT','/api/v4/uren',{})
    def test_legacy_delete_204_remains_none_without_json_parse(self):
        n=Network(204);self.assertIsNone(self.transport(n).request('DELETE','/api/v4/uren/10'))
        self.assertEqual(n.response.reads,0)
    def test_explicit_201_parses_json(self):
        n=Network(201,{'id':10});self.assertEqual(self.transport(n,accepted_statuses=(200,201)).request('POST','/api/v4/uren',{}),{'id':10})
    def test_explicit_204_avoids_empty_json_parse(self):
        n=Network(204);self.assertIsNone(self.transport(n,accepted_statuses=(200,204)).request('PUT','/api/v4/uren',{}))
        self.assertEqual(n.response.reads,0)
    def test_invalid_explicit_status_set_stops_without_network(self):
        for statuses in [(),(199,),(300,),(True,),('201',),(200,'201'),([200],)]:
            n=Network()
            with self.subTest(statuses=statuses),self.assertRaisesRegex(app.app.Stop,'INVALID_ACCEPTED_HTTP_STATUSES'):
                self.transport(n,accepted_statuses=statuses)
            self.assertEqual(n.created,0)
    def test_unaccepted_202_is_not_final_success(self):
        with self.assertRaisesRegex(app.RequestFailure,'HTTP_202'):
            self.transport(Network(202),accepted_statuses=(200,201)).request('POST','/api/v4/uren',{})
    def test_existing_default_allowlist_not_broadened(self):
        n=Network();t=shared.Transport('app',factory=n.factory,accepted_statuses=(200,201))
        with self.assertRaisesRegex(app.app.Stop,'EXEMPLAR_REQUEST_NOT_ALLOWED'):t.request('PUT','/api/v4/mutaties',{})
        self.assertEqual(n.created,0)
    def test_invalid_session_still_rejected_without_network(self):
        n=Network()
        with self.assertRaisesRegex(app.app.Stop,'INVALID_SESSION'):
            self.transport(n).request('GET','/api/v4/auth/userinfo',token='bad\r\nheader')
        self.assertEqual(n.created,0)
    def test_one_shot_shared_call_limit_unchanged(self):
        n=Network(200,True);t=self.transport(n);t.request('PUT','/api/v4/uren',{})
        with self.assertRaisesRegex(app.app.Stop,'EXEMPLAR_CALL_LIMIT'):t.request('PUT','/api/v4/uren',{})
        self.assertEqual(len(n.requests),1)

class NarrowAdapters(unittest.TestCase):
    def wire(self,n,writes=False):return SharedWire(shared.Transport,app.ObservedConnection,n.factory,allow_writes=writes)
    def test_readonly_wire_cannot_write_hours(self):
        n=Network()
        for method in ['POST','PUT','DELETE']:
            with self.subTest(method=method),self.assertRaises(HoursError):
                self.wire(n).call(method,'/api/v4/uren',{})
        self.assertEqual(n.created,0)
    def test_write_wire_cannot_write_other_app_domains(self):
        n=Network()
        for path in ['/api/v4/mutaties','/api/v4/bestanden/upload','/api/v4/projecten']:
            with self.subTest(path=path),self.assertRaises(HoursError):self.wire(n,True).call('PUT',path,{})
        self.assertEqual(n.created,0)
    def test_status_observation_and_source_bound_request(self):
        n=Network(201,{'id':41});result=self.wire(n,True).call('POST','/api/v4/uren',{'id':0},access='synthetic',accepted=(200,201))
        self.assertEqual(result.status,201);self.assertEqual(result.data(),{'id':41})
        self.assertEqual(n.requests[0][0:2],('POST','/api/v4/uren'))
        self.assertEqual(json.loads(n.requests[0][2]['body']),{'id':0})
    def test_context_mismatch_stops_before_fresh_context_call(self):
        class Auth:
            admin=(12,'other')
            def require_same_admin(self):raise AssertionError('must not call')
        with self.assertRaisesRegex(HoursError,'ADMINISTRATION_MISMATCH'):AppContext(Auth()).confirm(800100)
    def test_day_query_exact_read_route_and_bounds(self):
        n=Network(200,{'items':[],'hasMoreRows':False})
        reader=AppHoursReader(self.wire(n),SimpleNamespace(token='synthetic'),app.RequestFailure)
        self.assertEqual(reader.find_marker('synthetic-marker','2030-10-31'),())
        method,path,kwargs=n.requests[0];body=json.loads(kwargs['body'])
        self.assertEqual((method,path),('POST','/api/v4/uren/filter'))
        self.assertEqual((body['page'],body['pageSize']),(1,20))
        self.assertEqual(body['period'],{'startDate':'2030-10-31T00:00:00Z','endDate':'2030-10-31T23:59:59Z'})
    def test_incomplete_day_query_cannot_claim_marker_absent(self):
        n=Network(200,{'items':[],'hasMoreRows':True})
        reader=AppHoursReader(self.wire(n),SimpleNamespace(token='synthetic'),app.RequestFailure)
        with self.assertRaisesRegex(HoursError,'HOURS_DAY_QUERY_INCOMPLETE'):reader.find_marker('synthetic','2030-10-31')
    def test_matching_detail_id_is_mandatory(self):
        n=Network(200,{'id':99})
        reader=AppHoursReader(self.wire(n),SimpleNamespace(token='synthetic'),app.RequestFailure)
        with self.assertRaisesRegex(HoursError,'HOURS_DETAIL_IDENTITY_MISMATCH'):reader.read_hour(41)

if __name__=='__main__':unittest.main()
