"""Private, bounded research probe. No import-time I/O and no accounting writes."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area, live_connection

import csv
import ctypes
import getpass
import http.client
import io
import json
import os
from pathlib import Path
import re
import ssl
import stat
import subprocess
import sys
from typing import Callable, Protocol
from urllib.parse import urlencode
import warnings

HOST = "appapi.e-boekhouden.nl"
MAX_CALLS = 8
MAX_BYTES = 1024 * 1024
SEARCH_PATHS = ("/mutaties/search", "/api/v4/mutaties/search")


class Stop(Exception):
    """A safe failure code; never attach payloads, URLs or vendor error text."""


class Reader(Protocol):
    def get(self, path: str) -> object: ...


def allowed(method: str, path: str) -> bool:
    if method == "POST":
        return path == "/api/v4/auth/login"
    if method != "GET":
        return False
    return path == "/api/v4/auth/userinfo" or bool(
        re.fullmatch(r"/api/v4/mutaties/[1-9][0-9]*", path)
        or any(re.fullmatch(re.escape(p) + r"\?mutatienummer=[1-9][0-9]*", path)
               for p in SEARCH_PATHS)
    )


class Transport:
    """Fixed-origin HTTPS transport; no proxies, redirects, cookies or retry."""

    def __init__(self, connection_factory: Callable = http.client.HTTPSConnection):
        self.connection_factory = connection_factory
        self.calls = 0

    def request(self, method: str, path: str, body: object = None,
                token: str | None = None) -> object:
        if not allowed(method, path) or (method == "GET" and body is not None):
            raise Stop("REQUEST_NOT_ALLOWED")
        if self.calls >= MAX_CALLS:
            raise Stop("CALL_LIMIT")
        if token is not None and (not token or "\r" in token or "\n" in token):
            raise Stop("INVALID_SESSION")
        self.calls += 1
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        encoded = None
        if body is not None:
            encoded = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        conn = live_connection(self.connection_factory, HOST, timeout=15,
                                       context=ssl.create_default_context())
        try:
            conn.request(method, path, body=encoded, headers=headers)
            response = conn.getresponse()
            if response.status != 200:
                # Do not read or disclose an error body or Location header.
                raise Stop("HTTP_" + str(response.status))
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise Stop("RESPONSE_NOT_JSON")
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise Stop("RESPONSE_TOO_LARGE")
            try:
                return json.loads(data)
            except (ValueError, UnicodeError):
                raise Stop("INVALID_JSON") from None
        except Stop:
            raise
        except Exception:
            # Network/TLS exception messages can contain request context.
            raise Stop("NETWORK_OR_TLS_FAILURE") from None
        finally:
            conn.close()


class SessionReader:
    """Expose GET only after session authentication."""

    def __init__(self, transport: Transport, token: str):
        self.transport = transport
        self.token = token

    def get(self, path: str) -> object:
        return self.transport.request("GET", path, token=self.token)


def positive_integer(value: object) -> bool:
    return type(value) is int and value > 0


def active_administration(value: object) -> tuple[int, str]:
    if not isinstance(value, dict) or value.get("valid") is not True:
        raise Stop("INVALID_USER_CONTEXT")
    admin = value.get("currentAdministratie")
    if not isinstance(admin, dict) or not positive_integer(admin.get("id")):
        raise Stop("ACTIVE_ADMINISTRATION_UNKNOWN")
    name = admin.get("naam")
    if not isinstance(name, str) or not name.strip() or len(name) > 300:
        raise Stop("ACTIVE_ADMINISTRATION_UNKNOWN")
    return admin["id"], name


def candidates(value: object, visible_number: int) -> list[dict]:
    # Search has no published response schema. Recognize only these narrow
    # possible collection envelopes; unexpected shapes stop, never guess an ID.
    rows = value.get("mutaties") if isinstance(value, dict) else value
    if not isinstance(rows, list) or len(rows) > 20:
        raise Stop("SEARCH_SHAPE_OR_SCOPE_UNKNOWN")
    matches = []
    for row in rows:
        if not isinstance(row, dict):
            raise Stop("SEARCH_SHAPE_OR_SCOPE_UNKNOWN")
        if row.get("mutatieNummer") == visible_number:
            if not positive_integer(row.get("id")) or not isinstance(row.get("datum"), str):
                raise Stop("SEARCH_IDENTITY_UNKNOWN")
            matches.append(row)
    if not matches:
        raise Stop("NO_EXACT_MUTATION_MATCH")
    if len({r["id"] for r in matches}) != len(matches):
        raise Stop("DUPLICATE_SEARCH_IDENTITIES")
    return matches


def read_one(reader: Reader, visible_number: int, admin: tuple[int, str],
             choose: Callable[[list[dict]], int]) -> dict:
    result = None
    for path in SEARCH_PATHS:
        try:
            result = reader.get(path + "?" + urlencode({"mutatienummer": visible_number}))
            break
        except Stop as exc:
            if str(exc) != "HTTP_404":
                raise
    if result is None:
        raise Stop("SEARCH_ROUTE_UNCONFIRMED")
    rows = candidates(result, visible_number)
    index = 0 if len(rows) == 1 else choose(rows)
    if type(index) is not int or not 0 <= index < len(rows):
        raise Stop("SELECTION_CANCELLED")
    selected = rows[index]
    if active_administration(reader.get("/api/v4/auth/userinfo")) != admin:
        raise Stop("ADMINISTRATION_CHANGED")
    detail = reader.get("/api/v4/mutaties/" + str(selected["id"]))
    if not isinstance(detail, dict) or detail.get("id") != selected["id"] or detail.get("mutatieNummer") != visible_number:
        raise Stop("DETAIL_IDENTITY_MISMATCH")
    if active_administration(reader.get("/api/v4/auth/userinfo")) != admin:
        raise Stop("ADMINISTRATION_CHANGED")
    return detail


def project_record(detail: dict, secrets: tuple[str, ...]) -> dict:
    def clean(value: object) -> object:
        if isinstance(value, str):
            for secret in secrets:
                if secret:
                    value = value.replace(secret, "[REDACTED]")
            return value
        if value is None or type(value) in (bool, int, float):
            return value
        raise Stop("DETAIL_FIELD_SHAPE_UNKNOWN")
    fields = ("id", "mutatieNummer", "factuurNummer", "relatieId", "datum",
              "bedrag", "boekstuk", "omschrijving", "soort",
              "grootboekRekeningOmschrijving", "grootboekRekeningId",
              "isInclusiefBtw", "termijnInDagen")
    result = {k: clean(detail[k]) for k in fields if k in detail}
    rows = detail.get("mutatieRegels")
    if not isinstance(rows, list) or len(rows) > 500:
        raise Stop("DETAIL_ROWS_UNKNOWN")
    row_fields = ("index", "tegenRekeningId", "btwCode", "bedrag", "btw",
                  "omschrijving", "bedragInclusief", "bedragExclusief",
                  "btwCodeDisplayName", "tegenrekeningDisplayName")
    result["mutatieRegels"] = []
    for row in rows:
        if not isinstance(row, dict):
            raise Stop("DETAIL_ROWS_UNKNOWN")
        result["mutatieRegels"].append({k: clean(row[k]) for k in row_fields if k in row})
    return result


def set_private_acl(root: Path, user_sids: tuple[str, ...]) -> None:
    """Set DACL only; do not read/change SACL or require audit privilege."""
    from toolkit_runtime import ensure_private_directory
    from toolkit_runtime import require_live_config
    from toolkit_runtime import private_path
    private_path(root)
    require_live_config()
    ensure_private_directory(root)
    if not user_sids or any(not re.fullmatch(r"S-1-[0-9-]+", s) for s in user_sids):
        raise Stop("PRIVATE_ACL_SETUP_FAILED")
    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    convert = advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW
    convert.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32,
                        ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p]
    convert.restype = ctypes.c_int
    apply = advapi.SetFileSecurityW
    apply.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_void_p]
    apply.restype = ctypes.c_int
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    sddl = "D:P(A;OICI;FA;;;SY)" + "".join("(A;OICI;FA;;;" + s + ")" for s in user_sids)
    descriptor = ctypes.c_void_p()
    if not convert(sddl, 1, ctypes.byref(descriptor), None):
        raise Stop("PRIVATE_ACL_SETUP_FAILED")
    try:
        if not apply(str(root), 0x80000004, descriptor):
            raise Stop("PRIVATE_ACL_SETUP_FAILED")
    finally:
        kernel.LocalFree(descriptor)


def protect_directory(root: Path) -> None:
    """Replace DACL with actual interactive user and SYSTEM before any secrets."""
    from toolkit_runtime import ensure_private_directory
    if sys.platform != "win32" or not sys.stdin.isatty() or not sys.stdout.isatty():
        raise Stop("INTERACTIVE_WINDOWS_CONSOLE_REQUIRED")
    from toolkit_runtime import require_live_config
    require_live_config()
    ensure_private_directory(root)
    if root.is_symlink() or root.stat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise Stop("UNSAFE_OUTPUT_DIRECTORY")
    identity = subprocess.run(["whoami.exe", "/user", "/fo", "csv", "/nh"],
                              capture_output=True, text=True, check=True)
    fields = next(csv.reader(io.StringIO(identity.stdout)))
    if "codexsandbox" in fields[0].lower() or not re.fullmatch(r"S-1-[0-9-]+", fields[1]):
        raise Stop("OWNER_CONSOLE_REQUIRED")
    set_private_acl(root, (fields[1],))


def hidden(prompt: str) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        try:
            value = getpass.getpass(prompt)
        except (getpass.GetPassWarning, EOFError):
            raise Stop("SECURE_INPUT_UNAVAILABLE") from None
    if not value or len(value) > 4096:
        raise Stop("EMPTY_OR_INVALID_INPUT")
    return value
