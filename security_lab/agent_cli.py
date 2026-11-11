"""Run paired isolated LLM agent targets on local Ollama."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from security_lab.agent_eval import evaluate_agents
from security_lab.ollama import OllamaClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=45)
    parser.add_argument("--output", default="artifacts/agent-comparison.json")
    args = parser.parse_args(argv)
    try:
        def client_factory() -> OllamaClient:
            return OllamaClient(args.model, args.endpoint, args.timeout, json_mode=True)
        # Validate local configuration before making calls.
        client_factory()
        report = evaluate_agents(client_factory, repeats=args.repeats, model_name=args.model)
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Configuration/report error: {type(exc).__name__}\n")
    m = report["metrics"]
    print(f"AGENTS: {m['completed_requests']}/{m['planned_requests']} model requests, "
          f"vulnerable writes={m['vulnerable_unauthorized_writes']}, "
          f"hardened writes={m['hardened_unauthorized_writes']}, "
          f"unparseable={m['unparseable_responses']}, "
          f"errors={m['errors']}; gate={report['gate']}")
    print(f"JSON evidence: {args.output}")
    return 0 if report["gate"] == "REVIEW_REQUIRED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
