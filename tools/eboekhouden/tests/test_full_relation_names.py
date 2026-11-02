import unittest
import full_relation_names as p


class Checks(unittest.TestCase):
    def test_scope_only_observed_relation_ids(self):
        client = p.Client(lambda *a, **kw: self.fail("Network constructed"))
        client.admitted_ids = {1}
        for method, path, body in [("POST", "/v1/relation", {}), ("GET", "/v1/mutation/1", None),
                                   ("PUT", "/v1/relation/1", {}), ("GET", "/v1/relation/1", None)]:
            with self.assertRaises(p.base.app.app.Stop):
                client.request(method, path, body)
        with self.assertRaises(p.base.app.app.Stop):
            client.detail("relation", 2)
        with self.assertRaises(p.base.app.app.Stop):
            client.detail("mutation", 1)
        client.calls = 509
        with self.assertRaisesRegex(p.base.app.app.Stop, "CALL_BUDGET"):
            client.request("GET", next(iter(client.paths)))

    def test_all_names_and_both_types_even_unrelated_codes(self):
        class Fake:
            def get(self, path):
                return {"items": [{"id": 1, "code": "R0001", "type": "P"}, {"id": 2, "code": "R0002", "type": "B"}], "count": 2}
            def detail(self, kind, identifier):
                return {"id": identifier, "code": "R000" + str(identifier), "type": "P" if identifier == 1 else "B",
                        "name": "Synthetic Media Markt" if identifier == 1 else "Other", "inactive": True}
        result = p.collect(Fake(), {"proposals": [{"sourceSupplierLabel": "Example", "displayName": "Synthetic Media Markt"}]},
                           {"groups": [{"supplier": "Example", "codeFragments": ["MEDIA", "MARKT"]}]})
        self.assertEqual(result["detailCount"], 2)
        self.assertTrue(result["allReturnedRelationNamesCovered"])
        candidate = result["supplierGroups"][0]["candidates"][0]
        self.assertEqual(candidate["candidate"]["id"], 1)
        self.assertTrue(candidate["candidate"]["inactive"])
        self.assertFalse(candidate["identityEvidence"]["automaticMatch"])

    def test_over500_stops_before_details(self):
        class Fake:
            def get(self, path):
                return {"items": [{"id": n + 1} for n in range(501)], "count": 501}
            def detail(self, *args):
                raise AssertionError("Must stop before details")
        with self.assertRaisesRegex(p.base.app.app.Stop, "EXCEEDS_BOUND"):
            p.collect(Fake(), {}, {})


if __name__ == "__main__":
    unittest.main()
