"""Small host adapters over the existing shared App transport/auth/log writer."""
from __future__ import annotations
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from typing import Any, Callable, Mapping
from hours_domain import (FILTER_PATH, HOURS_PATH, DTO_FIELDS, HoursError, HoursPlan, HourSnapshot,
                          canonical, positive_id, record_date, work_date)


@dataclass(frozen=True)
class HttpResult:
    status: int
    body_json: str

    def data(self) -> Any:
        return json.loads(self.body_json)


class SharedWire:
    """Admit only auth and hours paths; delegate all network/TLS to shared code."""
    def __init__(self, transport_factory: Callable, observed_connection: Callable,
                 connection_factory: Callable, allow_writes: bool = False):
        self.transport_factory = transport_factory
        self.observed_connection = observed_connection
        self.connection_factory = connection_factory
        self.allow_writes = allow_writes
        self.calls = 0

    def call(self, method: str, path: str, body: Mapping[str, Any] | None = None,
             access: str | None = None, accepted: tuple[int, ...] = (200,)) -> HttpResult:
        auth = (method == "POST" and path == "/api/v4/auth/login" and isinstance(body, Mapping)
                and set(body) == {"username", "password"})
        read = ((method == "GET" and body is None and (path == "/api/v4/auth/userinfo" or
                 re.fullmatch(re.escape(HOURS_PATH) + r"/[1-9][0-9]*", path))) or
                (method == "POST" and path == FILTER_PATH and isinstance(body, Mapping)))
        write = self.allow_writes and ((method in ("POST", "PUT") and path == HOURS_PATH and isinstance(body, Mapping)
                                      and set(body) <= DTO_FIELDS | {"$id"}) or
                                     (method == "DELETE" and body is None and
                                      re.fullmatch(re.escape(HOURS_PATH) + r"/[1-9][0-9]*", path)))
        if not (auth or read or write) or self.calls >= 80:
            raise HoursError("HOURS_TRANSPORT_SCOPE_REJECTED")
        self.calls += 1
        observed: dict[str, int] = {}
        def observe(response):
            observed["status"] = response.status
        def factory(*args, **kwargs):
            return self.observed_connection(self.connection_factory(*args, **kwargs), observe)
        expected = None if body is None else canonical(dict(body))
        def allowed(m, p, b):
            return m == method and p == path and (None if b is None else canonical(b)) == expected
        transport = self.transport_factory("app", factory=factory, command_policy=allowed,
                                           accepted_statuses=accepted)
        value = transport.request(method, path, None if body is None else dict(body), token=access)
        return HttpResult(observed["status"], canonical(value))


class AuthRequests:
    """Only the auth contract expected by the existing AppAuthentication."""
    def __init__(self, wire: SharedWire):
        self.wire = wire
        self.last_user_info: Mapping[str, Any] | None = None

    def request(self, method, path, body=None, token=None):
        if (method, path) not in (("POST", "/api/v4/auth/login"), ("GET", "/api/v4/auth/userinfo")):
            raise HoursError("AUTH_ONLY_REQUEST_REQUIRED")
        value = self.wire.call(method, path, body, access=token).data()
        if path == "/api/v4/auth/userinfo":
            self.last_user_info = value
        return value


class AppContext:
    def __init__(self, authentication):
        self.authentication = authentication

    def confirm(self, expected_administration: int) -> None:
        if self.authentication.admin[0] != expected_administration:
            raise HoursError("ADMINISTRATION_MISMATCH")
        self.authentication.require_same_admin()


