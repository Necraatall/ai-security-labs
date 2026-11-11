"""Deterministic red-team case evaluator with explicit policy semantics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Iterable

from security_lab.core import Decision, Request, SyntheticTarget


@dataclass(frozen=True)
class Case:
    case_id: str
    category: str
    request: Request
    expected_decision: Decision
    expected_reason: str
    benign: bool = False


@dataclass(frozen=True)
class Observation:
    case_id: str
    category: str
    expected_decision: str
    actual_decision: str
    expected_reason: str
    actual_reason: str
    passed: bool
    benign: bool


def validate_cases(cases: list[Case]) -> None:
    ids = [case.case_id for case in cases]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate case_id")
    if not cases:
        raise ValueError("At least one case is required")


def evaluate(target: SyntheticTarget, cases: Iterable[Case]) -> dict:
    selected = list(cases)
    validate_cases(selected)
    observations = []
    for case in selected:
        response = target.respond(case.request)
        passed = (
            response.decision == case.expected_decision
            and response.reason == case.expected_reason
        )
        observations.append(
            Observation(
                case_id=case.case_id,
                category=case.category,
                expected_decision=case.expected_decision.value,
                actual_decision=response.decision.value,
                expected_reason=case.expected_reason,
                actual_reason=response.reason,
                passed=passed,
                benign=case.benign,
            )
        )

    count = len(observations)
    failures = sum(not item.passed for item in observations)
    failures_benign = sum(item.benign and not item.passed for item in observations)
    definition = "Fixture mismatches / total evaluated synthetic cases"
    return {
        "schema_version": 1,
        "target_kind": "synthetic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "fixture_digest": sha256(
            "\n".join(
                f"{x.case_id}|{x.expected_decision}|{x.expected_reason}" for x in selected
            ).encode()
        ).hexdigest(),
        "metrics": {
            "total": count,
            "passed": count - failures,
            "failed": failures,
            "benign_failed": failures_benign,
            "fixture_mismatch_rate": failures / count,
            "definition": definition,
        },
        "observations": [asdict(item) for item in observations],
    }
