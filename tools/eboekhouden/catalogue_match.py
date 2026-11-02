from toolkit_runtime import WORKROOT, runtime_area
"""Complete base relation metadata and bounded source-identity candidate review."""
import argparse
import hashlib
import json
from pathlib import Path
import uuid

import preflight as base


class Client(base.Client):
    def __init__(self, factory=base.http.client.HTTPSConnection):
        super().__init__([], {"acceptedAmazonCentralCode": "unused"}, factory)
        self.paths = {base.query("/v1/relation", limit=1000, offset=offset) for offset in range(0, 5000, 1000)}

    def request(self, method, path, body=None):
        logout = method == "DELETE" and path == "/v1/session"
        if self.calls >= 120 or (not logout and self.calls >= 119):
            raise base.app.app.Stop("CATALOGUE_MATCH_CALL_BUDGET")
        if method == "GET" and not path.startswith("/v1/relation"):
            raise base.app.app.Stop("CATALOGUE_MATCH_SCOPE_DENIED")
        return super().request(method, path, body)


def shortlist(catalogue, groups, prior):
    previous = {g["supplierOriginal"]: {c["id"] for c in g["candidates"]} for g in prior["groups"]}
    ranked = {}
    for group in groups:
        scores = []
        for item in catalogue:
            code = base.normalize(item["code"])
            matched = [term for term in group["codeFragments"] if base.normalize(term) in code]
            historical = item["id"] in previous.get(group["supplier"], set())
            if matched or historical:
                score = max((len(base.normalize(t)) for t in matched), default=0)
                scores.append({"id": item["id"], "code": item["code"], "codeFragments": matched,
                               "priorNameFilterCandidate": historical, "score": score})
        ranked[group["supplier"]] = sorted(scores, key=lambda x: (-x["score"], x["code"], x["id"]))
    selected = []
    for index in range(max((len(v) for v in ranked.values()), default=0)):
        for candidates in ranked.values():
            if index < len(candidates) and candidates[index]["id"] not in selected:
                if len(selected) < 100:
                    selected.append(candidates[index]["id"])
    return ranked, selected


def identity_evidence(profile, candidate):
    pairs = [("vatNumber", "vatNumber"), ("companyRegistrationNumber", "companyRegistrationNumber"),
             ("address", "address"), ("postalCode", "postalCode"), ("city", "city")]
    evidence = {}
    for source, target in pairs:
        a, b = profile.get(source), candidate.get(target)
        evidence[source] = "same" if a and b and base.normalize(a) == base.normalize(b) else "different" if a and b else "unavailable"
    names = [profile.get("displayName"), profile.get("legalName"), profile.get("brandName")]
    evidence["name"] = "exact_source_name" if any(n and base.normalize(n) == base.normalize(candidate.get("name")) for n in names) else "not_exact_or_missing"
    email, domain = profile.get("emailAddress"), candidate.get("emailAddress")
    evidence["email"] = "same" if email and domain and email.casefold() == domain.casefold() else "different" if email and domain else "unavailable"
    if evidence["vatNumber"] == "same" or evidence["companyRegistrationNumber"] == "same":
        strength = "strong_existing_identity_candidate"
    elif evidence["name"] == "exact_source_name" and evidence["postalCode"] == "same" and evidence["address"] == "same":
        strength = "strong_name_address_candidate"
    elif evidence["name"] == "exact_source_name":
        strength = "existing_exact_name_candidate"
    else:
        strength = "weak_code_or_alias_candidate_requires_review"
    return {"strength": strength, "comparisons": evidence, "inactive": candidate.get("inactive"), "automaticMatch": False}


def filter_control(client, candidate):
    checks = []
    for field in ("name", "code"):
        value = candidate.get(field)
        if not isinstance(value, str) or not value:
            continue
        path = base.query("/v1/relation", **{field: value, "limit": 20, "offset": 0})
        client.paths.add(path)
        result = client.get(path)
        rows = result.get("items") if isinstance(result, dict) else None
        checks.append({"field": field, "knownExistingIdReturned": isinstance(rows, list) and any(isinstance(row, dict) and row.get("id") == candidate["id"] for row in rows),
                       "responseShapeValid": isinstance(rows, list) and len(rows) <= 20})
    return {"checks": checks, "noAbsenceInferenceFromFailure": True}



def checked(path, expected):
    """Dependency-required hash-bound local JSON read; no batch orchestration."""
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        raise base.app.app.Stop("CATALOGUE_INPUT_FINGERPRINT_CHANGED")
    return json.loads(raw)
