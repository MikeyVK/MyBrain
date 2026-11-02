"""Meaningful offline tests through the public hours-plan/operation interfaces."""
from contextlib import nullcontext
from dataclasses import FrozenInstanceError, replace
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from uuid import uuid4
from hours_domain import (HourSnapshot, HoursError, HoursExecutor, HoursReconciler, HoursPlan,
                          canonical, cleanup_plan, prepare_create, prepare_edit)
from hours_io import AppContext, HttpResult, OneShotHoursCommand, SharedWire, SharedEventWriter

ADMIN = 800100
MARKER = "SYNTHETIC-HOURS-TEST-MARKER"
REQUEST = {"datum": "2030-10-31", "medewerkerId": 800101, "projectId": 800102,
           "activiteitId": 800103, "aantalUren": "0.01", "aantalKilometers": None,
           "opmerkingen": MARKER}
CONTRACT = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


def create(**overrides):
    options = dict(operation_id=str(uuid4()), administration_id=ADMIN, source_key=str(uuid4()),
                   contract_sha256=CONTRACT, marker=MARKER, synthetic_pilot=True)
    options.update(overrides)
    return prepare_create(REQUEST, **options)


class MemoryEvents:
    def __init__(self): self.rows = []
    def events(self): return tuple(dict(x) for x in self.rows)
    def append(self, event): self.rows.append(dict(event))


class Guard:
    def __init__(self, actual=ADMIN): self.actual = actual
    def confirm(self, expected):
        if self.actual != expected: raise HoursError("ADMINISTRATION_MISMATCH")


class NoContention:
    def acquire(self): return nullcontext()


class MemoryHours:
    def __init__(self): self.records = {}; self.reads = 0
    def read_hour(self, identifier):
        self.reads += 1
        return self.records.get(identifier)
    def find_marker(self, marker, day):
        return tuple(x for x in self.records.values() if marker in x.data().get("opmerkingen", "") and x.data()["datum"][:10] == day)


class SimulatedCommand:
    def __init__(self, reader): self.reader = reader; self.calls = []; self.fail_after_write = False; self.wrong_saved_hours = False
    def send(self, plan):
        self.calls.append((plan.method, plan.path, plan.payload()))
        identifier = 900001 if plan.kind == "create" else plan.expected()["id"]
        if plan.kind == "cleanup": self.reader.records.pop(identifier, None)
        else:
            value = {k: v for k, v in plan.expected().items() if v is not None}
            value["id"] = identifier
            if self.wrong_saved_hours: value["aantalUren"] = 4.0
            self.reader.records[identifier] = HourSnapshot.capture(value)
        if self.fail_after_write: raise TimeoutError("SIMULATED_LOST_RESPONSE")
        return {"id": identifier}


