from toolkit_runtime import WORKROOT, runtime_area, private_path, live_connection
"""Shared fixed-origin, payload-admitted REST create exchange; no authentication."""
import hashlib
import json
import preflight as base


def payload_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest()


class RestCreateCommand:
    def __init__(self, client, path, payloads):
        if path not in ("/v1/relation", "/v1/mutation") or not payloads or len(payloads) > (9 if path == "/v1/relation" else 1):
            raise base.app.app.Stop("CREATE_COMMAND_SCOPE_INVALID")
        if path == "/v1/mutation" and any(type(p.get("type")) not in (int, str) or p.get("type") not in (1, "1") for p in payloads):
            raise base.app.app.Stop("CREATE_ONLY_PURCHASE_INVOICE_ALLOWED")
        self.client, self.path = client, path
        self.payloads = {payload_hash(p) for p in payloads}
        self.sent = set()

    def create(self, payload):
        fingerprint = payload_hash(payload)
        if fingerprint not in self.payloads or fingerprint in self.sent:
            raise base.app.app.Stop("CREATE_PAYLOAD_NOT_ADMITTED_OR_ALREADY_SENT")
        if self.client.calls >= 199 or not isinstance(self.client.token, str) or not self.client.token or any(c in self.client.token for c in "\r\n"):
            raise base.app.app.Stop("CREATE_CALL_BUDGET_OR_SESSION")
        self.sent.add(fingerprint)
        self.client.calls += 1
        connection = live_connection(self.client.factory, "api.e-boekhouden.nl", timeout=15,
            context=base.ssl.create_default_context(cafile=base.certifi.where()))
        headers = {"Accept": "application/json", "Content-Type": "application/json",
                   "Authorization": ("Bearer " if self.client.bearer else "") + self.client.token}
        try:
            connection.request("POST", self.path, body=json.dumps(payload).encode(), headers=headers)
            response = connection.getresponse()
            if response.status != 201:
                raise base.app.app.Stop("CREATE_HTTP_" + str(response.status))
            if response.getheader("Content-Type", "").split(";")[0].strip().lower() != "application/json":
                raise base.app.app.Stop("CREATE_RESPONSE_NOT_JSON")
            raw = response.read(1024 * 1024 + 1)
            if len(raw) > 1024 * 1024:
                raise base.app.app.Stop("CREATE_RESPONSE_TOO_LARGE")
            result = json.loads(raw)
            if (not isinstance(result, dict) or not base.app.app.positive_integer(result.get("id"))
                    or (self.path == "/v1/relation" and result.get("code") != payload.get("code"))):
                raise base.app.app.Stop("CREATE_RESPONSE_IDENTITY_UNKNOWN")
            return result["id"]
        except base.app.app.Stop:
            raise
        except Exception:
            raise base.app.app.Stop("CREATE_OUTCOME_UNCERTAIN") from None
        finally:
            connection.close()
