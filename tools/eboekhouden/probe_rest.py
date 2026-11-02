"""Private feasibility probe for one official REST mutation; no financial writes."""
from __future__ import annotations
from toolkit_runtime import WORKROOT, runtime_area, live_connection

import http.client
import argparse
import json
from pathlib import Path
import re
import ssl
import sys
import uuid

import certifi

# Reuse only local, separately reviewed secure-input and DACL helpers.
from probe import Stop, hidden, protect_directory, set_private_acl

HOST = "api.e-boekhouden.nl"
MAX_CALLS = 5
MAX_BYTES = 1024 * 1024


def stage(method: str, path: str) -> str:
    if path == "/v1/session":
        return "SESSION" if method == "POST" else "SESSION_CLOSE"
    return "MUTATION"


def safe_http_error(response, operation: str) -> str:
    """Return only public enumerated diagnostics; never echo vendor text."""
    summary = operation + "_HTTP_" + str(response.status)
    try:
        raw = response.read(16385)
        if len(raw) > 16384:
            return summary
        value = json.loads(raw)
        if not isinstance(value, dict):
            return summary
        fields = {k.lower(): v for k, v in value.items() if isinstance(k, str)}
        code = fields.get("code")
        if isinstance(code, str) and code in {"API_SESSION_001", "API_SESSION_002", "API_SESSION_003", "API_SESSION_004"}:
            summary += "|code=" + code
        kind = fields.get("type")
        if isinstance(kind, str) and kind in {"validation", "security"}:
            summary += "|type=" + kind
        prop = fields.get("propertyname")
        if isinstance(prop, str) and prop in {"accessToken", "source", "id"}:
            summary += "|property=" + prop
    except Exception:
        pass
    return summary


def normalize_access_token(value: str) -> str:
    token = value.strip()
    if not token or any(ch.isspace() or ord(ch) < 32 or ord(ch) == 127 for ch in token):
        raise Stop("TOKEN_INPUT_INVALID_WHITESPACE_OR_CONTROL")
    return token


def allowed(method: str, path: str) -> bool:
    return ((method in ("POST", "DELETE") and path == "/v1/session")
            or (method == "GET" and bool(re.fullmatch(r"/v1/mutation/[1-9][0-9]*", path))))


class Transport:
    def __init__(self, factory=http.client.HTTPSConnection):
        self.factory = factory
        self.calls = 0

    def request(self, method: str, path: str, body=None, token=None, bearer=False):
        if not allowed(method, path) or (method != "POST" and body is not None):
            raise Stop("REQUEST_NOT_ALLOWED")
        if self.calls >= MAX_CALLS:
            raise Stop("CALL_LIMIT")
        if token is not None and (not isinstance(token, str) or not token or "\r" in token or "\n" in token):
            raise Stop("INVALID_SESSION")
        self.calls += 1
        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = ("Bearer " if bearer else "") + token
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        # Existing runtime Mozilla CA bundle; preserve full chain and hostname
        # verification without modifying Windows trust or disabling TLS checks.
        connection = live_connection(self.factory, HOST, timeout=15,
                                  context=ssl.create_default_context(cafile=certifi.where()))
        try:
            connection.request(method, path, body=data, headers=headers)
            response = connection.getresponse()
            if method == "DELETE" and response.status == 204:
                return None
            if response.status != 200:
                raise Stop(safe_http_error(response, stage(method, path)))
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise Stop("RESPONSE_NOT_JSON")
            raw = response.read(MAX_BYTES + 1)
            if len(raw) > MAX_BYTES:
                raise Stop("RESPONSE_TOO_LARGE")
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError):
                raise Stop("INVALID_JSON") from None
        except Stop:
            raise
        except ssl.SSLCertVerificationError:
            raise Stop("TLS_CERTIFICATE_VERIFY_FAILED") from None
        except Exception:
            raise Stop("NETWORK_OR_TLS_FAILURE") from None
        finally:
            connection.close()


