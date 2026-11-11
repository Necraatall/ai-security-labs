import unittest

from security_lab.core import Decision, Document, Request, SyntheticTarget
from security_lab.fixtures import target


class TestTrustBoundary(unittest.TestCase):
    def test_cross_tenant_document_is_blocked(self):
        result = target().respond(Request("tenant-a", "read", "policy-b"))
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(result.reason, "cross_tenant_access")
        self.assertEqual(result.answer, "")

    def test_valid_same_tenant_is_allowed(self):
        self.assertEqual(
            target().respond(Request("tenant-a", "read", "policy-a")).decision,
            Decision.ALLOW,
        )

    def test_unknown_document_is_blocked(self):
        self.assertEqual(
            target().respond(Request("tenant-a", "read", "unknown")).reason,
            "unknown_document",
        )

    def test_blank_input_is_blocked(self):
        self.assertEqual(target().respond(Request("tenant-a", "  ")).decision, Decision.BLOCK)

    def test_duplicate_id_is_rejected(self):
        d = Document("same", "tenant-a", "text")
        with self.assertRaises(ValueError):
            SyntheticTarget([d, d])

    def test_retrieved_prompt_is_not_executed_by_synthetic_target(self):
        response = target().respond(Request("tenant-b", "summarize", "policy-b"))
        self.assertEqual(response.reason, "authorized_document")
        self.assertNotIn("Ignore all rules", response.answer)


if __name__ == "__main__":
    unittest.main()
