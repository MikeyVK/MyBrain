from toolkit_runtime import WORKROOT, runtime_area, live_connection
"""Bounded App archive metadata probe; no downloads or account writes."""
import argparse
import json
from pathlib import Path
import re
import ssl
import sys
import uuid

import app_probe as core


class ShapeFailure(core.app.Stop):
    def __init__(self, shape):
        super().__init__("ARCHIVE_METADATA_SHAPE_UNKNOWN")
        self.shape = shape


def redact(text, secrets):
    for secret in sorted(secrets, key=len, reverse=True):
        if secret:
            text = text.replace(secret, "[REDACTED]")
    return "".join(ch if ch.isprintable() else "?" for ch in text)[:1000]


def shape_only(value, secrets, depth=0):
    if depth > 2:
        return type(value).__name__
    if isinstance(value, dict):
        return {redact(str(k), secrets)[:80]: shape_only(v, secrets, depth + 1)
                for k, v in list(value.items())[:12]}
    if isinstance(value, list):
        return {"type": "list", "firstItemShape": shape_only(value[0], secrets, depth + 1) if value else "empty"}
    return type(value).__name__


def allowed(method, path, body):
    if method == "POST":
        return (path == "/api/v4/auth/login" and isinstance(body, dict)
                and set(body) == {"username", "password"}
                and all(isinstance(v, str) and v for v in body.values()))
    return method == "GET" and body is None and (path in ("/api/v4/auth/userinfo", "/api/v4/bestanden")
            or bool(re.fullmatch(r"/api/v4/bestanden/[1-9][0-9]*", path)))


class Transport:
    def __init__(self, factory=core.tls_connection):
        self.factory = factory
        self.calls = 0
        self.secrets = []

    def request(self, method, path, body=None, token=None):
        if not allowed(method, path, body):
            raise core.app.Stop("ARCHIVE_REQUEST_NOT_ALLOWED")
        if self.calls >= 6:
            raise core.app.Stop("ARCHIVE_CALL_LIMIT")
        if token is not None and (not isinstance(token, str) or not token or "\r" in token or "\n" in token):
            raise core.app.Stop("INVALID_SESSION")
        self.calls += 1
        headers = {"Accept": "application/json"}
        if token:
            self.secrets.append(token)
            headers["Authorization"] = "Bearer " + token
        data = None
        if body is not None:
            self.secrets.extend(body.values())
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        connection = live_connection(self.factory, "appapi.e-boekhouden.nl", timeout=15, context=ssl.create_default_context())
        try:
            connection.request(method, path, body=data, headers=headers)
            response = connection.getresponse()
            if response.status != 200:
                fields = core.error_fields(response, self.secrets) if 400 <= response.status < 500 else {}
                label = "APP_ARCHIVE_METADATA" if path.startswith("/api/v4/bestanden") else core.request_label(method, path)
                raise core.RequestFailure("HTTP_" + str(response.status), label, fields)
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise core.app.Stop("ARCHIVE_RESPONSE_NOT_JSON")
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise core.app.Stop("ARCHIVE_RESPONSE_TOO_LARGE")
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError):
                raise core.app.Stop("ARCHIVE_RESPONSE_INVALID_JSON") from None
        except core.app.Stop:
            raise
        except Exception:
            raise core.app.Stop("ARCHIVE_NETWORK_OR_TLS_FAILURE") from None
        finally:
            connection.close()


FOLDER_FIELDS = ("id", "naam", "datum", "parentDirectoryId", "isMailEnHerkenInbox", "childCount")
FILE_FIELDS = ("id", "naam", "datum", "directoryId", "scanStatus")


def project_listing(value, secrets):
    def fail():
        raise ShapeFailure(shape_only(value, secrets))
    def metadata(item, fields, root=False):
        if (not isinstance(item, dict) or type(item.get("id")) is not int
                or item["id"] < (0 if root else 1) or not isinstance(item.get("naam"), str)):
            fail()
        result = {}
        for key in fields:
            if key not in item:
                continue
            field = item[key]
            if isinstance(field, str):
                result[key] = redact(field, secrets)
            elif field is None or type(field) in (int, bool):
                result[key] = field
            else:
                fail()
        return result
    if (not isinstance(value, dict) or not isinstance(value.get("directories"), list)
            or not isinstance(value.get("files"), list)
            or len(value["directories"]) + len(value["files"]) > 200):
        fail()
    result = metadata(value, FOLDER_FIELDS, root=True)
    result["directories"] = [metadata(item, FOLDER_FIELDS) for item in value["directories"]]
    result["files"] = [metadata(item, FILE_FIELDS) for item in value["files"]]
    return result


