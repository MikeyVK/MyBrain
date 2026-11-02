from toolkit_runtime import WORKROOT, runtime_area
"""Bounded full identity coverage of the REST-exposed relation catalogue."""
import argparse
import json
from pathlib import Path
import uuid
import catalogue_match as prior

base = prior.base
# Process-local bound for the unchanged reviewed transport; no shared-file edit.
base.MAX_CALLS = 510
KEYS = ("id", "code", "name", "type", "country", "address", "postalCode", "city",
        "emailAddress", "website", "vatNumber", "companyRegistrationNumber", "inactive", "termOfPayment")


class Client(base.Client):
    def __init__(self, factory=base.http.client.HTTPSConnection):
        super().__init__([], {"acceptedAmazonCentralCode": "unused"}, factory)
        self.paths = {base.query("/v1/relation", limit=1000, offset=0)}

    def detail(self, kind, identifier):
        if kind != "relation" or identifier not in self.admitted_ids:
            raise base.app.app.Stop("FULL_NAMES_DETAIL_SCOPE_DENIED")
        return super().detail(kind, identifier)


def collect(client, profiles, plan):
    catalogue, complete, reason = base.complete_pages(client.get,
        lambda offset: base.query("/v1/relation", limit=1000, offset=offset), 1000, 1)
    if not complete or len(catalogue) > 500:
        raise base.app.app.Stop("FULL_NAMES_CATALOGUE_EXCEEDS_BOUND_OR_INCOMPLETE")
    if any(row.get("type") not in ("B", "P") or not isinstance(row.get("code"), str) or not row["code"] for row in catalogue):
        raise base.app.app.Stop("FULL_NAMES_CATALOGUE_SHAPE_UNKNOWN")
    client.admitted_ids = {row["id"] for row in catalogue}
    details = []
    for index, item in enumerate(catalogue, 1):
        value = client.detail("relation", item["id"])
        if value.get("code") != item["code"] or value.get("type") != item["type"]:
            raise base.app.app.Stop("FULL_NAMES_CATALOGUE_IDENTITY_CHANGED")
        details.append({key: value.get(key) for key in KEYS})
        if index % 50 == 0:
            print("Volledige relatiedetails gelezen:", index, "van", len(catalogue), flush=True)
    groups = []
    by_supplier = {p["sourceSupplierLabel"]: p for p in profiles["proposals"]}
    for group in plan["groups"]:
        profile = by_supplier[group["supplier"]]
        candidates = []
        for detail in details:
            evidence = prior.identity_evidence(profile, detail)
            names = base.normalize(str(detail.get("name") or "") + " " + detail["code"])
            fragments = [f for f in group["codeFragments"] if base.normalize(f) in names]
            if fragments or evidence["strength"] != "weak_code_or_alias_candidate_requires_review":
                candidates.append({"candidate": detail, "identityEvidence": evidence, "nameOrCodeFragments": fragments})
        groups.append({"supplierOriginal": group["supplier"], "candidates": candidates,
                       "automaticMatchPerformed": False, "ownerConfirmedExisting": group.get("ownerConfirmedExists", False)})
    return {"status": "READ_ONLY_FULL_REST_RELATION_IDENTITY_COVERAGE", "catalogueCount": len(catalogue),
            "detailCount": len(details), "allReturnedRelationNamesCovered": True,
            "allReturnedBusinessAndPrivateTypesCovered": True, "relations": details, "supplierGroups": groups,
            "caveat": "Coverage applies only to relations returned by official REST; no documented inactive filter or active-only default. No claim of global absence or automatic mapping.",
            "noNewRelationsCreated": True, "noFinancialOrRegisterWrites": True}
