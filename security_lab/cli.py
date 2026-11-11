"""CLI for the synthetic AI security lab."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from security_lab.evaluation import evaluate
from security_lab.fixtures import cases, target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run a synthetic security evaluation")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--output", type=Path, default=Path("artifacts/results.json"))
    run.add_argument("--fail-on-compromise", action="store_true")
    args = parser.parse_args(argv)

    if args.command != "run":
        parser.error("Unknown command")

    result = evaluate(target(), cases())
    destination: Path = args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    metrics = result["metrics"]
    print(f"SYNTHETIC: {metrics['passed']}/{metrics['total']} fixture checks passed")
    print(f"JSON evidence: {destination}")
    return 1 if args.fail_on_compromise and metrics["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
