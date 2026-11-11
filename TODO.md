# AI Security Labs — verified status and release backlog

**Current:** public v1.0.0rc1 on open PR #9 (`f0e6a60`); final `v1.0.0` is **NOT RELEASED**. Checkboxes distinguish evidence from aspirations. Updated 2026-11-11.

## Completed and evidenced

- [x] Separate public MIT-licensed repository; training/course repository remains private, without reused Git history.
- [x] Offline synthetic tenant-boundary suite, FinanceBot scenario reconstruction (20 cases/25 turns), and independent synthetic vulnerable/hardened agent targets.
- [x] Local Ollama live evidence reported: v0.8 12/12 requests; v0.9.1 Gemma 42/42 requests, benign correct 12/12, vulnerable unauthorized writes 7, hardened writes 0, vulnerable marker leaks 1, hardened marker leaks 0. These are bounded observed results, not general security claims.
- [x] Limited labelled oracle metric: v0.9.1 13 synthetic fixtures, TP=9/TN=4/FP=0/FN=0; complete-token reversal handling fixed.
- [x] v0.6 model-report manifest implementation and verifier (SHA-256 of JSON/HTML), with exact model and Git provenance contract; full independent reproduction of every historical model run is **not** claimed.
- [x] v0.10 Ruff, Bandit, pip-audit (project metadata only), wheel/sdist verification and isolated wheel smoke test; PR #8 merged with green CI.
- [x] v1.0-rc1 source bundle builder/verifier, tamper tests, threat model; PR #9 head `f0e6a60` GitHub Actions run `43028293678` PASS across four jobs.
- [x] v1.0-rc1 maintainer-local unit tests 96/96 PASS (reported transcript).
- [x] Trivy v0.76.2 `secret` filesystem scan on `f0e6a60`: no findings reported.
- [x] Trivy v0.76.2 `vuln,misconfig` run: **documented as NOT SCANNED** (no supported files), not counted as a clean security result.
- [x] Documentation reconciled with v1.0-rc1 and GitHub CI; explicit runtime/host distinctions and review limitations.

## Release blockers for final v1.0.0

- [ ] Independent reviewer acceptance of code and trust boundaries; resolve or explicitly accept material review findings (see `docs/SECURITY_REVIEW.md`).
- [ ] If review changes code, rerun unit tests, Ruff/Bandit/pip-audit, CI and relevant Ollama probes on the new exact SHA.
- [ ] Review source provenance/attribution and verify no nonpublic training materials are included before publication.
- [ ] Decide and document whether `vuln,misconfig` scan needs alternative input/scope; do not misreport a skipped scan.
- [ ] Merge PR #9 only after review and CI acceptance; confirm `main` SHA and release version.
- [ ] Build/verify the **final release-commit** ZIP and manifest, record both SHA-256 values, attach artifacts to GitHub Release `v1.0.0`, and verify published release assets against the accepted commit.
- [ ] Update `Necraatall/Necraatall` profile README with the public project link and accurate release status (separate repo/change).

## Research enhancements beyond v1.0 (not automatically blockers)

- [ ] Complete independent labelling of live model false-positive/false-negative rates beyond the small synthetic oracle fixtures.
- [ ] Evaluate semantic/tool-mediated leakage and additional novel encodings, with explicit limitations.
- [ ] Verify/curate each original course-inspired scenario's authorship and any required attribution; do not import nonpublic course code.
- [ ] Assess more realistic authenticated write flows (current hardened demo deliberately allows no writes).
- [ ] Optional Trivy CI integration and immutable signed release provenance/attestations.
- [ ] Modernize SHA-pinned GitHub Actions to supported Node.js runtime and consider pinning a runner image; do not disguise host/runtime mismatch.

## Interpretation

`NO_BLOCKING_EVIDENCE`, clean unit tests and CI PASS are **scoped evidence, not a security certification**. Historical observations and current source revision must never be conflated.
