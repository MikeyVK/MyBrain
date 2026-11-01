"""Thin composition/presentation boundary for one hours operation at a time."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
import argparse
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import sys
from uuid import uuid4
from hours_domain import (HourSnapshot, HoursError, HoursPlan, HoursExecutor, HoursReconciler,
                          cleanup_plan, positive_id, prepare_create, prepare_edit)
from hours_io import (AppContext, AppHoursReader, AuthRequests, ExclusiveFileLock,
                      JsonEventReader, OneShotHoursCommand, SharedEventWriter, SharedWire)


@dataclass(frozen=True)
class RuntimeConfig:
    administration_id: int
    contract_sha256: str


def load_json(path: Path, expected_sha256: str | None = None):
    raw = path.read_bytes()
    if len(raw) > 16 * 1024 * 1024:
        raise HoursError("LOCAL_INPUT_TOO_LARGE")
    if expected_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_sha256.lower():
        raise HoursError("LOCAL_INPUT_HASH_MISMATCH")
    return json.loads(raw.decode("utf-8"))


def config(root: Path) -> RuntimeConfig:
    value = load_json(root / "runtime-config.json")
    return RuntimeConfig(positive_id(value["administrationId"]), value["contractSha256"])


def load_plan(args) -> HoursPlan:
    value = load_json(private_path(Path(args.input)), args.input_sha256)
    return HoursPlan.load(value["plan"], value["planHash"])


def output_only(root: Path):
    from private_output import PrivateOutput
    return PrivateOutput(root, secrets=[])


def read_components(root: Path, settings: RuntimeConfig, output):
    # Host paths and credential access stay at the CLI composition root.
    p = root.parent
    import app_probe as app
    import processed_invoice_probe as transport
    from app_session import AppAuthentication
    from private_output import PrivateOutput
    wire = SharedWire(transport.Transport, app.ObservedConnection, app.tls_connection)
    auth_requests = AuthRequests(wire)
    authentication = AppAuthentication(auth_requests)
    login = app.load_login(app.WindowsBackend().api)
    output.secrets.extend((login.username, login.password))
    try:
        authentication.login(login, settings.administration_id)
    finally:
        output.secrets.extend(authentication.secrets)
    userinfo = auth_requests.last_user_info or {}
    user = userinfo.get("user", {})
    output.save("hours-auth-context", {"administrationId": settings.administration_id,
                "userId": user.get("id"), "isSuper": user.get("isSuper"),
                "permissionRead": userinfo.get("permissies"),
                "permissionMeaning": "OBSERVED_CONTEXT_NOT_A_SERVER_WRITE_GUARANTEE"})
    reader = AppHoursReader(wire, authentication, app.RequestFailure)
    return authentication, reader, AppContext(authentication), output, transport, app


def save_plan(root: Path, plan: HoursPlan, output):
    file = output.save("hours-plan", {"plan": plan.document(), "planHash": plan.digest})
    return {"status": "PREPARED_NO_WRITE", "plan": str(file),
            "fileSha256": hashlib.sha256(file.read_bytes()).hexdigest(),
            "planHash": plan.digest, "operationId": plan.operation_id}


def common_plan_args(args, settings: RuntimeConfig):
    return {"operation_id": args.operation_id or str(uuid4()),
            "administration_id": settings.administration_id,
            "source_key": args.source_key,
            "contract_sha256": settings.contract_sha256,
            "marker": args.marker, "synthetic_pilot": args.synthetic_pilot}


def do_prepare_create(args, root: Path, settings: RuntimeConfig):
    request = load_json(private_path(Path(args.request)))
    return save_plan(root, prepare_create(request, **common_plan_args(args, settings)), args.output)


def do_prepare_edit(args, root: Path, settings: RuntimeConfig):
    authentication, reader, context, output, _, _ = read_components(root, settings, args.output)
    context.confirm(settings.administration_id)
    before = reader.read_hour(args.id)
    if before is None:
        raise HoursError("HOURS_RECORD_NOT_FOUND")
    output.save("hours-before-edit", {"record": before.data(), "sha256": before.digest})
    changes = load_json(private_path(Path(args.changes)))
    plan = prepare_edit(before, changes, owner_operation_id=args.owner_operation_id,
                        **common_plan_args(args, settings))
    return save_plan(root, plan, args.output)


def do_prepare_cleanup(args, root: Path, settings: RuntimeConfig):
    history = JsonEventReader(root / "hours-journal.jsonl")
    plan = cleanup_plan(args.create_operation_id, args.latest_operation_id, history.events(),
                        operation_id=args.operation_id or str(uuid4()),
                        administration_id=settings.administration_id,
                        contract_sha256=settings.contract_sha256)
    return save_plan(root, plan, args.output)


def do_read(args, root: Path, settings: RuntimeConfig):
    _, reader, context, output, _, _ = read_components(root, settings, args.output)
    context.confirm(settings.administration_id)
    result = reader.read_hour(args.id)
    context.confirm(settings.administration_id)
    file = output.save("hours-detail", {"record": None if result is None else result.data(),
                                       "status": "NOT_FOUND" if result is None else "READ"})
    return {"status": "READ_ONLY", "result": str(file), "fileSha256": hashlib.sha256(file.read_bytes()).hexdigest()}


def do_query_marker(args, root: Path, settings: RuntimeConfig):
    _, reader, context, output, _, _ = read_components(root, settings, args.output)
    context.confirm(settings.administration_id)
    rows = reader.find_marker(args.marker, args.day)
    context.confirm(settings.administration_id)
    file = output.save("hours-marker-query", {"day": args.day, "marker": args.marker,
                      "matches": [r.data() for r in rows], "status": "COMPLETE_BOUNDED_DAY_READ"})
    return {"status": "READ_ONLY", "matchCount": len(rows), "result": str(file)}


def do_apply(args, root: Path, settings: RuntimeConfig):
    plan = load_plan(args)
    if plan.administration_id != settings.administration_id or plan.contract_sha256 != settings.contract_sha256:
        raise HoursError("RUNTIME_PLAN_BINDING_MISMATCH")
    if not args.apply:
        return {"status": "DRYRUN_NO_API", "operationId": plan.operation_id, "planHash": plan.digest,
                "method": plan.method, "path": plan.path, "expected": plan.expected()}
    authentication, reader, context, output, transport, app = read_components(root, settings, args.output)
    wire = SharedWire(transport.Transport, app.ObservedConnection, app.tls_connection, allow_writes=True)
    command = OneShotHoursCommand(wire, authentication)
    history = JsonEventReader(root / "hours-journal.jsonl")
    engine = HoursExecutor(reader, command, context, history,
                           SharedEventWriter(root / "hours-journal.jsonl", output),
                           ExclusiveFileLock(root / "hours-command.lock"))
    engine.apply(plan)
    result = [e for e in history.events() if e.get("operationId") == plan.operation_id][-1]
    file = output.save("hours-operation-result", result)
    return {"status": result["status"], "operationId": plan.operation_id, "targetId": result["targetId"], "result": str(file)}


def do_reconcile(args, root: Path, settings: RuntimeConfig):
    plan = load_plan(args)
    if plan.administration_id != settings.administration_id or plan.contract_sha256 != settings.contract_sha256:
        raise HoursError("RUNTIME_PLAN_BINDING_MISMATCH")
    _, reader, context, output, _, _ = read_components(root, settings, args.output)
    result = HoursReconciler(reader, context, JsonEventReader(root / "hours-journal.jsonl")).reconcile(plan)
    file = output.save("hours-reconciliation", result.data())
    return {"status": result.data()["status"], "result": str(file), "planHash": plan.digest}


def parser():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(required=True)
    for name, handler in (("prepare-create", do_prepare_create), ("prepare-edit", do_prepare_edit)):
        s = sub.add_parser(name);s.set_defaults(handler=handler)
        s.add_argument("--source-key", required=True);s.add_argument("--operation-id")
        s.add_argument("--marker");s.add_argument("--synthetic-pilot", action="store_true")
        if name == "prepare-create":
            s.add_argument("--request", required=True)
        else:
            s.add_argument("--id", type=int, required=True);s.add_argument("--changes", required=True)
            s.add_argument("--owner-operation-id")
    s = sub.add_parser("prepare-cleanup");s.set_defaults(handler=do_prepare_cleanup)
    s.add_argument("--create-operation-id", required=True);s.add_argument("--latest-operation-id", required=True);s.add_argument("--operation-id")
    s = sub.add_parser("read");s.set_defaults(handler=do_read);s.add_argument("--id", type=int, required=True)
    s = sub.add_parser("query-marker");s.set_defaults(handler=do_query_marker);s.add_argument("--marker", required=True);s.add_argument("--day", required=True)
    for name, handler in (("apply", do_apply), ("reconcile", do_reconcile)):
        s = sub.add_parser(name);s.set_defaults(handler=handler)
        s.add_argument("--input", required=True);s.add_argument("--input-sha256", required=True)
        if name == "apply":s.add_argument("--apply", action="store_true")
    return p


def main() -> int:
    root = runtime_area("hours")
    args = parser().parse_args()
    from toolkit_runtime import ensure_private_directory
    ensure_private_directory(root)
    args.output = output_only(root)
    try:
        result = args.handler(args, root, config(root))
        print(json.dumps(result, ensure_ascii=True), flush=True)
        return 0
    except Exception as exc:
        # CLI presentation boundary; shared writer retains structured diagnostics.
        file = args.output.save("hours-cli-stop", {"exceptionType": type(exc).__name__,
                       "code": str(exc), "facts": getattr(exc, "facts", None),
                       "httpFields": getattr(exc, "fields", None)})
        print(json.dumps({"status": "STOPPED", "exceptionType": type(exc).__name__, "diagnostic": str(file)}), flush=True)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
