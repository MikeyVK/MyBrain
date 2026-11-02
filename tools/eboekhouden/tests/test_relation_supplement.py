"""Synthetic curated alias-query scope tests; no actual API/credential use."""
import unittest
import relation_supplement as p


def hints(expected=None):
    group = {"supplier": "Synthetic Supplier", "nameTerms": ["Synthetic"], "codeTerms": ["SYNTH"]}
    if expected:
        group["expectedCurrentEntry"] = expected
    return {"groups": [group], "isolatechPolicy": "synthetic policy",
            "positiveControl": {"invoiceNumber": "CONTROL", "expectedMutationId": 7, "type": 1}}


PRIOR = {"invoices": [{"supplierOriginal": "Synthetic Supplier", "relationMapping": {"status": "unresolved"}}]}


class FakeClient:
    def __init__(self, rows):
        self.rows = rows
        self.calls = 0
        self.paths = []
    def get(self, path):
        self.calls += 1
        self.paths.append(path)
        if path.startswith("/v1/mutation?"):
            return {"items": [{"id": 7, "invoiceNumber": "CONTROL", "type": 1}], "count": 1}
        return {"items": self.rows, "count": len(self.rows)}
    def detail(self, kind, identifier):
        self.calls += 1
        return {"id": identifier, "code": "SYNTH01", "name": "Synthetic Supplier", "inactive": False, "termOfPayment": 0}


class Checks(unittest.TestCase):
    def test_only_planned_relation_queries_and_no_mutation_rescan(self):
        client = p.Client(hints(), factory=lambda *a, **kw: self.fail("Network constructed"))
        self.assertTrue(all(path.startswith("/v1/relation?") or path in client.control_paths for path in client.paths))
        for method, path, body in [("GET", "/v1/mutation?invoiceNumber=SYNTHETIC", None),
                                   ("GET", "/v1/ledger?limit=200&offset=0", None),
                                   ("PATCH", "/v1/relation/1", {}), ("POST", "/v1/relation", {})]:
            with self.assertRaises(p.base.app.app.Stop):
                client.request(method, path, body)

    def test_complete_empty_queries_mean_curated_absence_only(self):
        result = p.collect(FakeClient([]), hints(), PRIOR)
        group = result["groups"][0]
        self.assertEqual(group["status"], "no_matches_for_curated_aliases")
        self.assertTrue(group["searchCompleteWithinBound"])
        self.assertFalse(group["automaticMappingPerformed"])

    def test_candidate_and_verified_identity_do_not_automatically_write_mapping(self):
        expected = {"code": "SYNTH01", "id": 1, "evidence": "synthetic historical proof"}
        client = FakeClient([{"id": 1, "code": "SYNTH01"}])
        group = p.collect(client, hints(expected), PRIOR)["groups"][0]
        self.assertTrue(group["expectedCurrentEntryStillPresent"])
        self.assertEqual(group["status"], "existing_candidates_require_alias_review")
        self.assertFalse(group["automaticMappingPerformed"])
        self.assertTrue(all(path.startswith(("/v1/relation?", "/v1/mutation?")) for path in client.paths))

    def test_full_pages_never_claim_complete_absence(self):
        class Full(FakeClient):
            def get(self, path):
                if path.startswith("/v1/mutation?"):
                    return super().get(path)
                self.calls += 1
                offset = 10 if "offset=10" in path else 0
                return {"items": [{"id": offset + n + 1, "code": "SYNTH01"} for n in range(10)], "count": 10}
        group = p.collect(Full([]), hints(), PRIOR)["groups"][0]
        self.assertEqual(group["status"], "bounded_search_or_details_incomplete")
        self.assertFalse(group["searchCompleteWithinBound"])

    def test_changed_supplier_scope_fails_before_query(self):
        client = FakeClient([])
        with self.assertRaisesRegex(p.base.app.app.Stop, "SUPPLIER_SCOPE_CHANGED"):
            p.collect(client, hints(), {"invoices": []})
        self.assertEqual(client.calls, 0)

    def test_missing_positive_control_invalidates_prior_empty_evidence(self):
        class Missing(FakeClient):
            def get(self, path):
                self.calls += 1
                return {"items": [], "count": 0}
        client = Missing([])
        with self.assertRaisesRegex(p.base.app.app.Stop, "POSITIVE_CONTROL_FAILED"):
            p.collect(client, hints(), PRIOR)
        self.assertEqual(client.calls, 1)

    def test_curated_terms_cannot_inject_wildcards_or_control(self):
        for term in ("%", "Synthetic%", "Synthetic\nSupplier"):
            with self.assertRaises(p.base.app.app.Stop):
                p.planned_queries({"nameTerms": [term], "codeTerms": []})


if __name__ == "__main__":
    unittest.main()
