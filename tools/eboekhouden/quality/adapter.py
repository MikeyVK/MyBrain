"""PGMCP check/test v1 boundary for one explicitly configured research toolkit.

Bootstrap candidate only. No implicit CWD/PATH interpreter or workspace fallback.
The native child parses source or runs offline pytest; it never imports a helper CLI.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys


class Refusal(ValueError):
    """A request or deployment outside the approved boundary."""


def plain_path(value, *, must_exist=False):
    if not isinstance(value, str) or not value or "\0" in value:
        raise Refusal("INVALID_PATH")
    path = Path(value)
    if not path.is_absolute() or any(p in (".", "..") for p in path.parts):
        raise Refusal("ABSOLUTE_PATH_WITHOUT_TRAVERSAL_REQUIRED")
    for part in reversed([path, *path.parents]):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise Refusal("LINK_OR_REPARSE_PATH_REFUSED")
    resolved = path.resolve(strict=must_exist)
    if resolved != path:
        raise Refusal("NONCANONICAL_PATH_REFUSED")
    return resolved


def contained(value, root, *, must_exist=False):
    path = plain_path(value, must_exist=must_exist)
    if path == root or not path.is_relative_to(root):
        raise Refusal("OUTSIDE_APPROVED_ROOT")
    return path


def config(value):
    required = {"workspace", "interpreter", "python_version", "pins"}
    if type(value) is not dict or set(value) != required:
        raise Refusal("INVALID_DEPLOYMENT_CONFIG")
    workspace = plain_path(value["workspace"], must_exist=True)
    toolkit = plain_path(str(workspace / "tools" / "eboekhouden"), must_exist=True)
    interpreter = plain_path(value["interpreter"], must_exist=True)
    expected = toolkit / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if interpreter != expected or not interpreter.is_file():
        raise Refusal("EXPLICIT_TOOLKIT_INTERPRETER_REQUIRED")
    cfg = toolkit / ".venv" / "pyvenv.cfg"
    if "include-system-site-packages = false" not in cfg.read_text(encoding="utf-8").lower():
        raise Refusal("ISOLATED_VENV_REQUIRED")
    if not isinstance(value["python_version"], str) or type(value["pins"]) is not dict:
        raise Refusal("INVALID_DEPLOYMENT_IDENTITIES")
    if set(value["pins"]) != {"pytest", "pytest-cov", "pytest-xdist", "coverage", "pytest-asyncio"}:
        raise Refusal("EXPLICIT_NATIVE_TEST_PINS_REQUIRED")
    if not all(isinstance(v, str) and v for v in value["pins"].values()):
        raise Refusal("INVALID_TEST_PIN")
    return workspace, toolkit, interpreter


def request(value, toolkit):
    if type(value) is not dict:
        raise Refusal("REQUEST_OBJECT_REQUIRED")
    operation = value.get("operation")
    content_mode = "target_path" in value
    required = {"operation", "args", "execution_context"} | (
        {"target_path", "content"} if content_mode else {"targets"})
    if set(value) != required or value.get("args") != []:
        raise Refusal("CLOSED_REQUEST_NO_CALLER_NATIVE_ARGUMENTS")
    context = value["execution_context"]
    if type(context) is not dict or set(context) != {"scratch_directory"}:
        raise Refusal("EXECUTION_CONTEXT_REQUIRED")
    scratch = plain_path(context["scratch_directory"], must_exist=True)
    if not scratch.is_dir():
        raise Refusal("EXECUTION_SCRATCH_DIRECTORY_REQUIRED")
    if content_mode:
        if operation != "syntax" or not isinstance(value["content"], str):
            raise Refusal("CONTENT_SYNTAX_ONLY")
        target = contained(value["target_path"], toolkit)
        if target.suffix != ".py" or any(p in {".venv", ".local", ".local-work", "__pycache__"} for p in target.relative_to(toolkit).parts):
            raise Refusal("TOOLKIT_SOURCE_PYTHON_ONLY")
        return {"operation": "syntax", "target_path": str(target), "content": value["content"]}
    if operation not in {"syntax", "tests"} or type(value["targets"]) is not list or not value["targets"]:
        raise Refusal("EXPLICIT_NONEMPTY_SELECTION_REQUIRED")
    selection_root = toolkit / "tests" if operation == "tests" else toolkit
    targets = []
    for item in value["targets"]:
        path = plain_path(item, must_exist=True)
        if path.is_relative_to(toolkit) and any(
                p in {".venv", ".local", ".local-work", "__pycache__"}
                for p in path.relative_to(toolkit).parts):
            raise Refusal("PRIVATE_OR_ENVIRONMENT_SELECTION_REFUSED")
        if path != selection_root:
            path = contained(item, selection_root, must_exist=True)
        elif not path.is_dir():
            raise Refusal("SELECTION_ROOT_NOT_DIRECTORY")
        if path.is_dir():
            for child in path.rglob("*"):
                plain_path(str(child), must_exist=True)
                if child.is_file() and child.suffix == ".py":
                    if any(p in {".venv", ".local", ".local-work", "__pycache__"} for p in child.relative_to(toolkit).parts):
                        continue
                    targets.append(child)
        elif path.suffix == ".py":
            targets.append(path)
        else:
            raise Refusal("PYTHON_SELECTION_REQUIRED")
    if not targets:
        raise Refusal("EMPTY_PYTHON_SELECTION")
    return {"operation": operation, "targets": list(dict.fromkeys(str(p) for p in targets))}


NATIVE = r'''
import ast, contextlib, importlib.metadata, io, json, pathlib, platform, sys
job=json.load(sys.stdin)
identity={"python":platform.python_version(),"prefix":str(pathlib.Path(sys.prefix).resolve()),"pins":{}}
expected=job["identity"]
if identity["python"]!=expected["python_version"] or identity["prefix"]!=expected["prefix"]:
 print(json.dumps({"status":"unavailable","reason":"dependency_unavailable","identity":identity,"message":"ISOLATED_INTERPRETER_IDENTITY_MISMATCH"}));sys.exit(3)
if job["operation"]=="syntax":
 try:
  if "content" in job: ast.parse(job["content"],filename=job["target_path"])
  else:
   for name in job["targets"]: ast.parse(pathlib.Path(name).read_text(encoding="utf-8-sig"),filename=name)
 except (SyntaxError,UnicodeError) as exc:
  print(json.dumps({"status":"failed","identity":identity,"message":"PYTHON_SYNTAX_FAILED","diagnostic":str(exc)}));sys.exit(1)
 print(json.dumps({"status":"passed","identity":identity,"parsed":1 if "content" in job else len(job["targets"])}));sys.exit(0)
try:
 for name,version in expected["pins"].items():
  identity["pins"][name]=importlib.metadata.version(name)
 if identity["pins"]!=expected["pins"]: raise ValueError("NATIVE_TEST_DEPENDENCY_PIN_MISMATCH")
 import pytest
except (ImportError,importlib.metadata.PackageNotFoundError,ValueError) as exc:
 print(json.dumps({"status":"unavailable","reason":"dependency_unavailable","identity":identity,"message":str(exc)}));sys.exit(3)
def offline(event,args):
 if event.startswith("socket."): raise RuntimeError("OFFLINE_TEST_NETWORK_REFUSED")
 if event=="ctypes.dlsym" and len(args)>1 and str(args[1]).startswith(("CredRead","CredWrite","CredEnumerate","CredDelete")):
  raise RuntimeError("OFFLINE_TEST_HOST_CREDENTIALS_REFUSED")
sys.addaudithook(offline)
capture=io.StringIO()
with contextlib.redirect_stdout(capture),contextlib.redirect_stderr(capture):
 code=pytest.main(["-c",job["pytest_ini"],"-q","-rA","-p","no:cacheprovider","--confcutdir="+job["tests_root"],*job["targets"]])
status="passed" if code==0 else "failed" if code==1 else "unavailable"
result={"status":status,"identity":identity,"message":"OFFLINE_PYTEST_EXIT_"+str(int(code)),"nativeExitCode":int(code),"output":capture.getvalue()}
if status=="unavailable": result["reason"]="execution_error"
print(json.dumps(result));sys.exit(0 if code==0 else 1 if code==1 else 3)
'''


def run(value, deployment, launch=subprocess.run):
    """Public adapter boundary; injectable subprocess used by offline admission tests."""
    selection = isinstance(value, dict) and value.get("operation") == "syntax" and "targets" in value
    checked_coverage = None

    def response(payload, code):
        if selection:
            payload["coverage"] = checked_coverage if payload["decision"]["status"] == "passed" else None
            payload["required_targets"] = []
        return payload, code

    try:
        workspace, toolkit, interpreter = config(deployment)
        job = request(value, toolkit)
        if selection:
            checked_coverage = {
                "targets": [Path(p).relative_to(workspace).as_posix() for p in job["targets"]],
                "expanded": any(Path(p).is_dir() for p in value["targets"]),
            }
        job["identity"] = {"python_version": deployment["python_version"], "pins": deployment["pins"],
                           "prefix": str(toolkit / ".venv")}
        if job["operation"] == "tests":
            ini = plain_path(str(toolkit / "pytest.ini"), must_exist=True)
            job.update(pytest_ini=str(ini), tests_root=str(toolkit / "tests"))
        env = {key: os.environ[key] for key in ("SystemRoot", "WINDIR", "TEMP", "TMP") if key in os.environ}
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        process = launch([str(interpreter), "-I", "-B", "-c", NATIVE], input=json.dumps(job),
                         text=True, encoding="utf-8", capture_output=True, timeout=180,
                         cwd=str(toolkit), env=env, shell=False)
        native = json.loads(process.stdout)
        status = native.get("status")
        exits = {"passed": 0, "failed": 1, "unavailable": 3}
        if status not in exits or process.returncode != exits[status]:
            raise Refusal("NATIVE_RESULT_EXIT_MISMATCH")
        observed = native.get("identity", {})
        if status != "unavailable" and (observed.get("python") != deployment["python_version"]
                or observed.get("prefix") != str(toolkit / ".venv")):
            raise Refusal("NATIVE_RESULT_IDENTITY_MISMATCH")
        decision = {"status": status}
        if job["operation"] == "tests" and status == "passed":
            decision["message"] = native["message"]
        if status != "passed": decision["message"] = native.get("message", "NATIVE_OPERATION_FAILED")
        if status == "unavailable": decision["reason"] = native.get("reason", "invalid_result")
        identities = [{"tool_id": "python", "version": observed.get("python")}]
        if "pytest" in observed.get("pins", {}):
            identities.append({"tool_id": "pytest", "version": observed["pins"]["pytest"]})
        return response({"decision": decision, "external_tools": identities,
                "evidence": {"format": "json", "data": native}}, exits[status])
    except Refusal as exc:
        return response({"decision": {"status": "unavailable", "reason": "unsupported_input", "message": str(exc)},
                "external_tools": []}, 3)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        return response({"decision": {"status": "unavailable", "reason": "execution_error", "message": type(exc).__name__},
                "external_tools": []}, 3)


def main():
    try:
        deployment = json.loads(Path(__file__).with_name("config.json").read_text(encoding="utf-8"))
        value = json.loads(sys.stdin.buffer.read(16 * 1024 * 1024 + 1).decode("utf-8"))
        result, code = run(value, deployment)
    except (OSError, ValueError) as exc:
        result, code = {"decision": {"status": "unavailable", "reason": "invalid_configuration",
                                    "message": type(exc).__name__}, "external_tools": []}, 3
    print(json.dumps(result, ensure_ascii=True), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
