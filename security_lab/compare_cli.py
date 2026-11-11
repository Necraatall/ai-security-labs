"""Explicit opt-in repeated local LLM evaluation with limited secret-free reports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from security_lab.comparison import evaluate_comparison
from security_lab.ollama import OllamaClient
from security_lab.report import write_reports
from security_lab.reproducibility import collect_metadata, write_manifest, verify_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run repeated local AI security comparison")
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--json-output", type=Path, default=Path("artifacts/comparison.json"))
    parser.add_argument("--html-output", type=Path, default=Path("artifacts/comparison.html"))
    parser.add_argument("--manifest-output", type=Path, default=Path("artifacts/repro-manifest.json"))
    args = parser.parse_args(argv)
    try:
        model = OllamaClient(model=args.model, endpoint=args.endpoint, timeout=args.timeout)
        metadata = collect_metadata(model, Path.cwd(), repeats=args.repeats)
        paths = (args.json_output, args.html_output, args.manifest_output)
        if len({p.resolve() for p in paths}) != 3:
            raise ValueError("All evidence paths must be distinct")
        result = evaluate_comparison(model, repeats=args.repeats, model_name=args.model)
        write_reports(result, args.json_output, args.html_output)
        write_manifest(args.manifest_output, args.json_output, args.html_output, metadata, result)
        verify_manifest(args.manifest_output, args.json_output, args.html_output)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"Configuration/output error: {type(exc).__name__}", file=sys.stderr)
        return 2

    metrics = result["metrics"]
    print(
        f"LIVE: {metrics['requests']} requests, {metrics['baseline_attack_leaks']} "
        f"observed baseline attack leaks, {metrics['output_guard_blocks']} "
        f"output blocks, {metrics['errors']} errors. Gate: {result['gate']}"
    )
    print(f"Reports: {args.json_output} | {args.html_output} | {args.manifest_output}")
    return 1 if result["gate"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
