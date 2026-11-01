from private_output import PrivateOutput as _SyntheticOutput

def synthetic_output(root, secrets=()):
    return _SyntheticOutput(root, secrets, path_validator=Path)

import copy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import prepare_edit as p


def records():
    rest={"id":8,"type":1,"date":"2030-08-16","description":"Synthetic source","termOfPayment":0,"ledgerId":10,
          "relationId":20,"inExVat":"IN","invoiceNumber":"SYNTH-INVOICE","entryNumber":"",
          "rows":[{"ledgerId":30,"vatCode":"HOOG_INK_21","vatAmount":21,"costCenterId":40,"amount":121,
                   "description":"Synthetic row","invoiceNumber":"SYNTH-INVOICE","relationId":20}],
          "vat":[{"vatCode":"HOOG_INK_21","amount":21}]}
    app={"id":123456,"mutatieNummer":8,"factuurNummer":"SYNTH-INVOICE","datum":"2030-08-16T00:00:00",
         "bedrag":0,"mutatieRegels":[{"bedrag":121,"btw":0,"bedragInclusief":121,"bedragExclusief":121}]}
    manifest={"mutationNumber":8,"knownDate":"2030-08-16","requestedChanges":[],"ownerPatchApproved":False}
    return rest,app,manifest


class Checks(unittest.TestCase):
    def test_zero_app_calculations_never_become_put_or_financial_truth(self):
        rest,app,manifest=records();plan=p.make_plan(rest,app,manifest,'synthetic',{})
        self.assertIsNone(plan['putPayload']);self.assertFalse(plan['applyEnabled'])
        self.assertEqual(plan['intendedRestState']['vat'][0]['amount'],21)
        self.assertEqual(plan['intendedRestState']['rows'][0]['costCenterId'],40)
        self.assertEqual(plan['appIdMapping']['appInternalId'],123456)
        self.assertEqual(plan['baseline'],rest)

    def test_wrong_visible_number_invoice_or_date_rejected(self):
        rest,app,manifest=records()
        for key,value in [('mutatieNummer',9),('factuurNummer','OTHER'),('datum','2030-08-17T00:00:00')]:
            wrong=copy.deepcopy(app);wrong[key]=value
            with self.assertRaisesRegex(p.app.app.Stop,'ID_MAPPING_MISMATCH'):p.identity_mapping(rest,wrong)

    def test_synthetic_descriptive_patch_preserves_every_other_field(self):
        rest,app,manifest=records()
        manifest['requestedChanges']=[{'path':'/description','before':'Synthetic source','after':'Synthetic edited'}]
        plan=p.make_plan(rest,app,manifest,'synthetic-not-owner-authority',{})
        self.assertEqual(plan['fieldDiff'],[{'path':'/description','before':'Synthetic source','after':'Synthetic edited'}])
        self.assertEqual(plan['intendedRestState']['rows'],rest['rows'])
        self.assertFalse(plan['applyEnabled'])
        actual=copy.deepcopy(plan['intendedRestState']);actual['rows'][0]['vatAmount']=0
        self.assertEqual(p.verify_state(plan,actual)['state'],'REST_POSTSTATE_MISMATCH_STOP')

    def test_stale_baseline_stops_not_overwritten(self):
        rest,app,manifest=records();changed=copy.deepcopy(rest);changed['termOfPayment']=14
        with self.assertRaisesRegex(p.app.app.Stop,'BASELINE_CHANGED'):p.optimistic_check(rest,changed)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(p.app.app.Stop):p.capture(manifest,lambda:rest,lambda:app,lambda:changed,synthetic_output(d))
            self.assertEqual(len(list(Path(d).glob('edit-rest-baseline-*.json'))),1)

    def test_apply_disabled_before_any_network_or_secret_and_no_uncertain_replay(self):
        with patch.object(p,'compose_reader',side_effect=AssertionError('No network')):
            with self.assertRaisesRegex(p.app.app.Stop,'APPLY_DISABLED'):p.deny_apply()
        self.assertFalse(p.app.request_allowed('PUT','/api/v4/mutaties',{}))
        # No PUT exists: uncertain write/retry behavior is NOT claimed implemented.

    def test_unsupported_money_patch_or_stale_before_rejected(self):
        rest,app,manifest=records()
        with self.assertRaisesRegex(p.app.app.Stop,'DESCRIPTION_ONLY'):
            p.intended_state(rest,[{'path':'/rows/0/amount','before':121,'after':0}])
        with self.assertRaisesRegex(p.app.app.Stop,'BASELINE_OR_VALUE'):
            p.intended_state(rest,[{'path':'/description','before':'Wrong','after':'New'}])

    def test_selected_rest_snapshot_redaction_and_private_writer(self):
        rest,app,manifest=records();rest['description']='synthetic-session-secret'
        clean=p.base.redact(p.project_rest(rest,8),['synthetic-session-secret'])
        with tempfile.TemporaryDirectory() as d:
            out=synthetic_output(d,['synthetic-session-secret'])
            file=out.save('test',{'baseline':clean,'token':'not-persisted','note':'synthetic-session-secret'})
            text=file.read_text();self.assertNotIn('synthetic-session-secret',text);self.assertNotIn('not-persisted',text)


if __name__=='__main__':unittest.main()