class Plans(unittest.TestCase):
    def test_create_exact_date_ids_wire_and_null_omission(self):
        p = create()
        self.assertEqual((p.method, p.path), ("POST", "/api/v4/uren"))
        self.assertEqual(p.payload()["datum"], "2030-10-31T00:00:00Z")
        self.assertEqual(p.payload()["id"], 0)
        self.assertEqual(p.payload()["$id"], "1")
        self.assertNotIn("aantalKilometers", p.payload())
        self.assertIsNone(p.expected()["aantalKilometers"])
    def test_explicit_zero_and_empty_text_are_not_omitted(self):
        p = prepare_create({**REQUEST, "aantalUren": 0, "aantalKilometers": 0, "opmerkingen": ""},
                operation_id=str(uuid4()), administration_id=ADMIN, source_key="zero-case", contract_sha256=CONTRACT)
        self.assertEqual(p.payload()["aantalUren"], 0.0)
        self.assertEqual(p.payload()["aantalKilometers"], 0.0)
        self.assertEqual(p.payload()["opmerkingen"], "")
    def test_dates_reject_invalid_or_timezone_shift_inputs(self):
        for value in ["2030-02-30", "2030-10-31T23:00:00-01:00", "31-10-2030"]:
            with self.subTest(value=value), self.assertRaises(HoursError):
                prepare_create({**REQUEST, "datum": value}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="bad-date", contract_sha256=CONTRACT)
    def test_ids_are_int32_and_never_boolean(self):
        for value in [True, 0, -1, 2147483648, 800101.0]:
            with self.subTest(value=value), self.assertRaises(HoursError):
                prepare_create({**REQUEST, "medewerkerId": value}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="bad-id", contract_sha256=CONTRACT)
    def test_extra_precision_and_nonfinite_numbers_rejected(self):
        for value in ["0.001", float("nan"), float("inf"), True, "800104.01"]:
            with self.subTest(value=str(value)), self.assertRaises(HoursError):
                prepare_create({**REQUEST, "aantalUren": value}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="bad-number", contract_sha256=CONTRACT)
    def test_edit_preserves_metadata_empty_zero_and_raw_date(self):
        data = {**create().expected(), "id": 41, "aantalKilometers": 0, "medewerker": "Synthetic", "project": "", "activiteit": None, "invoerDatum": "2030-10-01T13:14:15Z"}
        data["datum"] = "2030-10-31T00:00:00"
        p = prepare_edit(HourSnapshot.capture(data), {"aantalUren": "0.02"}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="edit", contract_sha256=CONTRACT)
        self.assertEqual(p.payload()["datum"], data["datum"])
        for field in ["id", "medewerkerId", "projectId", "activiteitId", "medewerker", "project", "invoerDatum", "aantalKilometers"]:
            self.assertEqual(p.payload()[field], data[field])
        self.assertIn("activiteit", p.expected())
        self.assertNotIn("activiteit", p.payload())
    def test_unknown_baseline_fields_fail_instead_of_being_lost(self):
        before = HourSnapshot.capture({**create().expected(), "id": 41, "futureServerProperty": "retain-me"})
        with self.assertRaisesRegex(HoursError, "UNKNOWN_HOURS_FIELDS"):
            prepare_edit(before, {"aantalUren": 1}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="edit", contract_sha256=CONTRACT)
        self.assertEqual(before.data()["futureServerProperty"], "retain-me")
    def test_loaded_plan_cannot_send_a_different_payload(self):
        p = create(); doc = p.document();doc["payload_json"] = canonical({**p.payload(), "aantalUren": 99})
        with self.assertRaisesRegex(HoursError, "PAYLOAD_EXPECTATION_MISMATCH"):
            HoursPlan(**doc)
    def test_edit_cannot_change_immutable_invoice_metadata(self):
        before = HourSnapshot.capture({**create().expected(), "id": 41, "invoerDatum": "original"})
        p = prepare_edit(before, {"aantalUren": 1}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="edit", contract_sha256=CONTRACT)
        expected = {**p.expected(), "invoerDatum": "overwritten"}
        from hours_domain import wire_payload
        with self.assertRaisesRegex(HoursError, "IMMUTABLE_METADATA_CHANGED"):
            replace(p, expected_json=canonical(expected), payload_json=canonical(wire_payload(expected)))
    def test_snapshot_and_plan_are_immutable_and_hash_bound(self):
        p = create()
        with self.assertRaises(FrozenInstanceError): p.kind = "edit"
        with self.assertRaisesRegex(HoursError, "PLAN_HASH_MISMATCH"):
            HoursPlan.load(p.document(), "0" * 64)
        self.assertEqual(HoursPlan.load(p.document(), p.digest), p)


