from toolkit_runtime import WORKROOT, runtime_area, live_connection
"""One processed invoice: official REST records and separate App archive bytes."""
import argparse
import hashlib
import http.client
import json
from pathlib import Path
import re
import ssl
import sys
import uuid
from urllib.parse import urlencode

import certifi
import app_probe as app
import probe_rest as rest
from credential_store import CredentialStore, CredentialFailure, WindowsBackend


def invoice_query(number):
    if not isinstance(number, str) or not 1 <= len(number) <= 50 or any(ord(c) < 32 or ord(c) == 127 for c in number):
        raise app.app.Stop("INVOICE_NUMBER_INVALID")
    return "/v1/mutation?" + urlencode({"invoiceNumber": number, "type": 1, "limit": 5, "offset": 0})


class Transport:
    def __init__(self, mode, invoice=None, file_id=None, factory=http.client.HTTPSConnection, command_policy=None, accepted_statuses=None):
        if mode not in ("rest", "app"):
            raise app.app.Stop("INVALID_MODE")
        if accepted_statuses is None:
            self.accepted_statuses = frozenset((200,))
        else:
            try:
                admitted = frozenset(accepted_statuses)
            except TypeError:
                raise app.app.Stop("INVALID_ACCEPTED_HTTP_STATUSES") from None
            if not admitted or any(type(code) is not int or not 200 <= code < 300 for code in admitted):
                raise app.app.Stop("INVALID_ACCEPTED_HTTP_STATUSES")
            self.accepted_statuses = admitted
        self.mode, self.file_id, self.factory = mode, file_id, factory
        if command_policy is not None and mode != "app":
            raise app.app.Stop("COMMAND_POLICY_ONLY_APP")
        self.command_policy = command_policy
        self.query = invoice_query(invoice) if mode == "rest" else None
        self.host = "api.e-boekhouden.nl" if mode == "rest" else "appapi.e-boekhouden.nl"
        self.calls, self.secrets = 0, []

    def allowed(self, method, path, body):
        if self.command_policy is not None:
            return self.command_policy(method, path, body)
        if self.mode == "rest":
            if method == "POST":
                return (path == "/v1/session" and isinstance(body, dict)
                        and set(body) == {"accessToken", "source"} and body["source"] == "MBProbe")
            if method == "DELETE":
                return path == "/v1/session" and body is None
            return method == "GET" and body is None and (path == self.query or
                   bool(re.fullmatch(r"/v1/(mutation|relation|ledger)/[1-9][0-9]*", path)))
        if method == "POST":
            return path == "/api/v4/auth/login" and isinstance(body, dict) and set(body) == {"username", "password"}
        return method == "GET" and body is None and path in (
            "/api/v4/auth/userinfo", "/api/v4/bestanden/bestand/" + str(self.file_id),
            "/api/v4/bestanden/download/" + str(self.file_id))

    def request(self, method, path, body=None, token=None, bearer=False):
        if not self.allowed(method, path, body):
            raise app.app.Stop("EXEMPLAR_REQUEST_NOT_ALLOWED")
        if self.calls >= (1 if self.command_policy is not None else 10 if self.mode == "rest" else 5):
            raise app.app.Stop("EXEMPLAR_CALL_LIMIT")
        if token is not None and (not isinstance(token, str) or not token or "\r" in token or "\n" in token):
            raise app.app.Stop("INVALID_SESSION")
        self.calls += 1
        headers = {"Accept": "application/json"}
        if token:
            self.secrets.append(token)
            headers["Authorization"] = ("Bearer " if bearer or self.mode == "app" else "") + token
        encoded = None
        if body is not None:
            self.secrets.extend(v for k, v in body.items() if k in ("username", "password", "accessToken") and isinstance(v, str))
            encoded = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        binary = self.mode == "app" and path.startswith("/api/v4/bestanden/download/")
        if binary:
            headers["Accept"] = "application/octet-stream,application/pdf,image/png,image/jpeg"
        connection = live_connection(self.factory, self.host, timeout=15, context=ssl.create_default_context(cafile=certifi.where()))
        try:
            connection.request(method, path, body=encoded, headers=headers)
            response = connection.getresponse()
            if method == "DELETE" and response.status == 204:
                return None
            if response.status not in self.accepted_statuses:
                fields = app.error_fields(response, self.secrets) if 400 <= response.status < 500 else {}
                raise app.RequestFailure("HTTP_" + str(response.status), "EXEMPLAR_" + self.mode.upper(), fields)
            if response.status == 204:
                return None
            content_type = response.getheader("Content-Type", "").split(";")[0].strip().lower()
            maximum = 5 * 1024 * 1024 if binary else 1024 * 1024
            raw = response.read(maximum + 1)
            if len(raw) > maximum:
                raise app.app.Stop("EXEMPLAR_RESPONSE_TOO_LARGE")
            if binary:
                return validate_file(raw, content_type)
            if content_type != "application/json":
                raise app.app.Stop("EXEMPLAR_RESPONSE_NOT_JSON")
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError):
                raise app.app.Stop("EXEMPLAR_INVALID_JSON") from None
        except app.app.Stop:
            raise
        except Exception:
            raise app.app.Stop("EXEMPLAR_NETWORK_OR_TLS_FAILURE") from None
        finally:
            connection.close()


