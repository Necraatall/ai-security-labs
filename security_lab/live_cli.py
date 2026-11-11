"""CLI for local-model red-team runs (requires a local running Ollama)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from security_lab.live import evaluate_live
from security_lab.ollama import OllamaClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local Ollama attack cases")
    parser.add_argument("--model", required=True, help="Already installed Ollama model name")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--output", type=Path, default=Path("artifacts/live-results.json"))
    args = parser.parse_args(argv)
    try:
        client = OllamaClient(args.model, args.endpoint, args.timeout)
        result = evaluate_live(client)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Configuration/output error: {type(exc).__name__}\n")
    metrics = result["metrics"]
    print(
        f"LIVE: {metrics['attacks']} attacks, "
        f"{metrics['attack_leaks']} observed plaintext leaks, "
        f"{metrics['errors']} errors. Gate: {result['gate']}"
    )
    print(f"JSON evidence: {args.output}")
    return 1 if result["gate"] == "BLOCK" else 0


if __name__ == "__main__":
    raise SystemExit(main())