class Workflow(unittest.TestCase):
    def setUp(self):
        self.rows = MemoryHours();self.command = SimulatedCommand(self.rows);self.events = MemoryEvents();self.guard = Guard()
        self.executor = HoursExecutor(self.rows, self.command, self.guard, self.events, self.events, NoContention())
    def test_one_create_edit_owned_cleanup_round_trip(self):
        p = create();self.executor.apply(p)
        before = self.rows.read_hour(900001)
        edit = prepare_edit(before, {"aantalUren": .02, "aantalKilometers": 1.25, "opmerkingen": MARKER + " edited"}, operation_id=str(uuid4()), administration_id=ADMIN, source_key="edit", contract_sha256=CONTRACT, marker=MARKER, owner_operation_id=p.operation_id, synthetic_pilot=True)
        self.executor.apply(edit)
        cleanup = cleanup_plan(p.operation_id, edit.operation_id, self.events.events(), operation_id=str(uuid4()), administration_id=ADMIN, contract_sha256=CONTRACT)
        self.executor.apply(cleanup)
        self.assertIsNone(self.rows.read_hour(900001))
        self.assertEqual([c[:2] for c in self.command.calls], [("POST", "/api/v4/uren"), ("PUT", "/api/v4/uren"), ("DELETE", "/api/v4/uren/900001")])
        self.assertEqual([e["status"] for e in self.events.events()].count("VERIFIED"), 3)
    def test_admin_mismatch_stops_before_intent_or_command(self):
        self.guard.actual = 12
        with self.assertRaisesRegex(HoursError, "ADMINISTRATION_MISMATCH"): self.executor.apply(create())
        self.assertEqual(self.command.calls, []);self.assertEqual(self.events.events(), ())
    def test_stale_baseline_stops_before_edit(self):
        p=create();self.executor.apply(p);before=self.rows.read_hour(900001)
        edit=prepare_edit(before,{"aantalUren": .02},operation_id=str(uuid4()),administration_id=ADMIN,source_key="edit",contract_sha256=CONTRACT)
        self.rows.records[900001]=HourSnapshot.capture({**before.data(),"opmerkingen":"changed elsewhere"})
        with self.assertRaisesRegex(HoursError,"STALE_BASELINE"):self.executor.apply(edit)
        self.assertEqual(len(self.command.calls),1)
    def test_lost_response_never_retries_and_reconciliation_reads_only(self):
        p=create();self.command.fail_after_write=True
        with self.assertRaises(TimeoutError):self.executor.apply(p)
        self.assertEqual([x['status'] for x in self.events.events()],['PENDING','UNCERTAIN'])
        with self.assertRaisesRegex(HoursError,'OPERATION_ALREADY_ATTEMPTED'):self.executor.apply(p)
        result=HoursReconciler(self.rows,self.guard,self.events).reconcile(p)
        self.assertEqual(result.data()['status'],'MATCHES_EXPECTED');self.assertEqual(len(self.command.calls),1)
        self.assertEqual(len(self.events.events()),2)
        self.executor.record_reconciliation(p,result)
        self.assertEqual(self.events.events()[-1]['status'],'RECONCILED_VERIFIED')
        cleanup=cleanup_plan(p.operation_id,p.operation_id,self.events.events(),operation_id=str(uuid4()),administration_id=ADMIN,contract_sha256=CONTRACT)
        self.command.fail_after_write=False;self.executor.apply(cleanup)
        self.assertIsNone(self.rows.read_hour(900001))
    def test_success_ack_does_not_hide_wrong_saved_values(self):
        self.command.wrong_saved_hours=True
        with self.assertRaisesRegex(HoursError,'READBACK_FIELD_MISMATCH'):self.executor.apply(create())
        self.assertEqual(self.events.events()[-1]['status'],'UNCERTAIN')
        self.assertNotIn('VERIFIED',[x['status'] for x in self.events.events()])
    def test_source_key_blocks_a_new_operation_retry(self):
        p=create(source_key='same-source');self.executor.apply(p)
        with self.assertRaisesRegex(HoursError,'CREATE_SOURCE_ALREADY_ATTEMPTED'):self.executor.apply(create(source_key='same-source'))
        self.assertEqual(len(self.command.calls),1)
    def test_duplicate_remote_marker_blocks_creation(self):
        self.rows.records[10]=HourSnapshot.capture({**create().expected(),'id':10})
        with self.assertRaisesRegex(HoursError,'REMOTE_MARKER_ALREADY_EXISTS'):self.executor.apply(create())
        self.assertEqual(self.command.calls,[])
    def test_cleanup_cannot_target_an_unrelated_existing_record(self):
        p=create();self.executor.apply(p)
        cleanup=cleanup_plan(p.operation_id,p.operation_id,self.events.events(),operation_id=str(uuid4()),administration_id=ADMIN,contract_sha256=CONTRACT)
        other={**cleanup.expected(),'id':10};self.rows.records[10]=HourSnapshot.capture(other)
        forged=replace(cleanup,expected_json=canonical(other),baseline_json=canonical(other))
        with self.assertRaisesRegex(HoursError,'CLEANUP_NOT_OWNED_PILOT'):self.executor.apply(forged)
        self.assertIsNotNone(self.rows.read_hour(10));self.assertEqual(len(self.command.calls),1)
    def test_real_create_receipt_cannot_authorize_test_cleanup(self):
        p=create(synthetic_pilot=False);self.executor.apply(p)
        with self.assertRaisesRegex(HoursError,'OWNED_PILOT_RECEIPT_REQUIRED'):
            cleanup_plan(p.operation_id,p.operation_id,self.events.events(),operation_id=str(uuid4()),administration_id=ADMIN,contract_sha256=CONTRACT)
    def test_pending_is_durable_before_first_command(self):
        original=self.command.send
        def send(plan):
            self.assertEqual(self.events.events()[-1]['status'],'PENDING')
            return original(plan)
        self.command.send=send;self.executor.apply(create())


