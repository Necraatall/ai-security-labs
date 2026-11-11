# User-reported local evidence (2026-11-11)

**Evidence class:** User-provided terminal transcript; not executed by GitHub Actions and not independently reproduced on the assistant's host.

## Execution environment

- Local model name from `ollama list`: `gemma3:4b-it-q8_0`
- Ollama model ID shown: `2376388dec16` (short identifier, **not** a verified immutable full digest)
- Interface: loopback Ollama endpoint `http://127.0.0.1:11434`
- v0.3 runner: `python3 -m security_lab.compare_cli --model gemma3:4b-it-q8_0 --repeats 3 --json-output artifacts/comparison.json --html-output artifacts/comparison.html`
- JSON and HTML reports were generated **locally** under ignored `artifacts/`. Their bytes were not supplied here.

## User-reported results

- `unittest discover`: **36 tests**, `OK`, approx. `0.010s`.
- Live requests: **12** (3 attack categories + 1 benign control, repeated 3 times).
- `baseline_attack_leaks`: **6** observed marker leaks from unfiltered responses.
- `output_guard_blocks`: **6** filtered outputs.
- Transport/model errors: **0**.
- Gate: `NO_BLOCKING_EVIDENCE`, process exit **0**.

## Strict interpretation

The result is a demonstration of **detecting and suppressing recognizable leaked synthetic markers in the SAME model response**. The reported 6/6 filtered blocks are not a general defensive success rate, nor evidence of safety against novel encodings, hidden tool actions or multi-turn attacks. Since no full JSON or HTML report/model response was attached, per-case classifications and actual response payloads are not asserted here. A clean run on another revision or machine is unverified.

## Reproduction

```bash
python3 -m unittest discover -s tests -v
python3 -m security_lab.compare_cli \
  --model gemma3:4b-it-q8_0 \
  --repeats 3 \
  --json-output artifacts/comparison.json \
  --html-output artifacts/comparison.html
```

The report contains only digests and derived results; it intentionally omits raw prompts/responses and synthetic markers. For a complete release evidence record, capture local Ollama version, complete model manifest/digest, OS/CPU/RAM, exact Git SHA, report file hashes, runtime configuration and test logs. These details remain **OPEN**.
