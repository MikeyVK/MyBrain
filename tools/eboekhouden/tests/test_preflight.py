"""Synthetic-only preflight evidence. Never read credentials or make API calls."""
import unittest
from unittest.mock import patch
import preflight as p


INVOICE = {"factuur_id": "SYNTHETIC", "factuurnummer": "SYNTHETIC-1", "factuurdatum": "2000-01-01",
           "totaal_incl_btw": "12.10", "bedragen_incl_excl": "INCL", "leverancier_naam": "Synthetic Supplier"}


class Checks(unittest.TestCase):
    def test_readonly_client_rejects_writes_and_unplanned_reads_before_network(self):
        policy = {"acceptedAmazonCentralCode": "SYNTHCENTRAL01"}
        client = p.Client([INVOICE], policy, lambda *a, **kw: self.fail("Network constructed"))
        for method, path, body in [("POST", "/v1/mutation", {}), ("PATCH", "/v1/relation/1", {}),
                                   ("DELETE", "/v1/mutation/1", None), ("GET", "/v1/mutation", None),
                                   ("GET", "/v1/mutation/999", None), ("GET", "https://other.invalid", None)]:
            with self.assertRaisesRegex(p.app.app.Stop, "PREFLIGHT_REQUEST_NOT_ALLOWED"):
                client.request(method, path, body)

    def test_complete_pagination_requires_terminal_short_page(self):
        pages = iter([{"items": [{"id": 1}, {"id": 2}]}, {"items": [{"id": 3}]}])
        rows, complete, reason = p.complete_pages(lambda path: next(pages), lambda offset: str(offset), 2, 3)
        self.assertEqual(len(rows), 3)
        self.assertTrue(complete)
        rows, complete, reason = p.complete_pages(lambda path: {"items": [{"id": 1}, {"id": 2}]}, str, 2, 1)
        self.assertFalse(complete)
        self.assertEqual(reason, "page_budget_exhausted")

    def test_overlapping_pages_and_ledger_code_collisions_are_not_complete_mappings(self):
        pages = iter([{"items": [{"id": 1}]}, {"items": [{"id": 1}]}])
        self.assertFalse(p.complete_pages(lambda path: next(pages), str, 1, 2)[1])
        mapping = p.map_ledgers([{"id": 1, "code": "4700", "category": "VW"}, {"id": 2, "code": "4700", "category": "VW"}], True, ["4700"])
        self.assertEqual(mapping["4700"]["status"], "missing_or_duplicate_code")
        self.assertEqual(p.map_ledgers([], False, ["4700"])["4700"]["status"], "catalog_incomplete")

    def test_reported_nonempty_count_cannot_be_accepted_as_empty_complete_page(self):
        rows, complete, reason = p.complete_pages(lambda path: {"items": [], "count": 4}, str, 20, 3)
        self.assertFalse(complete)
        self.assertEqual(reason, "reported_count_disagrees_with_retrieved_items")

    def test_duplicate_needs_number_type_date_gross_and_counterparty(self):
        detail = {"id": 7, "invoiceNumber": "SYNTHETIC-1", "type": 1, "date": "2000-01-01", "relationId": 3,
                  "inExVat": "EX", "rows": [{"amount": 10}], "vat": [{"amount": "2.10"}]}
        self.assertEqual(p.compare_duplicate(INVOICE, detail, {"id": 3})["status"], "confirmed_existing_duplicate")
        self.assertEqual(p.compare_duplicate(INVOICE, detail, None)["status"], "possible_existing_requires_review")
        detail["date"] = "2001-01-01"
        self.assertEqual(p.compare_duplicate(INVOICE, detail, {"id": 3})["status"], "possible_existing_requires_review")

    def test_zero_terms_negative_credit_and_private_vat_are_preserved(self):
        self.assertEqual(p.payment_term("0", {"termOfPayment": 14})["days"], 0)
        self.assertEqual(p.payment_term("", {"termOfPayment": 0})["days"], 0)
        self.assertEqual(p.payment_term("", {})["status"], "missing_no_default_assumed")
        self.assertEqual(p.gross({"inExVat": "IN", "rows": [{"amount": "-121.00"}]}), p.money("-121.00"))
        policy = {"privateCode": "1410", "workClothingCode": "7050", "reverseChargeInvoiceIds": []}
        line = {"grootboekcode_voorgesteld": "1410", "regel_nr": 1, "omschrijving": "Synthetic private", "btw_percentage": 21,
                "bedrag_ex_btw": "5.00", "btw_bedrag": "1.05", "bedrag_incl_btw": "6.05"}
        result = p.line_proposal(line, INVOICE, policy, {"1410": {"status": "mapped"}})
        self.assertEqual(result["vatCode"], "GEEN")
        self.assertEqual(result["deductibleSourceVat"], "0.00")
        self.assertEqual(result["proposedAmountBasis"], "6.05")
        self.assertEqual(result["sourceAmounts"]["vat"], "1.05")

    def test_reverse_charge_is_not_flattened_to_no_vat(self):
        policy = {"privateCode": "1410", "workClothingCode": "7050", "reverseChargeInvoiceIds": ["SYNTHETIC"]}
        line = {"grootboekcode_voorgesteld": "4750", "regel_nr": 1, "omschrijving": "Synthetic EU service", "btw_percentage": 0,
                "bedrag_ex_btw": 10, "btw_bedrag": 0, "bedrag_incl_btw": 10}
        self.assertEqual(p.line_proposal(line, INVOICE, policy, {"4750": {"status": "mapped"}})["vatCode"], "BI_EU_INK")

    def test_incomplete_duplicate_query_cannot_claim_no_duplicate(self):
        class Client:
            def get(self, path):
                return {"items": [{"id": n + 1, "invoiceNumber": "SYNTHETIC-1", "type": 1} for n in range(20)]}
        result = p.inspect_duplicates(Client(), INVOICE, None)
        self.assertEqual(result["status"], "duplicate_check_incomplete")
        self.assertFalse(result["complete"])

    def test_noninvoice_mutation_reference_is_not_false_absence(self):
        class Client:
            def get(self, path):
                self.path = path
                return {"items": [{"id": 7, "invoiceNumber": "SYNTHETIC-1", "type": 6}]}
            def detail(self, kind, identifier):
                return {"id": 7, "invoiceNumber": "SYNTHETIC-1", "type": 6, "date": "2000-01-01", "relationId": 3,
                        "inExVat": "IN", "rows": [{"amount": "12.10"}], "vat": []}
        client = Client()
        result = p.inspect_duplicates(client, INVOICE, {"id": 3})
        self.assertNotIn("type=", client.path)
        self.assertEqual(result["status"], "possible_existing_requires_review")
        self.assertFalse(result["comparisons"][0]["checks"]["type"])

    def test_nonmatching_invoice_filter_response_fails_closed(self):
        class Client:
            def get(self, path):
                return {"items": [{"id": 7, "invoiceNumber": "OTHER", "type": 1}]}
            def detail(self, kind, identifier):
                raise AssertionError("Nonmatching record must not be read")
        result = p.inspect_duplicates(Client(), INVOICE, None)
        self.assertEqual(result["status"], "query_filter_not_honored")
        self.assertFalse(result["complete"])

    def test_payment_reference_without_purchase_amount_mode_remains_possible_existing(self):
        result = p.compare_duplicate(INVOICE, {"id": 9, "type": 4, "invoiceNumber": "SYNTHETIC-1"}, None)
        self.assertEqual(result["status"], "possible_existing_requires_review")
        self.assertFalse(result["checks"]["type"])

    def test_code_and_expected_id_must_both_match(self):
        class Client:
            def get(self, path):
                return {"items": [{"id": 99}]}
            def detail(self, kind, identifier):
                return {"id": 99, "code": "SYNTHCENTRAL01", "inactive": False, "name": "Synthetic"}
        result = p.Relations(Client()).resolve("Amazon Synthetic", {"acceptedAmazonCentralCode": "SYNTHCENTRAL01", "expectedAmazonRelationId": 3})
        self.assertNotIn("relation", result)
        self.assertEqual(result["status"], "expected_code_identity_or_active_conflict")

    def test_redaction_covers_nested_fields_and_json_escaping(self):
        secret = 'FAKE"SECRET'
        result = p.redact({secret: [{"name": "prefix " + secret}]}, [secret])
        self.assertEqual(result, {"[REDACTED]": [{"name": "prefix [REDACTED]"}]})


if __name__ == "__main__":
    unittest.main()
