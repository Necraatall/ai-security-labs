"""Verify detached report hashes and required provenance fields (no Ollama needed)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from security_lab.reproducibility import ProvenanceError, verify_manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('json_report', type=Path)
    parser.add_argument('html_report', type=Path)
    args = parser.parse_args(argv)
    try:
        verify_manifest(args.manifest, args.json_report, args.html_report)
    except ProvenanceError:
        print('FAIL: reproducibility evidence is invalid', file=sys.stderr)
        return 1
    print('PASS: report hashes and provenance structure verified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