class AdapterAcks(unittest.TestCase):
    def test_false_or_error_ack_is_never_success(self):
        from types import SimpleNamespace
        p=create()
        class Wire:
            def __init__(self,value):self.value=value
            def call(self,*args,**kwargs):return HttpResult(200,canonical(self.value))
        for value in [False, {'success':False},{'success':0},{'error':{'message':'failure'}},{'errors':['failure']},{'errorType':'validation'}]:
            with self.subTest(value=value),self.assertRaises(HoursError):
                OneShotHoursCommand(Wire(value),SimpleNamespace(token='synthetic')).send(p)
    def test_204_ack_is_allowed_but_itself_does_not_verify_storage(self):
        from types import SimpleNamespace
        p=create();before=HourSnapshot.capture({**p.expected(),'id':41})
        edit=prepare_edit(before,{'aantalUren':.02},operation_id=str(uuid4()),administration_id=ADMIN,source_key='edit',contract_sha256=CONTRACT)
        class Wire:
            def call(self,*args,**kwargs):return HttpResult(204,'null')
        self.assertIsNone(OneShotHoursCommand(Wire(),SimpleNamespace(token='synthetic')).send(edit))
    def test_shared_logging_redacts_token_and_known_secret_values(self):
        from private_output import PrivateOutput as _PrivateOutput
        def PrivateOutput(root, secrets=()):
            return _PrivateOutput(root, secrets, path_validator=Path)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'journal.jsonl';writer=SharedEventWriter(path,PrivateOutput(folder,('synthetic-secret',)))
            writer.append({'token':'not-for-output','diagnostic':'synthetic-secret'})
            value=path.read_text(encoding='utf-8')
            self.assertNotIn('synthetic-secret',value);self.assertNotIn('not-for-output',value);self.assertIn('[REDACTED]',value)

