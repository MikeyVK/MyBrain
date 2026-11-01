"""Shared private result/journal presentation; no credential/profile dumps."""
import json
import os
from pathlib import Path
import uuid


def screened(value, secrets=()):
    if isinstance(value, dict):
        return {str(k): screened(v, secrets) for k, v in value.items()
                if str(k).lower() not in {"token", "accesstoken", "password", "authorization", "secrets", "login"}}
    if isinstance(value, list):
        return [screened(v, secrets) for v in value]
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[REDACTED]")
        return "".join(c for c in value if c >= " " or c in "\n\t")
    return value


class PrivateOutput:
    def __init__(self, root, secrets=(), path_validator=None):
        from toolkit_runtime import private_path
        self._validate = path_validator or private_path
        self.root = self._validate(Path(root))
        self.secrets = secrets

    def note(self, text):
        print(screened(text, self.secrets), flush=True)

    def save(self, prefix, value):
        path = self.root / (prefix + "-" + uuid.uuid4().hex + ".json")
        self._validate(path)
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(screened(value, self.secrets), stream, ensure_ascii=True, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        return path

    def append(self, path, value):
        # A complete durable pending line MUST exist before any create request.
        self._validate(Path(path))
        with Path(path).open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(screened(value, self.secrets), ensure_ascii=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
