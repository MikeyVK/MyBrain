"""Private App-v4 credential-backed, one-record feasibility probe."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area, live_connection

import argparse
import ctypes
from datetime import date
from dataclasses import dataclass, field
import http.client
import json
import re
from pathlib import Path
import ssl
import sys
import uuid

import certifi

ROOT = runtime_area("app")
import probe as app
from credential_store import Credential, WindowsBackend, owner_sid

TARGET = "MyBrain/eBoekhouden-App-v4"


class RequestFailure(app.Stop):
    def __init__(self, code, label, fields):
        super().__init__(code)  # Preserve HTTP_404 for the existing fallback.
        self.label = label
        self.fields = fields


def request_label(method, path):
    if method == "POST" and path == "/api/v4/auth/login":
        return "APP_LOGIN"
    if path == "/api/v4/auth/userinfo":
        return "APP_USERINFO"
    if method == "POST" and path == "/api/v4/mutaties/filter":
        return "APP_FILTER_METADATA"
    if path.startswith("/mutaties/search?"):
        return "APP_SEARCH_ROOT"
    if path.startswith("/api/v4/mutaties/search?"):
        return "APP_SEARCH_V4"
    return "APP_MUTATION_DETAIL"


def error_fields(response, secrets):
    """Private transient diagnostics only; redact before limiting text."""
    try:
        raw = response.read(8193)
        if len(raw) > 8192:
            return {}
        value = json.loads(raw)
        if not isinstance(value, dict):
            return {}
        def clean(text):
            for secret in sorted(secrets, key=len, reverse=True):
                if secret:
                    text = text.replace(secret, "[REDACTED]")
            return "".join(ch if ch.isprintable() else "?" for ch in text)[:256]
        result = {}
        for key, text in value.items():
            if not isinstance(key, str):
                continue
            if key.lower() in {"code", "type", "title", "message", "propertyname"} and isinstance(text, str):
                result[key.lower()] = clean(text)
            elif key.lower() == "errors" and isinstance(text, dict):
                errors = {}
                for field, messages in list(text.items())[:8]:
                    if not isinstance(field, str) or not isinstance(messages, list):
                        continue
                    errors[clean(field)] = [clean(message) for message in messages[:3] if isinstance(message, str)]
                result["errors"] = errors
        return result
    except Exception:
        return {}


def filter_body(day, page):
    try:
        if date.fromisoformat(day).isoformat() != day or type(page) is not int or page not in (1, 2):
            raise ValueError()
    except (ValueError, TypeError):
        raise app.Stop("FILTER_SCOPE_INVALID") from None
    return {"page": page, "pageSize": 20,
            "period": {"startDate": day + "T00:00:00", "endDate": day + "T23:59:59"},
            "soort": 0, "sortBy": 0, "sortDirection": 1}


def request_allowed(method, path, body):
    if method == "POST" and path == "/api/v4/auth/login":
        return (isinstance(body, dict) and set(body) == {"username", "password"}
                and all(isinstance(body[k], str) and body[k] for k in body))
    if method == "POST" and path == "/api/v4/mutaties/filter":
        try:
            start = body["period"]["startDate"]
            return (isinstance(start, str) and type(body["page"]) is int
                    and body == filter_body(start[:10], body["page"]))
        except (KeyError, TypeError, app.Stop):
            return False
    return method == "GET" and body is None and (path == "/api/v4/auth/userinfo" or
           bool(re.fullmatch(r"/api/v4/mutaties/[1-9][0-9]*", path)))


class ObservedConnection:
    def __init__(self, connection, observe):
        self.connection = connection
        self.observe = observe

    def request(self, method, path, **kwargs):
        return self.connection.request(method, path, **kwargs)

    def getresponse(self):
        response = self.connection.getresponse()
        self.observe(response)
        return response

    def close(self):
        self.connection.close()


class Transport(app.Transport):
    def __init__(self, factory=None):
        self.base_factory = factory if factory is not None else tls_connection
        self.diagnostic_fields = {}
        self.secrets = []
        super().__init__(self.make_connection)

    def make_connection(self, *args, **kwargs):
        return ObservedConnection(self.base_factory(*args, **kwargs), self.observe)

    def observe(self, response):
        if 400 <= response.status < 500:
            self.diagnostic_fields = error_fields(response, self.secrets)

    def request(self, method, path, body=None, token=None):
        self.diagnostic_fields = {}
        if not request_allowed(method, path, body):
            raise app.Stop("REQUEST_NOT_ALLOWED")
        if self.calls >= 8:
            raise app.Stop("CALL_LIMIT")
        if token is not None and (not isinstance(token, str) or not token or "\r" in token or "\n" in token):
            raise app.Stop("INVALID_SESSION")
        if isinstance(body, dict):
            for key in ("username", "password"):
                if isinstance(body.get(key), str):
                    self.secrets.append(body[key])
        if isinstance(token, str):
            self.secrets.append(token)
        self.calls += 1
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = "Bearer " + token
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        connection = self.make_connection("appapi.e-boekhouden.nl", timeout=15,
                                          context=ssl.create_default_context())
        try:
            connection.request(method, path, body=data, headers=headers)
            response = connection.getresponse()
            if response.status != 200:
                raise RequestFailure("HTTP_" + str(response.status), request_label(method, path), self.diagnostic_fields)
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise app.Stop("RESPONSE_NOT_JSON")
            raw = response.read(app.MAX_BYTES + 1)
            if len(raw) > app.MAX_BYTES:
                raise app.Stop("RESPONSE_TOO_LARGE")
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError):
                raise app.Stop("INVALID_JSON") from None
        except app.Stop:
            raise
        except Exception:
            raise app.Stop("NETWORK_OR_TLS_FAILURE") from None
        finally:
            connection.close()


@dataclass(frozen=True)
class Login:
    username: str = field(repr=False)
    password: str = field(repr=False)


def decode_login(username: str, comment: str, persist: int, raw: bytes) -> Login:
    if (not isinstance(username, str) or not username or username != username.strip()
            or len(username) > 256 or any(ord(ch) < 32 or ord(ch) == 127 for ch in username)
            or comment != "" or persist not in (2, 3)):
        raise app.Stop("APP_CREDENTIAL_METADATA_UNKNOWN")
    try:
        password = raw.decode("utf-16-le")
    except UnicodeError:
        raise app.Stop("APP_CREDENTIAL_ENCODING_UNKNOWN") from None
    if not password or any(ord(ch) < 32 or ord(ch) == 127 for ch in password):
        raise app.Stop("APP_CREDENTIAL_PASSWORD_INVALID")
    return Login(username, password)


def load_login(api) -> Login:
    owner_sid()
    pointer = ctypes.POINTER(Credential)()
    if not api.CredReadW(TARGET, 1, 0, ctypes.byref(pointer)):
        if ctypes.get_last_error() == 1168:
            raise app.Stop("APP_CREDENTIAL_MISSING")
        raise app.Stop("APP_CREDENTIAL_READ_FAILED")
    try:
        entry = pointer.contents
        if (entry.Type != 1 or entry.TargetName != TARGET or not entry.CredentialBlob
                or not 0 < entry.CredentialBlobSize <= 2560):
            raise app.Stop("APP_CREDENTIAL_FORMAT_UNKNOWN")
        return decode_login(entry.UserName or "", entry.Comment or "", entry.Persist,
                            ctypes.string_at(entry.CredentialBlob, entry.CredentialBlobSize))
    finally:
        entry = pointer.contents
        if entry.CredentialBlob and 0 < entry.CredentialBlobSize <= 2560:
            ctypes.memset(entry.CredentialBlob, 0, entry.CredentialBlobSize)
        api.CredFree(pointer)


def tls_connection(host, timeout, context):
    if host != "appapi.e-boekhouden.nl" or not context.check_hostname or context.verify_mode != ssl.CERT_REQUIRED:
        raise app.Stop("TLS_OR_HOST_CONFIGURATION_INVALID")
    return live_connection(http.client.HTTPSConnection, host, timeout=timeout,
                                      context=ssl.create_default_context(cafile=certifi.where()))


def read_filtered_one(transport, reader, token, number, day, admin):
    matches = []
    seen = set()
    for page in (1, 2):
        result = transport.request("POST", "/api/v4/mutaties/filter", filter_body(day, page), token=token)
        if (not isinstance(result, dict) or type(result.get("currentPage")) is not int
                or result["currentPage"] != page or result.get("pageSize") != 20
                or type(result.get("hasMoreRows")) is not bool
                or not isinstance(result.get("items"), list) or len(result["items"]) > 20):
            raise app.Stop("FILTER_RESULT_SHAPE_UNKNOWN")
        for item in result["items"]:
            if (not isinstance(item, dict) or not app.positive_integer(item.get("id"))
                    or type(item.get("mutatieNummer")) is not int
                    or not isinstance(item.get("datum"), str) or item["datum"][:10] != day
                    or item["id"] in seen):
                raise app.Stop("FILTER_RESULT_SCOPE_OR_IDENTITY_UNKNOWN")
            seen.add(item["id"])
            if item["mutatieNummer"] == number:
                matches.append(item)
        if not result["hasMoreRows"]:
            break
    else:
        raise app.Stop("FILTER_SCOPE_EXCEEDS_TWO_PAGES")
    if len(matches) != 1:
        raise app.Stop("FILTER_EXACT_MATCH_NOT_UNIQUE")
    if app.active_administration(reader.get("/api/v4/auth/userinfo")) != admin:
        raise app.Stop("ADMINISTRATION_CHANGED")
    detail = reader.get("/api/v4/mutaties/" + str(matches[0]["id"]))
    if (not isinstance(detail, dict) or detail.get("id") != matches[0]["id"]
            or detail.get("mutatieNummer") != number or not isinstance(detail.get("datum"), str)
            or detail["datum"][:10] != day):
        raise app.Stop("DETAIL_IDENTITY_MISMATCH")
    if app.active_administration(reader.get("/api/v4/auth/userinfo")) != admin:
        raise app.Stop("ADMINISTRATION_CHANGED")
    return detail


def read_selected(transport, login: Login, number: int, day: str, confirm_admin) -> dict:
    response = transport.request("POST", "/api/v4/auth/login",
                                 {"username": login.username, "password": login.password})
    if not isinstance(response, dict) or response.get("twoFactorCodeRequired") is not False:
        raise app.Stop("APP_TWO_FACTOR_OR_FLOW_UNKNOWN")
    if response.get("loginOk") is not True or not isinstance(response.get("token"), str) or not response["token"]:
        raise app.Stop("APP_LOGIN_NOT_CONFIRMED")
    token = response["token"]
    reader = app.SessionReader(transport, token)
    admin = app.active_administration(reader.get("/api/v4/auth/userinfo"))
    if not confirm_admin(admin):
        raise app.Stop("ADMINISTRATION_NOT_CONFIRMED")
    detail = read_filtered_one(transport, reader, token, number, day, admin)
    selected = app.project_record(detail, (login.username, login.password, token))
    del token, reader, response, detail
    return selected


def confirm_admin(admin) -> bool:
    print("Actieve App-administratie:", json.dumps({"id": admin[0], "naam": admin[1]}, ensure_ascii=True), flush=True)
    return input("Is dit de bedoelde administratie? Typ JA, anders stopt de proef: ").strip() == "JA"


def main() -> None:
    parser = argparse.ArgumentParser(description="Read one App API v4 mutation using a distinct Windows credential")
    parser.add_argument("--number", type=int, required=True)
    parser.add_argument("--date", required=True, help="Known ISO date of the selected mutation; bounds metadata lookup to one day")
    args = parser.parse_args()
    if not 1 <= args.number <= 2147483647:
        raise app.Stop("INVALID_MUTATION_NUMBER")
    filter_body(args.date, 1)
    # Requires a real owner PTY for the administration confirmation; no secrets
    # are typed into this process. The Windows GUI is the sole setup path.
    app.protect_directory(ROOT)
    login = load_login(WindowsBackend().api)
    transport = Transport()
    selected = read_selected(transport, login, args.number, args.date, confirm_admin)
    output = ROOT / ("selected-app-mutation-" + uuid.uuid4().hex + ".json")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"status": "selected_record_read", "mutation": selected}, stream,
                  ensure_ascii=True, indent=2, allow_nan=False)
        stream.write("\n")
    print("Eén App-mutatie gelezen. Privéresultaat:", output, flush=True)
    print("App-sessie alleen in procesgeheugen; er is geen gedocumenteerde logout aangeroepen.", flush=True)
    del login, selected, transport


if __name__ == "__main__":
    try:
        main()
    except RequestFailure as exc:
        print("Gestopt:", exc.label + "_" + str(exc), flush=True)
        if exc.fields:
            print("Privé foutdetails:", json.dumps(exc.fields, ensure_ascii=True), flush=True)
    except app.Stop as exc:
        print("Gestopt:", str(exc), flush=True)
    except (KeyboardInterrupt, EOFError):
        print("Gestopt: CANCELLED", flush=True)
    except Exception:
        print("Gestopt: APP_LOCAL_FAILURE", flush=True)
    finally:
        if sys.stdin.isatty():
            try:
                input("Druk Enter om dit venster te sluiten.")
            except (KeyboardInterrupt, EOFError):
                pass