class QAR2Safety(unittest.TestCase):
    setUp = Workflow.setUp

    def target_plan(self, kind):
        owner = create(); self.executor.apply(owner)
        before = self.rows.read_hour(900001)
        if kind == "edit":
            plan = prepare_edit(before, {"aantalUren": .02}, operation_id=str(uuid4()),
                administration_id=ADMIN, source_key="edit-original", contract_sha256=CONTRACT,
                marker=MARKER, owner_operation_id=owner.operation_id, synthetic_pilot=True)
        else:
            plan = cleanup_plan(owner.operation_id, owner.operation_id, self.events.events(),
                operation_id=str(uuid4()), administration_id=ADMIN, contract_sha256=CONTRACT)
        return owner, plan

    def fail_before_write(self, plan):
        original = self.command.send
        def fail(value):
            self.command.calls.append((value.method, value.path, value.payload()))
            raise TimeoutError("SIMULATED_UNCERTAIN_BEFORE_WRITE")
        self.command.send = fail
        try:
            with self.assertRaises(TimeoutError): self.executor.apply(plan)
        finally:
            self.command.send = original

    def test_uncertain_edit_or_cleanup_new_ids_and_source_keys_cannot_retry(self):
        for kind in ("edit", "cleanup"):
            with self.subTest(kind=kind):
                self.setUp(); owner, plan = self.target_plan(kind); self.fail_before_write(plan)
                before_events = self.events.events(); before_calls = len(self.command.calls)
                replacement = replace(plan, operation_id=str(uuid4()), source_key="different-caller-key")
                with self.assertRaisesRegex(HoursError, "UNRESOLVED_TARGET_OPERATION"):
                    self.executor.apply(replacement)
                self.assertEqual(self.events.events(), before_events)
                self.assertEqual(len(self.command.calls), before_calls)

    def test_uncertain_edit_and_cleanup_block_each_others_followup(self):
        for kind in ("edit", "cleanup"):
            with self.subTest(kind=kind):
                self.setUp(); owner, plan = self.target_plan(kind); self.fail_before_write(plan)
                if kind == "edit":
                    next_plan = cleanup_plan(owner.operation_id, owner.operation_id, self.events.events(),
                        operation_id=str(uuid4()), administration_id=ADMIN, contract_sha256=CONTRACT)
                else:
                    next_plan = prepare_edit(self.rows.read_hour(900001), {"aantalUren": .03},
                        operation_id=str(uuid4()), administration_id=ADMIN, source_key="different-edit",
                        contract_sha256=CONTRACT)
                count = len(self.command.calls); journal = self.events.events()
                with self.assertRaisesRegex(HoursError, "UNRESOLVED_TARGET_OPERATION"):
                    self.executor.apply(next_plan)
                self.assertEqual(count, len(self.command.calls)); self.assertEqual(journal, self.events.events())

    def test_read_only_reconcile_does_not_release_edit_until_explicit_record(self):
        owner, plan = self.target_plan("edit"); self.command.fail_after_write = True
        with self.assertRaises(TimeoutError): self.executor.apply(plan)
        self.command.fail_after_write = False
        result = HoursReconciler(self.rows, self.guard, self.events).reconcile(plan)
        next_plan = prepare_edit(self.rows.read_hour(900001), {"aantalUren": .03},
            operation_id=str(uuid4()), administration_id=ADMIN, source_key="next-intent", contract_sha256=CONTRACT)
        before_calls = len(self.command.calls); journal = self.events.events()
        with self.assertRaisesRegex(HoursError, "UNRESOLVED_TARGET_OPERATION"): self.executor.apply(next_plan)
        self.assertEqual(before_calls, len(self.command.calls)); self.assertEqual(journal, self.events.events())
        self.executor.record_reconciliation(plan, result)
        self.executor.apply(next_plan)
        self.assertEqual(self.rows.read_hour(900001).data()["aantalUren"], .03)
        self.assertEqual(len(self.command.calls), before_calls + 1)

    def test_successful_cleanup_reconciliation_releases_gate_but_absent_baseline_still_stops(self):
        owner, plan = self.target_plan("cleanup"); self.command.fail_after_write = True
        with self.assertRaises(TimeoutError): self.executor.apply(plan)
        self.command.fail_after_write = False
        result = HoursReconciler(self.rows, self.guard, self.events).reconcile(plan)
        next_plan = replace(plan, operation_id=str(uuid4()), source_key="cleanup-new-key")
        count = len(self.command.calls); journal = self.events.events()
        with self.assertRaisesRegex(HoursError, "UNRESOLVED_TARGET_OPERATION"): self.executor.apply(next_plan)
        self.assertEqual(journal, self.events.events())
        self.executor.record_reconciliation(plan, result)
        with self.assertRaisesRegex(HoursError, "STALE_BASELINE"): self.executor.apply(next_plan)
        self.assertEqual(len(self.command.calls), count)
        self.assertEqual(self.events.events()[-1]["status"], "RECONCILED_VERIFIED")

    def test_unresolved_reconciliation_never_releases_target(self):
        from hours_domain import ReconciliationResult
        for kind in ("edit", "cleanup"):
            with self.subTest(kind=kind):
                self.setUp(); _, plan = self.target_plan(kind); self.fail_before_write(plan)
                result = HoursReconciler(self.rows, self.guard, self.events)
                if kind == "cleanup":
                    unresolved = result.reconcile(plan)
                    self.assertEqual(unresolved.data()["status"], "UNRESOLVED")
                else:
                    with self.assertRaisesRegex(HoursError, "READBACK_FIELD_MISMATCH"): result.reconcile(plan)
                    unresolved = ReconciliationResult(canonical({"status":"UNRESOLVED", "planHash":plan.digest, "targetId":900001}))
                count = len(self.command.calls); journal = self.events.events()
                with self.assertRaisesRegex(HoursError, "RECONCILIATION_NOT_VERIFIED"):
                    self.executor.record_reconciliation(plan, unresolved)
                with self.assertRaisesRegex(HoursError, "UNRESOLVED_TARGET_OPERATION"):
                    self.executor.apply(replace(plan, operation_id=str(uuid4())))
                self.assertEqual(len(self.command.calls), count); self.assertEqual(journal, self.events.events())

    def test_reconciliation_rejects_foreign_or_non_int32_target_before_get_or_receipt(self):
        from hours_domain import ReconciliationResult
        for kind in ("edit", "cleanup"):
            for target in (900002, True, 900001.0, 0, 2147483648):
                with self.subTest(kind=kind, target=target):
                    self.setUp(); _, plan = self.target_plan(kind); self.fail_before_write(plan)
                    result = ReconciliationResult(canonical({"status":"MATCHES_EXPECTED", "planHash":plan.digest, "targetId":target}))
                    reads = self.rows.reads; journal = self.events.events()
                    with self.assertRaises(HoursError): self.executor.record_reconciliation(plan, result)
                    self.assertEqual(self.rows.reads, reads); self.assertEqual(self.events.events(), journal)
                    self.assertIsNotNone(self.rows.records.get(900001))

    def test_forged_journal_target_cannot_confirm_edit_or_cleanup(self):
        from hours_domain import ReconciliationResult
        for kind in ("edit", "cleanup"):
            with self.subTest(kind=kind):
                self.setUp(); _, plan = self.target_plan(kind); self.fail_before_write(plan)
                self.events.rows[-1]["targetId"] = 900002
                result = ReconciliationResult(canonical({"status":"MATCHES_EXPECTED", "planHash":plan.digest, "targetId":900001}))
                reads = self.rows.reads; journal = self.events.events()
                with self.assertRaisesRegex(HoursError, "JOURNAL_TARGET_MISMATCH"):
                    self.executor.record_reconciliation(plan, result)
                with self.assertRaisesRegex(HoursError, "JOURNAL_TARGET_MISMATCH"):
                    HoursReconciler(self.rows, self.guard, self.events).reconcile(plan)
                self.assertEqual(reads, self.rows.reads); self.assertEqual(journal, self.events.events())

    def test_forged_pending_plan_or_receipt_binding_stops_before_get(self):
        from hours_domain import ReconciliationResult
        for kind in ("edit", "cleanup"):
            for forged_part in ("pending-plan", "receipt-planhash", "receipt-admin"):
                with self.subTest(kind=kind, forged_part=forged_part):
                    self.setUp(); _, plan = self.target_plan(kind); self.fail_before_write(plan)
                    if forged_part == "pending-plan":
                        pending = next(x for x in self.events.rows if x.get("operationId") == plan.operation_id and x["status"] == "PENDING")
                        pending["plan"] = {**pending["plan"], "source_key":"forged"}
                    elif forged_part == "receipt-planhash": self.events.rows[-1]["planHash"] = "0" * 64
                    else: self.events.rows[-1]["administrationId"] = 999
                    result = ReconciliationResult(canonical({"status":"MATCHES_EXPECTED", "planHash":plan.digest, "targetId":900001}))
                    reads = self.rows.reads; journal = self.events.events()
                    with self.assertRaisesRegex(HoursError, "JOURNAL_PLAN_MISMATCH"):
                        self.executor.record_reconciliation(plan, result)
                    self.assertEqual(reads, self.rows.reads); self.assertEqual(journal, self.events.events())

    def test_type_confused_wire_values_are_rejected_before_any_io(self):
        from hours_domain import fingerprint
        p = prepare_create({**REQUEST, "aantalUren":1}, operation_id=str(uuid4()),
            administration_id=ADMIN, source_key="typed-wire", contract_sha256=CONTRACT)
        for field, value in (("aantalUren", True), ("aantalUren", 1), ("aantalUren", "1.0"),
                             ("id", False), ("medewerkerId", 800101.0)):
            with self.subTest(field=field, value=value):
                doc = {**p.document(), "payload_json":canonical({**p.payload(), field:value})}
                with self.assertRaises(HoursError): HoursPlan.load(doc, fingerprint(doc))
        self.assertEqual(self.command.calls, []); self.assertEqual(self.events.events(), ())


if __name__=='__main__':unittest.main()
