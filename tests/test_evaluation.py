import json
import tempfile
import unittest
from pathlib import Path

from security_lab.cli import main
from security_lab.core import Decision, Request
from security_lab.evaluation import Case, evaluate
from security_lab.fixtures import cases, target


class TestEvaluation(unittest.TestCase):
    def test_expected_fixtures_pass(self):
        report = evaluate(target(), cases())
        self.assertEqual(report["metrics"]["failed"], 0)
        self.assertEqual(report["metrics"]["total"], 7)
        self.assertEqual(report["target_kind"], "synthetic")

    def test_mismatch_is_reported(self):
        bad = [Case("FAIL", "test", Request("tenant-a", "Q", "policy-b"),
                    Decision.ALLOW, "authorized_document")]
        result = evaluate(target(), bad)
        self.assertEqual(result["metrics"]["failed"], 1)
        self.assertEqual(result["metrics"]["fixture_mismatch_rate"], 1.0)

    def test_duplicate_case_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(target(), [cases()[0], cases()[0]])

    def test_empty_suite_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(target(), [])

    def test_cli_writes_report(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "result.json"
            self.assertEqual(main(["run", "--output", str(p), "--fail-on-compromise"]), 0)
            result = json.loads(p.read_text())
            self.assertEqual(result["metrics"]["total"], 7)


if __name__ == "__main__":
    unittest.main()
