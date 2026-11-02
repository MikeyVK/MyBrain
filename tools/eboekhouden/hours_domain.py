"""Pure hours plans and guarded orchestration; no host/auth/import side effects."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
import re
from typing import Any, Mapping, Protocol, ContextManager
from uuid import UUID

DTO_FIELDS = frozenset(("id", "datum", "medewerkerId", "projectId", "activiteitId", "aantalUren", "aantalKilometers", "opmerkingen", "medewerker", "project", "activiteit", "invoerDatum"))
EDIT_FIELDS = frozenset(("datum", "medewerkerId", "projectId", "activiteitId", "aantalUren", "aantalKilometers", "opmerkingen"))
ID_FIELDS = frozenset(("medewerkerId", "projectId", "activiteitId"))
NUMBER_FIELDS = frozenset(("aantalUren", "aantalKilometers"))
NULLABLE_FIELDS = frozenset(("datum", "aantalUren", "aantalKilometers", "opmerkingen", "medewerker", "project", "activiteit", "invoerDatum"))
HOURS_PATH = "/api/v4/uren"
FILTER_PATH = HOURS_PATH + "/filter"
METHODS = {"create": "POST", "edit": "PUT", "cleanup": "DELETE"}
VERIFIED_STATUSES = frozenset(("VERIFIED", "RECONCILED_VERIFIED"))

class HoursError(ValueError):
    def __init__(self, code: str, facts: Mapping[str, Any] | None = None):
        super().__init__(code)
        self.code = code
        self.facts = dict(facts or {})


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def positive_id(value: Any) -> int:
    if type(value) is not int or not 1 <= value <= 2147483647:
        raise HoursError("POSITIVE_INT32_ID_REQUIRED")
    return value


def work_date(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise HoursError("CALENDAR_DATE_REQUIRED")
    try:
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError()
    except ValueError as exc:
        raise HoursError("CALENDAR_DATE_REQUIRED") from exc
    return value


def record_date(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:T00:00:00(?:\.0+)?(?:Z|\+00:00)?)?", value):
        raise HoursError("NON_CALENDAR_RECORD_DATE", {"value": value})
    return work_date(value[:10])


def input_number(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise HoursError("HOURS_NUMBER_INVALID")
    try:
        number = Decimal(str(value))
        if not number.is_finite() or abs(number) > Decimal("100000") or number != number.quantize(Decimal("0.01")):
            raise ValueError()
    except (InvalidOperation, ValueError) as exc:
        raise HoursError("HOURS_NUMBER_INVALID") from exc
    return float(number)


def validate_payload(value: Mapping[str, Any], *, new: bool) -> dict[str, Any]:
    unknown = set(value) - DTO_FIELDS - {"$id"}
    if unknown:
        raise HoursError("UNKNOWN_HOURS_FIELDS", {"fields": sorted(unknown)})
    result = dict(value)
    if new:
        if type(result.get("id", 0)) is not int or result.get("id", 0) != 0:
            raise HoursError("CREATE_ID_MUST_BE_ZERO")
        result["id"] = 0
    else:
        positive_id(result.get("id"))
    for field in ID_FIELDS:
        positive_id(result.get(field))
    record_date(result.get("datum"))
    for field in NUMBER_FIELDS:
        if field in result:
            result[field] = input_number(result[field])
    if result.get("aantalUren") is None and result.get("aantalKilometers") is None:
        raise HoursError("HOURS_OR_KILOMETRES_REQUIRED")
    for field in ("opmerkingen", "medewerker", "project", "activiteit", "invoerDatum"):
        if field in result and result[field] is not None and not isinstance(result[field], str):
            raise HoursError("HOURS_TEXT_INVALID", {"field": field})
    if result.get("opmerkingen") is not None and len(result["opmerkingen"]) > 3000000:
        raise HoursError("REMARKS_EXCEED_CLIENT_BOUND")
    result.pop("$id", None)
    return result


@dataclass(frozen=True)
class HourSnapshot:
    raw_json: str

    @classmethod
    def capture(cls, value: Mapping[str, Any]) -> HourSnapshot:
        positive_id(value.get("id"))
        return cls(canonical(dict(value)))

    def data(self) -> dict[str, Any]:
        return json.loads(self.raw_json)

    @property
    def digest(self) -> str:
        return fingerprint(self.data())


@dataclass(frozen=True)
class HoursPlan:
    operation_id: str
    kind: str
    administration_id: int
    source_key: str
    contract_sha256: str
    payload_json: str
    expected_json: str
    baseline_json: str | None
    marker: str | None = None
    owner_operation_id: str | None = None
    synthetic_pilot: bool = False

    def __post_init__(self) -> None:
        if str(UUID(self.operation_id)) != self.operation_id or self.kind not in METHODS:
            raise HoursError("PLAN_ID_OR_KIND_INVALID")
        positive_id(self.administration_id)
        if not self.source_key or len(self.source_key) > 160 or any(ord(c) < 32 for c in self.source_key):
            raise HoursError("PLAN_SOURCE_KEY_INVALID")
        if not re.fullmatch(r"[0-9a-f]{64}", self.contract_sha256):
            raise HoursError("CONTRACT_HASH_INVALID")
        expected = self.expected()
        if type(self.synthetic_pilot) is not bool or (self.synthetic_pilot and not self.marker):
            raise HoursError("PILOT_FLAG_INVALID")
        if self.kind == "cleanup":
            positive_id(expected.get("id"))
            if not self.owner_operation_id or not self.marker or not self.synthetic_pilot:
                raise HoursError("CLEANUP_OWNERSHIP_REQUIRED")
        else:
            normalised = validate_payload(expected, new=self.kind == "create")
            if canonical(normalised) != canonical(expected):
                raise HoursError("EXPECTED_STATE_NOT_CANONICAL")
        if self.marker is not None and (not self.marker or self.marker not in str(expected.get("opmerkingen", ""))):
            raise HoursError("OPERATION_MARKER_MISSING")
        if self.kind in ("edit", "cleanup") and self.baseline_json is None:
            raise HoursError("BASELINE_REQUIRED")
        wanted_wire = {} if self.kind == "cleanup" else wire_payload(expected)
        if self.kind != "cleanup":
            validate_payload(self.payload(), new=self.kind == "create")
        if canonical(self.payload()) != canonical(wanted_wire):
            raise HoursError("PAYLOAD_EXPECTATION_MISMATCH")
        if self.baseline_json is not None:
            baseline = validate_payload(json.loads(self.baseline_json), new=False)
            if baseline["id"] != expected["id"]:
                raise HoursError("BASELINE_ID_MISMATCH")
            if any(baseline.get(k) != expected.get(k) for k in DTO_FIELDS - EDIT_FIELDS):
                raise HoursError("IMMUTABLE_METADATA_CHANGED")

    def payload(self) -> dict[str, Any]:
        return json.loads(self.payload_json)

    def expected(self) -> dict[str, Any]:
        return json.loads(self.expected_json)

    def document(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.__dataclass_fields__}

    @property
    def digest(self) -> str:
        return fingerprint(self.document())

    @property
    def method(self) -> str:
        return METHODS[self.kind]

    @property
    def path(self) -> str:
        return HOURS_PATH + "/" + str(self.expected()["id"]) if self.kind == "cleanup" else HOURS_PATH

    @classmethod
    def load(cls, value: Mapping[str, Any], expected_digest: str) -> HoursPlan:
        plan = cls(**dict(value))
        if plan.digest != expected_digest:
            raise HoursError("PLAN_HASH_MISMATCH")
        return plan


def wire_payload(expected: Mapping[str, Any]) -> dict[str, Any]:
    # Match explicit nullable omission; preserve zero and empty text. Reference
    # metadata follows the inspected Json.NET PreserveReferencesHandling.Objects.
    result = {k: v for k, v in expected.items() if v is not None}
    return {"$id": "1", **result}


def prepare_create(value: Mapping[str, Any], *, operation_id: str, administration_id: int,
                   source_key: str, contract_sha256: str, marker: str | None = None,
                   synthetic_pilot: bool = False) -> HoursPlan:
    if set(value) - EDIT_FIELDS - {"id"}:
        raise HoursError("CREATE_INPUT_FIELDS_INVALID")
    expected = dict(value)
    expected["datum"] = work_date(expected.get("datum")) + "T00:00:00Z"
    expected = validate_payload(expected, new=True)
    return HoursPlan(operation_id, "create", administration_id, source_key, contract_sha256,
                     canonical(wire_payload(expected)), canonical(expected), None, marker,
                     None, synthetic_pilot)


def prepare_edit(before: HourSnapshot, changes: Mapping[str, Any], *, operation_id: str,
                 administration_id: int, source_key: str, contract_sha256: str,
                 marker: str | None = None, owner_operation_id: str | None = None,
                 synthetic_pilot: bool = False) -> HoursPlan:
    if not changes or set(changes) - EDIT_FIELDS:
        raise HoursError("EDIT_FIELDS_INVALID")
    expected = validate_payload(before.data(), new=False)
    patch = dict(changes)
    if "datum" in patch:
        patch["datum"] = work_date(patch["datum"]) + "T00:00:00Z"
    expected.update(patch)
    expected = validate_payload(expected, new=False)
    return HoursPlan(operation_id, "edit", administration_id, source_key, contract_sha256,
                     canonical(wire_payload(expected)), canonical(expected), before.raw_json,
                     marker, owner_operation_id, synthetic_pilot)


def verify_saved(plan: HoursPlan, after: HourSnapshot, target_id: int) -> None:
    actual = after.data()
    unknown = set(actual) - DTO_FIELDS - {"$id"}
    if unknown:
        raise HoursError("UNEXPECTED_READBACK_FIELDS", {"fields": sorted(unknown)})
    if actual.get("id") != positive_id(target_id):
        raise HoursError("READBACK_ID_MISMATCH")
    expected = plan.expected()
    for field in DTO_FIELDS - {"id"}:
        if field not in expected and field not in NUMBER_FIELDS:
            continue
        left, right = expected.get(field), actual.get(field)
        if field == "datum":
            same = record_date(left) == record_date(right)
        elif field in NUMBER_FIELDS:
            same = (left is None and right is None) or (left is not None and right is not None and input_number(left) == input_number(right))
        else:
            same = left == right
        if not same:
            raise HoursError("READBACK_FIELD_MISMATCH", {"field": field, "expected": left, "actual": right})


@dataclass(frozen=True)
class ReconciliationResult:
    raw_json: str

    def data(self) -> dict[str, Any]:
        return json.loads(self.raw_json)


class HoursReader(Protocol):
    def read_hour(self, identifier: int) -> HourSnapshot | None: ...
    def find_marker(self, marker: str, day: str) -> tuple[HourSnapshot, ...]: ...


class HoursCommand(Protocol):
    def send(self, plan: HoursPlan) -> Mapping[str, Any] | None: ...


class ContextGuard(Protocol):
    def confirm(self, expected_administration: int) -> None: ...


class EventReader(Protocol):
    def events(self) -> tuple[Mapping[str, Any], ...]: ...


class EventWriter(Protocol):
    def append(self, value: Mapping[str, Any]) -> None: ...


class SerialLock(Protocol):
    def acquire(self) -> ContextManager[None]: ...


def cleanup_plan(create_operation_id: str, latest_operation_id: str, events: tuple[Mapping[str, Any], ...],
                 *, operation_id: str, administration_id: int, contract_sha256: str) -> HoursPlan:
    creates = [x for x in events if x.get("operationId") == create_operation_id and x.get("status") in VERIFIED_STATUSES and x.get("kind") == "create"]
    latest = [x for x in events if x.get("operationId") == latest_operation_id and x.get("status") in VERIFIED_STATUSES and x.get("kind") in ("create", "edit")]
    if len(creates) != 1 or len(latest) != 1 or creates[0].get("syntheticPilot") is not True:
        raise HoursError("OWNED_PILOT_RECEIPT_REQUIRED")
    owner, state = creates[0], latest[0]
    if owner["administrationId"] != administration_id or state["administrationId"] != administration_id or owner["targetId"] != state["targetId"] or owner["marker"] != state["marker"]:
        raise HoursError("CLEANUP_OWNERSHIP_MISMATCH")
    if state.get("ownerOperationId") not in (None, create_operation_id) or (state["kind"] == "edit" and state.get("ownerOperationId") != create_operation_id):
        raise HoursError("CLEANUP_LATEST_RECEIPT_UNBOUND")
    before = HourSnapshot.capture(state["after"])
    return HoursPlan(operation_id, "cleanup", administration_id, owner["sourceKey"], contract_sha256,
                     canonical({}), before.raw_json, before.raw_json, owner["marker"],
                     create_operation_id, True)


def _bound_operation_events(plan: HoursPlan, events: tuple[Mapping[str, Any], ...]) -> tuple[Mapping[str, Any], ...]:
    """A reconciliation/unresolved-intent check must refer to its original intent."""
    related = tuple(x for x in events if x.get("operationId") == plan.operation_id)
    pending = [x for x in related if x.get("status") == "PENDING"]
    if len(pending) != 1 or canonical(pending[0].get("plan")) != canonical(plan.document()):
        raise HoursError("JOURNAL_PLAN_MISMATCH")
    binding = {"planHash": plan.digest, "administrationId": plan.administration_id,
               "kind": plan.kind, "sourceKey": plan.source_key, "marker": plan.marker,
               "ownerOperationId": plan.owner_operation_id, "syntheticPilot": plan.synthetic_pilot}
    for event in related:
        if any(canonical(event.get(key)) != canonical(value) for key, value in binding.items()):
            raise HoursError("JOURNAL_PLAN_MISMATCH")
    return related


def _journal_target(plan: HoursPlan, events: tuple[Mapping[str, Any], ...]) -> int | None:
    targets = set()
    for event in events:
        if "targetId" not in event or event["targetId"] is None:
            continue
        value = event["targetId"]
        # A create timeout before receiving its ID records the initial zero.
        if plan.kind == "create" and type(value) is int and value == 0 and event.get("status") == "UNCERTAIN":
            continue
        targets.add(positive_id(value))
    if plan.kind != "create":
        expected_id = positive_id(plan.expected()["id"])
        if any(value != expected_id for value in targets):
            raise HoursError("JOURNAL_TARGET_MISMATCH")
        return expected_id
    if len(targets) > 1:
        raise HoursError("JOURNAL_TARGET_MISMATCH")
    return next(iter(targets), None)


def _require_resolved_target(plan: HoursPlan, events: tuple[Mapping[str, Any], ...]) -> None:
    if plan.kind == "create":
        return
    identifier = positive_id(plan.expected()["id"])
    for intent in events:
        if intent.get("status") != "PENDING" or intent.get("administrationId") != plan.administration_id:
            continue
        prior = HoursPlan.load(intent["plan"], intent["planHash"])
        related = _bound_operation_events(prior, events)
        target = _journal_target(prior, related)
        if target == identifier and related[-1].get("status") not in VERIFIED_STATUSES:
            raise HoursError("UNRESOLVED_TARGET_OPERATION", {"operationId": prior.operation_id, "targetId": identifier})


class HoursExecutor:
    """Execute one plan with a durable intent and mandatory independent readback."""
    def __init__(self, reader: HoursReader, command: HoursCommand, context: ContextGuard,
                 history: EventReader, journal: EventWriter, lock: SerialLock):
        self.reader, self.command, self.context = reader, command, context
        self.history, self.journal, self.lock = history, journal, lock

    def apply(self, plan: HoursPlan) -> None:
        with self.lock.acquire():
            events = self.history.events()
            if any(x.get("operationId") == plan.operation_id for x in events):
                raise HoursError("OPERATION_ALREADY_ATTEMPTED")
            if plan.kind == "create" and any(x.get("sourceKey") == plan.source_key and x.get("kind") == "create" for x in events):
                raise HoursError("CREATE_SOURCE_ALREADY_ATTEMPTED")
            _require_resolved_target(plan, events)
            self.context.confirm(plan.administration_id)
            if plan.kind == "create":
                if plan.marker and self.reader.find_marker(plan.marker, record_date(plan.expected()["datum"])):
                    raise HoursError("REMOTE_MARKER_ALREADY_EXISTS")
            else:
                identifier = positive_id(plan.expected()["id"])
                current = self.reader.read_hour(identifier)
                if current is None or current.raw_json != plan.baseline_json:
                    raise HoursError("STALE_BASELINE")
                if plan.kind == "cleanup":
                    owner = [x for x in events if x.get("operationId") == plan.owner_operation_id and x.get("kind") == "create" and x.get("status") in VERIFIED_STATUSES and x.get("syntheticPilot") is True]
                    if len(owner) != 1 or owner[0].get("targetId") != identifier or owner[0].get("administrationId") != plan.administration_id or owner[0].get("marker") != plan.marker or plan.marker not in str(current.data().get("opmerkingen", "")):
                        raise HoursError("CLEANUP_NOT_OWNED_PILOT")
            event = {"operationId": plan.operation_id, "kind": plan.kind, "sourceKey": plan.source_key,
                     "planHash": plan.digest, "administrationId": plan.administration_id,
                     "marker": plan.marker, "ownerOperationId": plan.owner_operation_id,
                     "syntheticPilot": plan.synthetic_pilot}
            self.context.confirm(plan.administration_id)
            self.journal.append({**event, "status": "PENDING", "plan": plan.document()})
            target_id = plan.expected().get("id")
            try:
                response = self.command.send(plan)
                if plan.kind == "create":
                    target_id = positive_id(response.get("id") if isinstance(response, Mapping) else None)
                self.journal.append({**event, "status": "ACKNOWLEDGED", "targetId": target_id, "response": response})
                self.context.confirm(plan.administration_id)
                after = self.reader.read_hour(positive_id(target_id))
                if plan.kind == "cleanup":
                    if after is not None:
                        raise HoursError("CLEANUP_RECORD_STILL_EXISTS")
                    saved = None
                else:
                    if after is None:
                        raise HoursError("READBACK_NOT_FOUND")
                    verify_saved(plan, after, positive_id(target_id))
                    saved = after.data()
                self.journal.append({**event, "status": "VERIFIED", "targetId": target_id, "after": saved})
            except Exception as exc:
                self.journal.append({**event, "status": "UNCERTAIN", "targetId": target_id,
                                     "diagnostic": {"type": type(exc).__name__, "message": str(exc),
                                                    "facts": getattr(exc, "facts", None), "httpFields": getattr(exc, "fields", None)}})
                raise

    def record_reconciliation(self, plan: HoursPlan, result: ReconciliationResult) -> None:
        with self.lock.acquire():
            facts = result.data()
            if facts.get("planHash") != plan.digest or facts.get("status") != "MATCHES_EXPECTED":
                raise HoursError("RECONCILIATION_NOT_VERIFIED")
            events = _bound_operation_events(plan, self.history.events())
            if any(x.get("status") in VERIFIED_STATUSES for x in events):
                raise HoursError("RECONCILIATION_JOURNAL_STATE_INVALID")
            identifier = positive_id(facts.get("targetId"))
            bound_target = _journal_target(plan, events)
            if bound_target is not None and identifier != bound_target:
                raise HoursError("RECONCILIATION_TARGET_MISMATCH")
            self.context.confirm(plan.administration_id)
            current = self.reader.read_hour(identifier)
            if plan.kind == "cleanup":
                if current is not None:
                    raise HoursError("CLEANUP_RECORD_STILL_EXISTS")
            elif current is None:
                raise HoursError("READBACK_NOT_FOUND")
            else:
                verify_saved(plan, current, identifier)
            self.journal.append({"operationId": plan.operation_id, "kind": plan.kind,
                "sourceKey": plan.source_key, "planHash": plan.digest,
                "administrationId": plan.administration_id, "marker": plan.marker,
                "ownerOperationId": plan.owner_operation_id, "syntheticPilot": plan.synthetic_pilot,
                "status": "RECONCILED_VERIFIED", "targetId": identifier,
                "after": None if current is None else current.data()})


class HoursReconciler:
    """Read-only investigation of an existing operation; no command/journal writer."""
    def __init__(self, reader: HoursReader, context: ContextGuard, history: EventReader):
        self.reader, self.context, self.history = reader, context, history

    def reconcile(self, plan: HoursPlan) -> ReconciliationResult:
        # Read-only. Recording a reconciliation is an explicit caller command.
        self.context.confirm(plan.administration_id)
        events = _bound_operation_events(plan, self.history.events())
        target_id = _journal_target(plan, events)
        if target_id is None and plan.kind == "create" and plan.marker:
            matches = self.reader.find_marker(plan.marker, record_date(plan.expected()["datum"]))
            if len(matches) != 1:
                return ReconciliationResult(canonical({"status": "UNRESOLVED", "matchCount": len(matches), "planHash": plan.digest}))
            target_id = matches[0].data()["id"]
        if target_id is None:
            raise HoursError("RECONCILIATION_TARGET_UNKNOWN")
        after = self.reader.read_hour(positive_id(target_id))
        if plan.kind == "cleanup":
            status = "MATCHES_EXPECTED" if after is None else "UNRESOLVED"
        elif after is None:
            status = "UNRESOLVED"
        else:
            verify_saved(plan, after, positive_id(target_id))
            status = "MATCHES_EXPECTED"
        return ReconciliationResult(canonical({"status": status, "planHash": plan.digest, "targetId": target_id,
                "after": None if after is None else after.data()}))