def project(detail: object, expected_number: int, secrets: tuple[str, ...]) -> dict:
    if not isinstance(detail, dict) or type(detail.get("id")) is not int or detail["id"] != expected_number:
        raise Stop("MUTATION_NUMBER_MISMATCH")
    def scalar(value):
        if isinstance(value, str):
            for secret in secrets:
                if secret:
                    value = value.replace(secret, "[REDACTED]")
            return value
        if value is None or type(value) in (bool, int, float):
            return value
        raise Stop("UNEXPECTED_FIELD_SHAPE")
    header = ("id", "type", "date", "description", "termOfPayment", "ledgerId",
              "relationId", "inExVat", "invoiceNumber", "entryNumber")
    result = {key: scalar(detail[key]) for key in header if key in detail}
    collections = {
        "rows": ("ledgerId", "vatCode", "vatAmount", "costCenterId", "amount",
                 "description", "invoiceNumber", "relationId"),
        "vat": ("vatCode", "amount"),
    }
    for key, fields in collections.items():
        rows = detail.get(key)
        if not isinstance(rows, list) or len(rows) > 500:
            raise Stop("UNEXPECTED_COLLECTION_SHAPE")
        result[key] = []
        for row in rows:
            if not isinstance(row, dict):
                raise Stop("UNEXPECTED_COLLECTION_SHAPE")
            result[key].append({k: scalar(row[k]) for k in fields if k in row})
    return result


def read_record(transport, token: str, number: int) -> tuple[object, bool]:
    # Official response prose prescribes a raw token; the security description
    # also mentions Bearer. Retry this GET once on 401 only, never login POST.
    try:
        return transport.request("GET", "/v1/mutation/" + str(number), token=token), False
    except Stop as exc:
        if str(exc).split("|", 1)[0] != "MUTATION_HTTP_401":
            raise
    return transport.request("GET", "/v1/mutation/" + str(number), token=token, bearer=True), True


def main() -> None:
    from credential_store import CredentialStore, WindowsBackend, owner_sid
    parser = argparse.ArgumentParser(description="Read one existing mutation using Windows Credential Manager")
    parser.add_argument("--number", help="Visible mutation number; never supply a token argument")
    args = parser.parse_args()
    root = runtime_area("rest")
    sid = owner_sid()
    set_private_acl(root, (sid,))
    output = root / ("selected-mutation-" + uuid.uuid4().hex + ".json")
    print("Officiële REST API, alleen één bestaande mutatie lezen.")
    number_text = (args.number if args.number is not None else input("Zichtbaar mutatienummer: ")).strip()
    if not re.fullmatch(r"[1-9][0-9]{0,9}", number_text) or int(number_text) > 2147483647:
        raise Stop("INVALID_MUTATION_NUMBER")
    access_token = normalize_access_token(CredentialStore(WindowsBackend()).load())
    transport = Transport()
    session = transport.request("POST", "/v1/session", {"accessToken": access_token, "source": "MBProbe"})
    if not isinstance(session, dict) or not isinstance(session.get("token"), str) or not session["token"]:
        raise Stop("SESSION_NOT_CONFIRMED")
    token = session["token"]
    bearer = False
    try:
        if type(session.get("expiresIn")) is not int or session["expiresIn"] <= 0:
            raise Stop("SESSION_EXPIRY_UNKNOWN")
        detail, bearer = read_record(transport, token, int(number_text))
        selected = project(detail, int(number_text), (access_token, token))
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump({"status": "selected_record_read", "mutation": selected}, stream,
                      ensure_ascii=True, indent=2, allow_nan=False)
            stream.write("\n")
        print("Eén bestaande mutatie opgehaald. Privébestand:", output)
        print(json.dumps(selected, ensure_ascii=True, indent=2))
    finally:
        try:
            transport.request("DELETE", "/v1/session", token=token, bearer=bearer)
            print("Tijdelijke API-sessie ingetrokken.")
        except Stop:
            print("Sessiebeëindiging niet bevestigd; sessie kan tot de serververvaldatum blijven bestaan.")
    del token, session, access_token


if __name__ == "__main__":
    from credential_store import CredentialFailure
    try:
        main()
    except (Stop, CredentialFailure) as exc:
        print("Gestopt:", str(exc))
    except (KeyboardInterrupt, EOFError):
        print("Gestopt: CANCELLED")
    except Exception:
        print("Gestopt: LOCAL_FAILURE (geen gevoelige details gelogd)")
    finally:
        if sys.stdin.isatty():
            try:
                input("Druk Enter om dit venster te sluiten.")
            except (EOFError, KeyboardInterrupt):
                pass
