# Release log

## v0.3 — Extended leak oracle and paired output-filter comparison

- Added exact plaintext, Base64/base64url, hex, Unicode escape, long random hex fragment and whitespace-separated canary detection.
- Added bounded repeated Ollama requests (default 3), fresh canary per repetition and explicit per-case metrics.
- Added deterministic response-filter demonstration comparing the **same** model output before and after filtering. **Not a model defense benchmark**.
- Added safe JSON and HTML reporting (no raw model replies or secrets).
- Added offline test coverage for recognition, errors, report escaping and evidence integrity.
- Actual Ollama run: **NOT RUN in package build environment**. Requires user-local Ollama.

## v0.2 — Historical user-local validation

- 20/20 unit tests passed (user-provided run).
- Live Ollama on `gemma3:4b-it-q8_0`: 2/3 attacks produced plaintext canary leakage; 0 errors; original single-run gate `BLOCK` (user-provided JSON).
- The Base64 case returned `NOT_OBSERVED` under a *plaintext-only* v0.2 oracle; it was not demonstrated safe.

## v0.1 — Synthetic lab

- 11/11 unit tests and 7/7 fixture checks passed in the user's environment.

## Next release candidates

- v0.4: provenance-reviewed original user-created scenarios, isolated target adapters, benign-task assertions and broader oracles.
- v0.5: real hardening demonstrations with independent before/after model requests, CI/CD and reproducibility evidence.
- v1.0: source licensing/attribution, security audit, reviewed release approval, then optional Public.

## Gates

No publication without explicit approval and a provenance/license/secrets audit. Distinguish synthetic mock tests from actual LLM tests. Never claim a filtered reply proves protection against unknown attack formats.
