"""Exact-key Windows Credential Manager adapter. Never enumerate credentials."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area

import csv
import ctypes
from ctypes import wintypes as w
from dataclasses import dataclass, field
import io
import re
import subprocess
import sys

TARGET = "MyBrain/eBoekhouden"
MARKER = "MyBrain API token - owner confirmed"
COMMENT = "MyBrain official REST; intended administration confirmed locally"
GENERIC = 1
LOCAL_MACHINE = 2
ENTERPRISE = 3
GUI_USERNAME = "api-token"
MAX_BLOB = 2560


class CredentialFailure(Exception):
    """Safe machine code only; never include token values."""


class CredentialAttribute(ctypes.Structure):
    _fields_ = [("Keyword", w.LPWSTR), ("Flags", w.DWORD),
                ("ValueSize", w.DWORD), ("Value", ctypes.POINTER(w.BYTE))]


class Credential(ctypes.Structure):
    _fields_ = [("Flags", w.DWORD), ("Type", w.DWORD), ("TargetName", w.LPWSTR),
                ("Comment", w.LPWSTR), ("LastWritten", w.FILETIME),
                ("CredentialBlobSize", w.DWORD), ("CredentialBlob", ctypes.POINTER(w.BYTE)),
                ("Persist", w.DWORD), ("AttributeCount", w.DWORD),
                ("Attributes", ctypes.POINTER(CredentialAttribute)),
                ("TargetAlias", w.LPWSTR), ("UserName", w.LPWSTR)]


@dataclass(frozen=True)
class Entry:
    target: str
    username: str
    comment: str
    persist: int
    value: str | None = field(default=None, repr=False)


def decode_blob(raw: bytes, username: str, comment: str) -> str:
    if username == MARKER and comment == COMMENT:
        encoding = "utf-8"
    elif username == GUI_USERNAME and comment == "":
        encoding = "utf-16-le"
    else:
        raise CredentialFailure("CREDENTIAL_KEY_NOT_MYBRAIN_OWNED")
    try:
        secret = raw.decode(encoding)
    except UnicodeError:
        raise CredentialFailure("WINDOWS_CREDENTIAL_FORMAT_UNKNOWN") from None
    if not secret or any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in secret):
        raise CredentialFailure("WINDOWS_CREDENTIAL_TOKEN_INVALID")
    if encoding == "utf-16-le" and not secret.isascii():
        # GUI API tokens are ASCII. Reject UTF-8 bytes accidentally interpreted
        # as UTF-16; never guess a different encoding after failure.
        raise CredentialFailure("WINDOWS_CREDENTIAL_FORMAT_UNKNOWN")
    return secret


def owner_sid(identity_reader=None) -> str:
    if sys.platform != "win32":
        raise CredentialFailure("WINDOWS_OWNER_REQUIRED")
    if identity_reader is None:
        from toolkit_runtime import require_live_config
        require_live_config()
        def identity_reader():
            result = subprocess.run(["whoami.exe", "/user", "/fo", "csv", "/nh"],
                                    capture_output=True, text=True, check=True)
            return result.stdout
    try:
        account, sid = next(csv.reader(io.StringIO(identity_reader())))
    except Exception:
        raise CredentialFailure("WINDOWS_IDENTITY_UNCONFIRMED") from None
    if "codexsandbox" in account.lower() or not re.fullmatch(r"S-1-[0-9-]+", sid):
        raise CredentialFailure("WINDOWS_OWNER_REQUIRED")
    return sid


class WindowsBackend:
    """CredRead/CredWrite exact key; native buffers freed/zeroed best effort."""

    def __init__(self):
        from toolkit_runtime import require_live_config
        require_live_config()
        self.api = ctypes.WinDLL("Advapi32", use_last_error=True)
        self.api.CredReadW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD,
                                      ctypes.POINTER(ctypes.POINTER(Credential))]
        self.api.CredReadW.restype = w.BOOL
        self.api.CredWriteW.argtypes = [ctypes.POINTER(Credential), w.DWORD]
        self.api.CredWriteW.restype = w.BOOL
        self.api.CredFree.argtypes = [ctypes.c_void_p]
        self.api.CredFree.restype = None
        self.api.CredDeleteW.argtypes = [w.LPCWSTR, w.DWORD, w.DWORD]
        self.api.CredDeleteW.restype = w.BOOL

    def read(self, target: str, include_secret: bool = False) -> Entry | None:
        pointer = ctypes.POINTER(Credential)()
        if not self.api.CredReadW(target, GENERIC, 0, ctypes.byref(pointer)):
            if ctypes.get_last_error() == 1168:
                return None
            raise CredentialFailure("WINDOWS_CREDENTIAL_READ_FAILED")
        try:
            value = pointer.contents
            if value.Type != GENERIC or not 0 < value.CredentialBlobSize <= MAX_BLOB or not value.CredentialBlob:
                raise CredentialFailure("WINDOWS_CREDENTIAL_FORMAT_UNKNOWN")
            secret = None
            if include_secret:
                secret = decode_blob(ctypes.string_at(value.CredentialBlob, value.CredentialBlobSize),
                                     value.UserName or "", value.Comment or "")
            return Entry(value.TargetName or "", value.UserName or "", value.Comment or "",
                         value.Persist, secret)
        finally:
            value = pointer.contents
            if value.CredentialBlob and 0 < value.CredentialBlobSize <= MAX_BLOB:
                ctypes.memset(value.CredentialBlob, 0, value.CredentialBlobSize)
            self.api.CredFree(pointer)

    def write(self, target: str, secret: str) -> None:
        raw = bytearray(secret, "utf-8")
        if not 0 < len(raw) <= MAX_BLOB:
            for index in range(len(raw)):
                raw[index] = 0
            raise CredentialFailure("WINDOWS_CREDENTIAL_SIZE_INVALID")
        buffer = (w.BYTE * len(raw)).from_buffer(raw)
        credential = Credential()
        credential.Type = GENERIC
        credential.TargetName = target
        credential.Comment = COMMENT
        credential.CredentialBlobSize = len(raw)
        credential.CredentialBlob = ctypes.cast(buffer, ctypes.POINTER(w.BYTE))
        credential.Persist = LOCAL_MACHINE
        credential.UserName = MARKER
        try:
            if not self.api.CredWriteW(ctypes.byref(credential), 0):
                raise CredentialFailure("WINDOWS_CREDENTIAL_WRITE_FAILED")
        finally:
            ctypes.memset(buffer, 0, len(raw))

    def delete_synthetic(self, target: str) -> None:
        # Only the disposable adapter smoke test can call this operation.
        if not target.startswith("MyBrain/credential-smoke-"):
            raise CredentialFailure("CREDENTIAL_DELETE_NOT_ALLOWED")
        if not self.api.CredDeleteW(target, GENERIC, 0) and ctypes.get_last_error() != 1168:
            raise CredentialFailure("SYNTHETIC_CREDENTIAL_DELETE_FAILED")


class CredentialStore:
    """Application boundary exposes only the one MyBrain-owned key."""

    def __init__(self, backend, identity_check=owner_sid):
        self.backend = backend
        self.identity_check = identity_check

    def metadata(self) -> Entry | None:
        self.identity_check()
        entry = self.backend.read(TARGET, include_secret=False)
        if entry is not None:
            self.validate(entry)
        return entry

    @staticmethod
    def validate(entry: Entry) -> None:
        helper = entry.username == MARKER and entry.comment == COMMENT and entry.persist == LOCAL_MACHINE
        manual = entry.username == GUI_USERNAME and entry.comment == "" and entry.persist in (LOCAL_MACHINE, ENTERPRISE)
        if entry.target != TARGET or not (helper or manual):
            raise CredentialFailure("CREDENTIAL_KEY_NOT_MYBRAIN_OWNED")

    def load(self) -> str:
        self.identity_check()
        entry = self.backend.read(TARGET, include_secret=True)
        if entry is None:
            raise CredentialFailure("CREDENTIAL_MISSING_RUN_SETUP")
        self.validate(entry)
        if not isinstance(entry.value, str) or not entry.value:
            raise CredentialFailure("WINDOWS_CREDENTIAL_FORMAT_UNKNOWN")
        return entry.value

    def save(self, secret: str, replace: bool = False) -> None:
        current = self.metadata()
        if current is not None and not replace:
            raise CredentialFailure("CREDENTIAL_REPLACEMENT_NOT_CONFIRMED")
        self.backend.write(TARGET, secret)