def validate_file(raw, content_type):
    formats = [(b"%PDF-", "application/pdf", ".pdf"),
               (b"\x89PNG\r\n\x1a\n", "image/png", ".png"), (b"\xff\xd8\xff", "image/jpeg", ".jpg")]
    for magic, mime, extension in formats:
        if raw.startswith(magic) and content_type in (mime, "application/octet-stream"):
            return {"bytes": raw, "mime": mime, "extension": extension}
    raise app.app.Stop("EXEMPLAR_FILE_TYPE_MISMATCH")


def read_rest_invoice(transport, access, number):
    session = transport.request("POST", "/v1/session", {"accessToken": access, "source": "MBProbe"})
    if not isinstance(session, dict) or not isinstance(session.get("token"), str) or not session["token"]:
        raise app.app.Stop("SESSION_NOT_CONFIRMED")
    token, bearer = session["token"], False
    def get(path):
        nonlocal bearer
        try:
            return transport.request("GET", path, token=token, bearer=bearer)
        except app.RequestFailure as exc:
            if str(exc) != "HTTP_401" or bearer:
                raise
        bearer = True
        return transport.request("GET", path, token=token, bearer=True)
    try:
        listed = get(invoice_query(number))
        if (not isinstance(listed, dict) or not isinstance(listed.get("items"), list)
                or len(listed["items"]) != 1):
            raise app.app.Stop("PURCHASE_INVOICE_NOT_UNIQUE")
        match = listed["items"][0]
        if (not isinstance(match, dict) or not app.app.positive_integer(match.get("id"))
                or match.get("invoiceNumber") != number or str(match.get("type")) != "1"):
            raise app.app.Stop("PURCHASE_INVOICE_MATCH_UNKNOWN")
        detail = get("/v1/mutation/" + str(match["id"]))
        if not isinstance(detail, dict) or detail.get("invoiceNumber") != number or str(detail.get("type")) != "1":
            raise app.app.Stop("PURCHASE_INVOICE_DETAIL_MISMATCH")
        selected = rest.project(detail, match["id"], (access, token))
        result = {"mutation": selected, "archiveLinkVerified": False}
        relation = detail.get("relationId")
        if app.app.positive_integer(relation):
            value = get("/v1/relation/" + str(relation))
            if not isinstance(value, dict) or value.get("id") != relation:
                raise app.app.Stop("RELATION_IDENTITY_MISMATCH")
            result["relation"] = safe_fields(value, ("id", "code", "name", "type", "vatNumber"), (access, token))
        ledgers = {detail.get("ledgerId")} | {row.get("ledgerId") for row in detail["rows"]}
        ledgers = {value for value in ledgers if app.app.positive_integer(value)}
        if len(ledgers) > 4:
            raise app.app.Stop("LEDGER_LOOKUP_SCOPE_EXCEEDED")
        result["ledgers"] = []
        for identifier in sorted(ledgers):
            value = get("/v1/ledger/" + str(identifier))
            if not isinstance(value, dict) or value.get("id") != identifier:
                raise app.app.Stop("LEDGER_IDENTITY_MISMATCH")
            result["ledgers"].append(safe_fields(value, ("id", "code", "description", "category", "group"), (access, token)))
        return result
    finally:
        try:
            transport.request("DELETE", "/v1/session", token=token, bearer=bearer)
            print("Tijdelijke REST-sessie ingetrokken.", flush=True)
        except app.app.Stop:
            print("REST-sessiebeëindiging niet bevestigd.", flush=True)


def safe_fields(value, names, secrets):
    result = {}
    for name in names:
        if name not in value:
            continue
        field = value[name]
        if isinstance(field, str):
            for secret in secrets:
                if secret:
                    field = field.replace(secret, "[REDACTED]")
        elif field is not None and type(field) not in (int, float, bool):
            raise app.app.Stop("EXEMPLAR_METADATA_SHAPE_UNKNOWN")
        result[name] = field
    return result