def read_metadata(transport, login, expected_admin, directory=None):
    response = transport.request("POST", "/api/v4/auth/login", {"username": login.username, "password": login.password})
    if not isinstance(response, dict) or response.get("twoFactorCodeRequired") is not False:
        raise core.app.Stop("APP_TWO_FACTOR_OR_FLOW_UNKNOWN")
    if response.get("loginOk") is not True or not isinstance(response.get("token"), str) or not response["token"]:
        raise core.app.Stop("APP_LOGIN_NOT_CONFIRMED")
    token = response["token"]
    admin = core.app.active_administration(transport.request("GET", "/api/v4/auth/userinfo", token=token))
    if admin[0] != expected_admin:
        raise core.app.Stop("ADMINISTRATION_MISMATCH")
    secrets = (login.username, login.password, token)
    root = project_listing(transport.request("GET", "/api/v4/bestanden", token=token), secrets)
    result = {"root": root}
    if directory is not None:
        if directory not in {entry["id"] for entry in root["directories"]}:
            raise core.app.Stop("DIRECTORY_NOT_IN_ROOT_LISTING")
        selected = project_listing(transport.request("GET", "/api/v4/bestanden/" + str(directory), token=token), secrets)
        if selected["id"] != directory:
            raise core.app.Stop("DIRECTORY_IDENTITY_MISMATCH")
        result["selectedDirectory"] = selected
    if core.app.active_administration(transport.request("GET", "/api/v4/auth/userinfo", token=token)) != admin:
        raise core.app.Stop("ADMINISTRATION_CHANGED")
    return result


def main():
    parser = argparse.ArgumentParser(description="Read only App archive root metadata and optional one chosen direct child")
    parser.add_argument("--admin-id", required=True, type=int)
    parser.add_argument("--directory-id", type=int)
    args = parser.parse_args()
    if args.admin_id <= 0 or (args.directory_id is not None and args.directory_id <= 0):
        raise core.app.Stop("INVALID_SCOPE")
    root = runtime_area("app")
    core.app.protect_directory(root)
    login = core.load_login(core.WindowsBackend().api)
    result = read_metadata(Transport(), login, args.admin_id, args.directory_id)
    output = root / ("archive-metadata-" + uuid.uuid4().hex + ".json")
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump({"status": "archive_metadata_read", "listing": result}, stream, ensure_ascii=True, indent=2)
        stream.write("\n")
    print("Archiefmetadata gelezen; privéresultaat:", output, flush=True)
    print("Rootmappen:", len(result["root"]["directories"]), "rootbestanden:", len(result["root"]["files"]), flush=True)


if __name__ == "__main__":
    try:
        if sys.argv[1:2] == ["rename"]:
            from metadata_repair import main as repair_main
            repair_main(["rename"] + sys.argv[2:])
        else:
            main()
    except ShapeFailure as exc:
        print("Gestopt:", str(exc), "structuur:", json.dumps(exc.shape, ensure_ascii=True), flush=True)
    except core.RequestFailure as exc:
        print("Gestopt:", exc.label + "_" + str(exc), "privédetails:", json.dumps(exc.fields, ensure_ascii=True), flush=True)
    except core.app.Stop as exc:
        print("Gestopt:", str(exc), flush=True)
    except (KeyboardInterrupt, EOFError):
        print("Gestopt: CANCELLED", flush=True)
    except Exception:
        print("Gestopt: ARCHIVE_LOCAL_FAILURE", flush=True)
    finally:
        if sys.stdin.isatty():
            try:
                input("Druk Enter om dit venster te sluiten.")
            except (KeyboardInterrupt, EOFError):
                pass
