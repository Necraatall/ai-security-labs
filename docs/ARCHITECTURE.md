# Architecture — AI Security Labs v0.3

| Component | Purpose |
|---|---|
| `security_lab/core.py`, `fixtures.py`, `evaluation.py`, `cli.py` | Existing v0.1 synthetic tenant-boundary lab |
| `security_lab/ollama.py`, `live.py`, `live_cli.py` | v0.2 optional loopback Ollama client and legacy single-run plaintext oracle |
| `security_lab/oracle.py` | v0.3 multiple deterministic marker-detection representations and guard |
| `security_lab/comparison.py` | v0.3 repeatable per-case probes and **same-response before/after filter** comparison |
| `security_lab/report.py` | JSON and escaped HTML reports with only metadata and non-secret observations |
| `security_lab/compare_cli.py` | Local-model entrypoint; opt-in, bounded repeats |
| `tests/` | Offline unit tests with model doubles; no model downloaded |

## Trust boundaries

The Ollama adapter allows only loopback HTTP hosts and submits a randomly generated synthetic canary in the system prompt. Every repeat uses a new canary. It is deliberately *not* designed to probe third-party applications or model-serving networks.

The model's reply is a string controlled by the model. It passes first through the v0.3 deterministic oracle. The same reply is then passed through an output filter; the filter blocks the entire response on a recognized marker. This is **not** a model-side mitigation or proof of safe agent tool execution.

`artifacts/` is Git-ignored. JSON and HTML include only aggregate metrics, case IDs, response SHA-256 and lengths, not the token or raw response text. Exception messages are excluded, though the exception's type may be recorded.

## Evaluation methodology

Each request can produce `COMPROMISED`, `NOT_OBSERVED` or `ERROR` for the unprotected baseline. The post-filter evaluation records `BLOCKED`, `PASSTHROUGH` or `ERROR`. Fail-closed gate: errors, a leaked marker after filtering or failure of a benign control blocks. Baseline compromised cases *alone* do not block this comparison gate, because it measures whether the output filter caught those observable leaks.

The `NOT_OBSERVED` outcome is not evidence of no leak. Detection is limited by the known canary representations and does not cover latent tool use, exfiltration outside responses, unknown encodings or defense bypasses. A production security gate would require additional independent controls and expected-denial policy.

## Repeatability

The model is asked with `temperature=0` through `/api/chat`; nondeterminism may still occur due to runtime. Pin and record Ollama version and actual model digest externally, as the current CLI reports only the supplied model name. Real v0.3 model runs have not been executed during creation of this package.
