from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import unittest
import json
from pathlib import Path
import tempfile
import probe_link_contract as p


class Session:
    token='synthetic-session';secrets=['synthetic-session']
    def read_mutation_raw(self,*args):
        return {'id':900,'mutatieNummer':8,'factuurNummer':'SYNTH','datum':'2030-01-19T00:00:00','mutatieRegels':[],
                'extraLinkField':[]}
    def require_same_admin(self):pass


class Metadata:
    def request(self,*args,**kwargs):return {'id':70,'naam':'Synthetic SYNTH.pdf','directoryId':0}


class Query:
    def __init__(self,value):self.value=value
    def request(self,method,path,body,**kwargs):
        assert method=='POST' and path=='/api/v4/bestanden/gekoppeld' and body=={'soort':1,'koppelId':8}
        return self.value


class Checks(unittest.TestCase):
    def item(self):return {'visibleMutationNumber':8,'knownDate':'2030-01-19','invoiceNumber':'SYNTH','knownFileId':70}
    def test_policy_only_one_source_backed_read_body_visible_number(self):
        reader,body=p.linked_query(8,factory=lambda *a,**kw:self.fail('No network'))
        self.assertEqual(body,{'soort':1,'koppelId':8})
        self.assertTrue(reader.allowed('POST','/api/v4/bestanden/gekoppeld',body))
        for path,candidate in [('/api/v4/bestanden/koppel',body),('/api/v4/bestanden/gekoppeld',{'soort':1,'koppelId':900}),
                               ('/api/v4/bestanden/gekoppeld',{'soort':2,'koppelId':8})]:
            self.assertFalse(reader.allowed('POST',path,candidate))

    def test_positive_candidate_found_with_distinct_internal_id(self):
        result=p.run(Session(),self.item(),lambda n:(Query({'files':[{'fileId':70,'naam':'Synthetic SYNTH.pdf'}]}),{'soort':1,'koppelId':n}),lambda n:Metadata())
        self.assertTrue(result['knownFileFoundInLinkedQuery']);self.assertEqual(result['actualAppInternalId'],900)
        self.assertEqual(result['hypothesis']['koppelId'],8);self.assertTrue(result['noLinkUploadMutationBankOrSheetWrites'])

    def test_empty_result_is_not_a_positive_contract_proof(self):
        result=p.run(Session(),self.item(),lambda n:(Query({'files':[]}),{'soort':1,'koppelId':n}),lambda n:Metadata())
        self.assertFalse(result['knownFileFoundInLinkedQuery'])

    def test_file_id_explicit_namespace_and_shape_unknown_stop(self):
        self.assertEqual(p.matches_file([{'id':700,'fileId':70}],70,8,{'soort':1,'koppelId':8}),[{'id':700,'fileId':70}])
        with self.assertRaises(p.LinkShapeFailure) as caught:p.project_files({'files':[{'unexpected':'synthetic-session'}]},['synthetic-session'])
        self.assertNotIn('synthetic-session',str(caught.exception.shape))

    def test_response_reference_is_not_request_target_but_query_is_bound(self):
        rows=[{'fileId':70,'koppelId':9000}]
        self.assertEqual(p.matches_file(rows,70,8,{'soort':1,'koppelId':8}),rows)
        with self.assertRaisesRegex(p.core.app.Stop,'REQUEST_TARGET_SCOPE'):
            p.matches_file(rows,70,8,{'soort':1,'koppelId':9})

    def test_nested_known_metadata_fields_stop_as_unknown_shape(self):
        for key in ['naam','datum','koppelId','directoryId','scanStatus']:
            with self.assertRaises(p.LinkShapeFailure):
                p.project_files({'files':[{'fileId':70,key:{'unexpected':'nested'}}]},[])

    def test_diagnostic_preserves_uninterpreted_values_before_target_stop(self):
        with tempfile.TemporaryDirectory() as d:
            output=synthetic_output(d,Session.secrets)
            query=lambda n:(Query({'files':[{'fileId':70,'koppelId':9000,'naam':'synthetic-session'}]}),{'soort':1,'koppelId':n})
            result=p.run(Session(),self.item(),query,lambda n:Metadata(),diagnostic_output=output)
            self.assertTrue(result['knownFileFoundInLinkedQuery'])
            files=list(Path(d).glob('link-read-diagnostic-*.json'));self.assertEqual(len(files),1)
            text=files[0].read_text();record=json.loads(text)
            self.assertEqual(record['queryBody'],{'soort':1,'koppelId':8})
            self.assertEqual(record['projectedLinkedFilesMetadata'][0]['koppelId'],9000)
            self.assertEqual(record['sameFileIdCandidatesWithoutTargetClaim'][0]['fileId'],70)
            self.assertFalse(record['targetContractProven']);self.assertNotIn('synthetic-session',text)

    def test_wrong_invoice_stops_before_archive_query(self):
        item=self.item();item['invoiceNumber']='OTHER'
        with self.assertRaisesRegex(p.core.app.Stop,'MUTATION_IDENTITY_MISMATCH'):
            p.run(Session(),item,lambda n:self.fail('No query'),lambda n:self.fail('No metadata'))

    def test_wrong_archive_file_stops_before_link_query(self):
        class Wrong:
            def request(self,*args,**kwargs):return {'id':71,'naam':'Synthetic SYNTH.pdf'}
        with self.assertRaisesRegex(p.core.app.Stop,'ARCHIVE_FILE_IDENTITY_MISMATCH'):
            p.run(Session(),self.item(),lambda n:self.fail('No query'),lambda n:Wrong())


if __name__=='__main__':unittest.main()
