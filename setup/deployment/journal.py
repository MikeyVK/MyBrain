"""Destination ownership, output hashes and exclusive resumable stage journal."""
from __future__ import annotations
from contextlib import contextmanager
import ctypes
from datetime import datetime, timezone
import json
import os
import time
from pathlib import Path
from contracts import DeploymentError, TargetOwnership, digest, no_links, relative_name, strict_json, tree_files

def atomic_json(path: Path, value: dict) -> None:
    no_links(path)
    temp = path.with_suffix(path.suffix + ".new")
    no_links(temp)
    if temp.exists():
        raise DeploymentError("unexpected_temporary_file", 4)
    body = (json.dumps(value, indent=2) + "\n").encode("utf-8")
    previous = path.read_bytes() if path.exists() else None
    if previous == body:
        return
    with temp.open("xb") as f:
        f.write(body)
        f.flush()
        os.fsync(f.fileno())
    for attempt in range(20):
        no_links(path)
        no_links(temp)
        observed = path.read_bytes() if path.exists() else None
        if observed != previous:
            raise DeploymentError("metadata_changed_during_write", 4)
        try:
            temp.replace(path)
            return
        except PermissionError as exc:
            if os.name != "nt" or getattr(exc, "winerror", None) not in (5, 32, 33) or attempt == 19:
                raise
            time.sleep(.05)


def live_process(pid: int) -> bool:
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        error = ctypes.get_last_error()
        if error == 87:
            return False
        raise DeploymentError("process_state_unavailable", 4)
    try:
        code = ctypes.c_ulong()
        if not kernel.GetExitCodeProcess(handle, ctypes.byref(code)):
            raise DeploymentError("process_state_unavailable", 4)
        return code.value == 259
    finally:
        kernel.CloseHandle(handle)

class Journal:
    """Write only verified-owned outputs and retain incomplete stage bytes."""
    def __init__(self, target: Path, package: Path, manifest: dict):
        self.target = target.absolute()
        self.package = package
        self.owner = TargetOwnership().inspect(self.target, package, manifest)
        self.directory = self.target / ".deployment"
        self.path = self.directory / "journal.json"
        self.lock = self.directory / "writer.lock"

    def claim(self) -> None:
        self.directory.mkdir(parents=True, exist_ok=True)
        owner_path = self.directory / "owner.json"
        if not owner_path.exists():
            atomic_json(owner_path, self.owner)
        if not self.path.exists():
            atomic_json(self.path, {"stages": {}, "outputs": {}, "quarantined": []})

    def read(self) -> dict:
        no_links(self.path)
        return strict_json(self.path.read_bytes())

    def validate(self) -> None:
        pending = self.path.with_suffix(self.path.suffix + ".new")
        no_links(pending)
        if pending.exists():
            raise DeploymentError("pending_metadata_requires_recovery", 4)
        state = self.read()
        for rel, sha in state["outputs"].items():
            p = self.target / relative_name(rel)
            no_links(p)
            if not p.is_file() or digest(p) != sha:
                raise DeploymentError("changed_owned_output:" + rel, 4)

    @contextmanager
    def exclusive(self):
        self.claim()
        no_links(self.lock)
        try:
            fd = os.open(self.lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
        except FileExistsError:
            raise DeploymentError("writer_lock_requires_recovery", 4)
        with os.fdopen(fd, "w") as stream:
            json.dump({"pid": os.getpid(), "owner": self.owner}, stream)
        try:
            self.validate()
            yield
        finally:
            value = strict_json(self.lock.read_bytes())
            if value != {"pid": os.getpid(), "owner": self.owner}:
                raise DeploymentError("lock_identity_changed", 4)
            self.lock.unlink()

    def recover_lock(self) -> None:
        no_links(self.lock)
        if self.lock.exists():
            value = strict_json(self.lock.read_bytes())
            if value.get("owner") != self.owner or type(value.get("pid")) is not int:
                raise DeploymentError("unknown_writer_lock", 4)
            if live_process(value["pid"]):
                raise DeploymentError("writer_still_live", 4)
            self.lock.unlink()
        pending = self.path.with_suffix(self.path.suffix + ".new")
        no_links(pending)
        saved = None
        if pending.exists():
            if not pending.is_file():
                raise DeploymentError("pending_metadata_not_regular", 4)
            saved = self.directory / "quarantine" / ("metadata-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
            no_links(saved)
            saved.parent.mkdir(exist_ok=True)
            pending.rename(saved)
        self.claim()
        if saved is not None:
            state = self.read()
            state["quarantined"].append(saved.relative_to(self.target).as_posix())
            atomic_json(self.path, state)

    def put(self, rel: str, data: bytes) -> None:
        p = self.target / relative_name(rel)
        no_links(p)
        if p.exists():
            if not p.is_file() or p.read_bytes() != data:
                raise DeploymentError("output_conflict:" + rel, 4)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open("xb") as f:
                f.write(data)
        state = self.read()
        sha = digest(p)
        if state["outputs"].get(rel) == sha:
            return
        state["outputs"][rel] = sha
        atomic_json(self.path, state)

    def stage(self, name: str, status: str) -> None:
        state = self.read()
        if state["stages"].get(name) == status:
            return
        state["stages"][name] = status
        atomic_json(self.path, state)

    def record_tree(self, root: Path) -> None:
        state = self.read()
        for rel, p in tree_files(root).items():
            state["outputs"][p.relative_to(self.target).as_posix()] = digest(p)
        atomic_json(self.path, state)

    def quarantine_incomplete(self, name: str, root: Path) -> None:
        state = self.read()
        if state["stages"].get(name) != "running" or not root.exists():
            return
        no_links(root)
        tree_files(root)
        if not root.is_relative_to(self.target) or root == self.target:
            raise DeploymentError("quarantine_outside_destination", 4)
        out = self.directory / "quarantine" / (name + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%f"))
        no_links(out)
        out.parent.mkdir(exist_ok=True)
        root.rename(out)
        state["quarantined"].append(out.relative_to(self.target).as_posix())
        for rel in list(state["outputs"]):
            if (self.target / rel).is_relative_to(root):
                del state["outputs"][rel]
        atomic_json(self.path, state)
