"""Explicit local-only FinanceBot red-team runner (20 cases, 25 turns)."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from security_lab.finance_eval import evaluate_finance
from security_lab.ollama import OllamaClient

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True)
    parser.add_argument('--endpoint', default='http://127.0.0.1:11434')
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--timeout', type=float, default=45)
    parser.add_argument('--output', default='artifacts/financebot-results.json')
    args = parser.parse_args(argv)
    try:
        client = OllamaClient(args.model, args.endpoint, args.timeout)
        report = evaluate_finance(client, repeats=args.repeats, model_name=args.model)
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Configuration/report error: {type(exc).__name__}\n')
    metrics = report['metrics']
    print(f"FinanceBot: {metrics['completed_requests']}/{metrics['planned_requests']} requests, "
          f"{metrics['leak_case_runs']} leaked case runs, "
          f"{metrics['manual_review_case_runs']} manual reviews, "
          f"{metrics['errors']} errors; gate {report['gate']}")
    print(f'JSON evidence: {args.output}')
    return 1 if report['gate'] == 'BLOCK' else 0

if __name__ == '__main__':
    raise SystemExit(main())
