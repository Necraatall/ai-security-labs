"""Negative tests for the strict fixture evidence gate."""

from __future__ import annotations

import copy
import unittest

from scripts.verify_synthetic_evidence import verify
from security_lab.evaluation import evaluate
from security_lab.fixtures import cases, target


class TestEvidenceVerification(unittest.TestCase):
    def setUp(self):
        self.report = evaluate(target(), cases())

    def test_valid_report(self):
        verify(self.report)

    def test_missing_observations(self):
        report = copy.deepcopy(self.report)
        report["observations"] = []
        with self.assertRaises(ValueError):
            verify(report)

    def test_wrong_total(self):
        report = copy.deepcopy(self.report)
        report["metrics"]["total"] += 1
        with self.assertRaises(ValueError):
            verify(report)

    def test_false_is_not_int_count(self):
        report = copy.deepcopy(self.report)
        report["metrics"]["failed"] = False
        with self.assertRaises(ValueError):
            verify(report)

    def test_duplicate_case_id(self):
        report = copy.deepcopy(self.report)
        report["observations"][1]["case_id"] = report["observations"][0]["case_id"]
        with self.assertRaises(ValueError):
            verify(report)

    def test_false_pass_is_blocking(self):
        report = copy.deepcopy(self.report)
        report["observations"][0]["passed"] = False
        with self.assertRaises(ValueError):
            verify(report)

    def test_missing_schema(self):
        report = copy.deepcopy(self.report)
        report.pop("schema_version")
        with self.assertRaises(ValueError):
            verify(report)


if __name__ == "__main__":
    unittest.main()
