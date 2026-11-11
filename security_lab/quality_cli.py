"""Run transparent hand-labelled offline detector accuracy fixtures."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from security_lab.quality import evaluate_oracle

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="artifacts/oracle-quality.json")
    args = parser.parse_args(argv)
    result = evaluate_oracle()
    dest = Path(args.output)
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except OSError:
        parser.exit(2, "Unable to write evidence\n")
    print("ORACLE FIXTURES:", result["confusion_matrix"], "JSON:", dest)
    # Known blindspots are findings; no misleading green verdict.
    return 1 if result["confusion_matrix"]["fn"] or result["confusion_matrix"]["fp"] else 0

if __name__ == "__main__":
    raise SystemExit(main())
