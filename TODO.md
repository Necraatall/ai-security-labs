# AI Security Labs — v1.0 release checklist

**Current state (2026-11-11):** v1.0.0 finalization in progress. PR #9 has been **MERGED** (`e80f5cbbc884ee8aa644344ec6f3b52126a92125`). The final `v1.0.0` GitHub Release is **NOT YET PUBLISHED**. Only evidenced work is checked.

## Completed and verified — milestones v0.1 through v1.0-rc1

- [x] v0.1: independent synthetic lab and basic tenant-boundary behavior; original course repository remains private.
- [x] v0.2: controlled live Ollama leakage experiment, with narrow, explicitly documented evidence.
- [x] v0.3: extended canary detectors and same-response filter; no general safety assertion.
- [x] v0.4: GitHub Actions matrix for Python 3.11, 3.12 and 3.13, strict synthetic evidence validation.
- [x] v0.5/v0.5.1: public independent MIT repository, SHA-pinned Actions, provenance/publication documentation.
- [x] v0.6: exact-model/Git experiment manifest implementation and detached JSON/HTML SHA-256 verifier (not a fully reproducible runtime).
- [x] v0.7: independently reconstructed FinanceBot concepts (20 synthetic cases, 25 turns), no imported teaching code.
- [x] v0.8/v0.8.1: separate vulnerable and hardened synthetic targets, multi-turn scenarios and fail-closed malformed model decisions.
- [x] v0.8 observed live experiment: 12/12 model requests; vulnerable unauthorized writes 3, hardened writes 0, subject to narrow scope.
- [x] v0.9: benign readback and narrow labelled oracle evaluation.
- [x] v0.9.1: complete-token reversal fix; 13 synthetic oracle fixtures TP=9, TN=4, FP=0, FN=0.
- [x] v0.9.1 observed live Gemma test: 42/42 model requests, benign correct 12/12, vulnerable unauthorized writes 7, hardened writes 0, vulnerable marker leaks 1, hardened 0; `REVIEW_REQUIRED`, not a safety certificate.
- [x] v0.10: Ruff, Bandit, pip-audit project-metadata scan, wheel/sdist validation and isolated import smoke test; PR #8 merged with green CI.
- [x] v1.0-rc1: threat model, source ZIP/manifest builder, deterministic/tamper tests and written limitations.
- [x] v1.0-rc1: maintainer-reported 96/96 local tests and GitHub CI 4/4 PASS on PR #9 head.
- [x] v1.0-rc1: Trivy 0.76.2 secret scan (no findings reported) on `f0e6a60`.
- [x] v1.0-rc1: Trivy vulnerability and misconfiguration scan correctly classified **NOT SCANNED** because there were no eligible inputs; not mislabeled PASS.
- [x] v1.0-rc1: internal AI-assisted security review and evidence limitations documented; external/independent acceptance not claimed.
- [x] v1.0-rc1: PR #9 merged; commit `e80f5cbbc884ee8aa644344ec6f3b52126a92125`.
- [x] Reconciled historical milestones and documented local Ubuntu 22.04 vs CI `ubuntu-latest` and Node.js runtime deprecation.

## Remaining gates — final GitHub Release v1.0.0

- [ ] **Acceptance/provenance:** independent reviewer or release owner verifies actual final-source trust boundaries, accepts/disposes SR-03/SR-04 limitations, and confirms authorized publication of every included source file. Record who accepted, the exact commit and any known residual risks; never call internal AI review independent.
- [ ] **Final build CI:** merge version `1.0.0` and synchronization changes, confirm tests, Ruff, Bandit, pip-audit, wheel/sdist and archive verifier PASS on the final commit. When code changes, rerun relevant Ollama probes or clearly mark the missing rerun.
- [ ] **Published assets:** create and verify the deterministic source ZIP and manifest from the *final tagged commit*, record both SHA-256 values, publish GitHub Release `v1.0.0`, then verify the uploaded assets match the manifest and commit.

## Portfolio follow-up (separate from release acceptance)

- [ ] Update `Necraatall/Necraatall` profile README with the public release link and precise status.

## Future research — v1.1+ (not part of v1.0 acceptance)

- Live independently labelled false-positive/false-negative evaluation beyond 13 synthetic fixtures.
- Semantic/tool-mediated leakage and additional encodings; realistic authorized write workflows.
- Optional Trivy CI integration, signed release attestations and external provenance verification.
- Review and upgrade SHA-pinned Actions to supported Node.js runtime; test runner-image pinning.
- If original course files are ever reused, perform a separate file-by-file authorship/license review first; do not import nonpublic source.

## Evidence interpretation

A green CI, clean secrets scan, synthetic detector results or `NO_BLOCKING_EVIDENCE` applies only to the declared scope. Unsigned manifests verify integrity relative to supplied hashes, not authenticity. Historical LIVE results are not a test of the final release commit.