class AppHoursReader:
    def __init__(self, wire: SharedWire, authentication, request_failure_type: type[Exception]):
        self.wire = wire
        self.authentication = authentication
        self.request_failure_type = request_failure_type

    def read_hour(self, identifier: int) -> HourSnapshot | None:
        identifier = positive_id(identifier)
        try:
            result = self.wire.call("GET", HOURS_PATH + "/" + str(identifier), access=self.authentication.token)
        except self.request_failure_type as exc:
            if str(exc) == "HTTP_404":
                return None
            raise
        value = result.data()
        if not isinstance(value, dict) or value.get("id") != identifier:
            raise HoursError("HOURS_DETAIL_IDENTITY_MISMATCH")
        return HourSnapshot.capture(value)

    def find_marker(self, marker: str, day: str) -> tuple[HourSnapshot, ...]:
        day = work_date(day)
        if not marker or len(marker) > 160:
            raise HoursError("MARKER_QUERY_INVALID")
        # Inspect one complete, bounded workday. Do not trust remote free-text
        # filtering to establish that no duplicate marker exists.
        body = {"page": 1, "pageSize": 20,
                "period": {"startDate": day + "T00:00:00Z", "endDate": day + "T23:59:59Z"},
                "filterType": 0, "sortBy": 0, "sortDirection": 0, "nietGefactureerd": False}
        result = self.wire.call("POST", FILTER_PATH, body, access=self.authentication.token).data()
        if (not isinstance(result, dict) or not isinstance(result.get("items"), list)
                or len(result["items"]) > 20 or result.get("hasMoreRows") is not False):
            raise HoursError("HOURS_DAY_QUERY_INCOMPLETE")
        records = []
        for row in result["items"]:
            if not isinstance(row, dict) or record_date(row.get("datum")) != day:
                raise HoursError("HOURS_QUERY_OUTSIDE_DAY")
            if marker in str(row.get("opmerkingen", "")):
                full = self.read_hour(positive_id(row.get("id")))
                if full is None:
                    raise HoursError("HOURS_QUERY_RESULT_DISAPPEARED")
                records.append(full)
        return tuple(records)


class OneShotHoursCommand:
    def __init__(self, wire: SharedWire, authentication):
        self.wire, self.authentication = wire, authentication
        self.attempted: set[str] = set()

    def send(self, plan: HoursPlan) -> Mapping[str, Any] | None:
        if plan.operation_id in self.attempted:
            raise HoursError("COMMAND_RETRY_REJECTED")
        self.attempted.add(plan.operation_id)
        accepted = (200, 201) if plan.kind == "create" else (200, 204)
        body = None if plan.kind == "cleanup" else plan.payload()
        result = self.wire.call(plan.method, plan.path, body,
                                access=self.authentication.token, accepted=accepted)
        response = result.data()
        rejected = response is False or (isinstance(response, dict) and
                    (("success" in response and response["success"] is not True) or ("error" in response and response["error"] is not None) or bool(response.get("errors")) or bool(response.get("errorType"))))
        if rejected or (response is None and result.status != 204):
            raise HoursError("HOURS_ACK_REJECTED", {"status": result.status, "response": response})
        if result.status == 204:
            return None
        if isinstance(response, dict):
            return response
        if response is True and plan.kind != "create":
            return {"success": True}
        raise HoursError("HOURS_ACK_SHAPE_UNPROVED", {"status": result.status})


class JsonEventReader:
    def __init__(self, path: Path):
        self.path = path

    def events(self) -> tuple[Mapping[str, Any], ...]:
        if not self.path.exists():
            return ()
        if self.path.stat().st_size > 64 * 1024 * 1024:
            raise HoursError("JOURNAL_SIZE_BOUND")
        return tuple(json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line)


class SharedEventWriter:
    def __init__(self, path: Path, output):
        self.path, self.output = path, output

    def append(self, value: Mapping[str, Any]) -> None:
        self.output.append(self.path, {**dict(value), "recordedAt": datetime.now(timezone.utc).isoformat()})


class ExclusiveFileLock:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def acquire(self):
        try:
            descriptor = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise HoursError("HOURS_OPERATION_LOCKED") from exc
        try:
            os.write(descriptor, str(os.getpid()).encode("ascii"))
            os.fsync(descriptor)
            yield
        finally:
            os.close(descriptor)
            self.path.unlink()
