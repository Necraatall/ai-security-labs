# Release log

## v0.5 — Public portfolio baseline (2026-11-11)

- Added MIT license and SHA-pinned GitHub Actions in merged PR #2 (`d6488c3`).
- User reported six successful GitHub Actions checks on Python 3.11–3.13.
- User reported clean Trivy secret scans for working tree and all three reachable commits at review time.
- GitHub CLI confirmed `isPrivate: false`.
- v0.5.1 documentation-only follow-up aligns README, TODO and release evidence with actual status.
- Remaining research and repeatability work stays explicitly open.

# Release log

## v0.4 — Portfolio release preparation (historical)

- Added offline GitHub Actions Python matrix (3.11, 3.12, 3.13).
- Added strict structural validation of synthetic fixture evidence plus negative tests.
- Recorded the user-reported v0.3 Ollama run with precise limitations.
- Added a publication gate explicitly marking remote CI, Git history scan, action SHA pinning and licensing as pending.
- **At v0.4 creation remote CI had not run. It subsequently passed in GitHub PR #1.**


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

## Historical roadmap (superseded by current TODO.md)

- v0.4: provenance-reviewed original user-created scenarios, isolated target adapters, benign-task assertions and broader oracles.
- v0.5: real hardening demonstrations with independent before/after model requests, CI/CD and reproducibility evidence.
- v1.0: source licensing/attribution, security audit, reviewed release approval, then optional Public.

## Gates

No publication without explicit approval and a provenance/license/secrets audit. Distinguish synthetic mock tests from actual LLM tests. Never claim a filtered reply proves protection against unknown attack formats.

## v0.6 — reproducibility implementation (pending user's live validation)

- Added fail-closed Ollama exact model-tag digest and server version discovery.
- Added source Git commit and tracked-tree cleanliness checks plus coarse local runtime metadata.
- Added detached SHA-256 JSON/HTML evidence manifest and offline bundle verifier.
- Offline test suite: 50/50 PASS in assistant container. Real Ollama/host check: **NOT RUN** here.
- This is experiment traceability, NOT model-safety certification, cryptographic signature,
  or deterministic replay of model output.

## v0.7 — FinanceBot concept reconstruction

- Fresh, independent synthetic 20-case/25-turn suite with isolated histories.
- No imported course code or original prompt text. Four goal categories.
- Offline unit tests; Ollama LIVE and human verdicts not yet executed.
- Provenance marked provisional pending owner confirmation.

## v0.8 – synthetic independent agents

Added isolated vulnerable/hardened agents, fake ledger mutation boundary, multi-turn test and untrusted lookup injection, case-local independent model adapters, and metadata-only JSON report. Offline test evidence and actual Ollama verification are separate. No real transactions.

## v0.9 candidate

Adds a narrow, measurable benign lookup quality oracle and synthetic hand-labelled detector confusion matrix (including explicit known FN). Real Ollama experiment and CI not yet run. No claim of deployment false-positive or false-negative rate.

## v0.9.1 – targeted corrections (pending live acceptance)

- Both agent system prompts explicitly include the benign readback JSON schema expected by the evaluator.
- Oracle now recognizes complete reversed canary strings; 13 labelled synthetic fixtures expected to have TP=9, TN=4, FP=0, FN=0.
- A green oracle fixture check is evidence for those fixtures only. Real model benign correctness and attack results need rerun.