def read_app_file(transport, login, expected_admin, identifier):
    session = transport.request("POST", "/api/v4/auth/login", {"username": login.username, "password": login.password})
    if not isinstance(session, dict) or session.get("twoFactorCodeRequired") is not False:
        raise app.app.Stop("APP_TWO_FACTOR_OR_FLOW_UNKNOWN")
    if session.get("loginOk") is not True or not isinstance(session.get("token"), str) or not session["token"]:
        raise app.app.Stop("APP_LOGIN_NOT_CONFIRMED")
    token = session["token"]
    admin = app.app.active_administration(transport.request("GET", "/api/v4/auth/userinfo", token=token))
    if admin[0] != expected_admin:
        raise app.app.Stop("ADMINISTRATION_MISMATCH")
    metadata = transport.request("GET", "/api/v4/bestanden/bestand/" + str(identifier), token=token)
    if not isinstance(metadata, dict) or metadata.get("id") != identifier or not isinstance(metadata.get("naam"), str):
        raise app.app.Stop("ARCHIVE_FILE_IDENTITY_MISMATCH")
    expected_mime = {".pdf": "application/pdf", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}.get(Path(metadata["naam"]).suffix.lower())
    if expected_mime is None:
        raise app.app.Stop("ARCHIVE_FILE_EXTENSION_UNSUPPORTED")
    file = transport.request("GET", "/api/v4/bestanden/download/" + str(identifier), token=token)
    if not isinstance(file, dict) or file.get("mime") != expected_mime:
        raise app.app.Stop("ARCHIVE_FILENAME_CONTENT_MISMATCH")
    if app.app.active_administration(transport.request("GET", "/api/v4/auth/userinfo", token=token)) != admin:
        raise app.app.Stop("ADMINISTRATION_CHANGED")
    return file, safe_fields(metadata, ("id", "naam", "datum", "directoryId", "scanStatus"), (login.username, login.password, token))


def main():
    parser = argparse.ArgumentParser(description="Inspect one processed invoice without bookkeeping changes")
    sub = parser.add_subparsers(dest="mode", required=True)
    lookup = sub.add_parser("lookup")
    lookup.add_argument("--invoice-number", required=True)
    download = sub.add_parser("download")
    download.add_argument("--file-id", required=True, type=int)
    download.add_argument("--admin-id", required=True, type=int)
    args = parser.parse_args()
    root = runtime_area("app")
    app.app.protect_directory(root)
    suffix = uuid.uuid4().hex
    if args.mode == "lookup":
        invoice_query(args.invoice_number)
        access = rest.normalize_access_token(CredentialStore(WindowsBackend()).load())
        result = read_rest_invoice(Transport("rest", invoice=args.invoice_number), access, args.invoice_number)
        output = root / ("processed-invoice-" + suffix + ".json")
    else:
        if args.file_id <= 0 or args.admin_id <= 0:
            raise app.app.Stop("INVALID_FILE_SCOPE")
        login = app.load_login(WindowsBackend().api)
        file, metadata = read_app_file(Transport("app", file_id=args.file_id), login, args.admin_id, args.file_id)
        binary_path = root / ("archive-exemplar-" + suffix + file["extension"])
        with binary_path.open("xb") as stream:
            stream.write(file["bytes"])
        result = {"metadata": metadata, "mime": file["mime"], "size": len(file["bytes"]),
                  "sha256": hashlib.sha256(file["bytes"]).hexdigest(), "localFile": binary_path.name,
                  "archiveLinkVerified": False}
        output = root / ("archive-exemplar-" + suffix + ".json")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=True, indent=2, allow_nan=False)
        stream.write("\n")
    print("Privéresultaat:", output, flush=True)


if __name__ == "__main__":
    try:
        main()
    except app.RequestFailure as exc:
        print("Gestopt:", exc.label + "_" + str(exc), "privédetails:", json.dumps(exc.fields, ensure_ascii=True), flush=True)
    except (app.app.Stop, CredentialFailure) as exc:
        print("Gestopt:", str(exc), flush=True)
    except (KeyboardInterrupt, EOFError):
        print("Gestopt: CANCELLED", flush=True)
    except Exception:
        print("Gestopt: EXEMPLAR_LOCAL_FAILURE", flush=True)
    finally:
        if sys.stdin.isatty():
            try:
                input("Druk Enter om dit venster te sluiten.")
            except (KeyboardInterrupt, EOFError):
                pass
