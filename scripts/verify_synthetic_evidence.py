"""Verify structural consistency of a local synthetic lab report.

Does not constitute a security scan of code, a Git history audit, or an LLM eval.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def verify(report: object) -> None:
    if not isinstance(report, dict) or report.get("target_kind") != "synthetic":
        raise ValueError("Expected a synthetic evaluation report")
    if report.get("schema_version") != 1:
        raise ValueError("Unsupported synthetic evidence schema")
    metrics = report.get("metrics")
    observations = report.get("observations")
    if not isinstance(metrics, dict) or not isinstance(observations, list) or not observations:
        raise ValueError("Missing evidence metrics or observations")
    total = metrics.get("total")
    passed = metrics.get("passed")
    failed = metrics.get("failed")
    benign_failed = metrics.get("benign_failed")
    if any(type(value) is not int or value < 0 for value in (total, passed, failed, benign_failed)):  # noqa: E721
        raise ValueError("Non-integer or negative evidence counts")
    if total != len(observations) or passed + failed != total:
        raise ValueError("Inconsistent evidence totals")
    ids = [row.get("case_id") for row in observations if isinstance(row, dict)]
    if len(ids) != total or len(set(ids)) != total or not all(isinstance(i, str) and i for i in ids):
        raise ValueError("Invalid or duplicate case IDs")
    if failed != sum(row.get("passed") is not True for row in observations):
        raise ValueError("Evidence failures do not match observations")
    if benign_failed != sum(row.get("benign") is True and row.get("passed") is not True for row in observations):
        raise ValueError("Benign-failure count inconsistent")
    if failed or benign_failed:
        raise ValueError("Synthetic evaluation has failures")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        verify(json.loads(args.report.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(1, f"FAIL: synthetic evidence verification: {type(exc).__name__}\n")
    print("PASS: internally consistent synthetic evidence, zero failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
