"""Offline scope, code-selection and identity-evidence checks."""
import unittest
import catalogue_match as p


class Checks(unittest.TestCase):
    def test_only_catalogue_relation_reads_no_account_or_bank_writes(self):
        client = p.Client(lambda *a, **kw: self.fail("Network constructed"))
        self.assertEqual(len(client.paths), 5)
        for method, path, body in [("GET", "/v1/mutation/1", None), ("GET", "/v1/ledger?limit=200&offset=0", None),
                                   ("GET", "/v1/relation/999", None), ("POST", "/v1/relation", {}),
                                   ("PATCH", "/v1/relation/1", {}), ("DELETE", "/v1/relation/1", None)]:
            with self.assertRaises(p.base.app.app.Stop):
                client.request(method, path, body)

    def test_media_fragments_and_private_type_retained_max100_directed_details(self):
        catalogue = [{"id": n + 1, "type": "P" if n % 2 else "B", "code": "MEDIA" + str(n)} for n in range(200)]
        ranked, selected = p.shortlist(catalogue, [{"supplier": "Synthetic", "codeFragments": ["MEDIA", "MARKT", "MM"]}], {"groups": []})
        self.assertEqual(len(ranked["Synthetic"]), 200)
        self.assertEqual(len(selected), 100)
        self.assertIn(2, selected)

    def test_identity_fields_produce_evidence_not_automatic_mapping(self):
        profile = {"vatNumber": "NL123456789B01", "companyRegistrationNumber": "00123456", "address": "Example 1", "postalCode": "1000 AA", "city": "Synthetic", "displayName": "Source supplier"}
        candidate = {"vatNumber": "NL 123456789 B01", "companyRegistrationNumber": "00123456", "address": "Different 2", "postalCode": "2000 BB", "name": "Registered trade name", "inactive": False}
        evidence = p.identity_evidence(profile, candidate)
        self.assertEqual(evidence["strength"], "strong_existing_identity_candidate")
        self.assertEqual(evidence["comparisons"]["address"], "different")
        self.assertFalse(evidence["automaticMatch"])

    def test_empty_name_filter_cannot_overrule_known_existing_id(self):
        class Client:
            paths = set()
            def get(self, path):
                return {"items": [], "count": 0}
        result = p.filter_control(Client(), {"id": 7, "name": "Synthetic", "code": "SYNTH01"})
        self.assertTrue(result["noAbsenceInferenceFromFailure"])
        self.assertFalse(any(check["knownExistingIdReturned"] for check in result["checks"]))

    def test_incomplete_pagination_is_not_complete_coverage(self):
        class Client:
            def get(self, path):
                return {"items": [{"id": n + 1} for n in range(1000)]}
        rows, complete, reason = p.base.complete_pages(Client().get, str, 1000, 1)
        self.assertFalse(complete)
        self.assertEqual(reason, "page_budget_exhausted")


if __name__ == "__main__":
    unittest.main()
