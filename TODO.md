# AI Security Labs — delivery status, release gates and research backlog

**Current status (2026-11-11):** Public, MIT-licensed **v1.0.0rc1 code merged into `main`** via PR #9 (`e80f5cbbc884ee8aa644344ec6f3b52126a92125`). The final GitHub Release **v1.0.0 has not been verified as published**. Checkboxes reflect completed, evidenced work, not the percentage of the entire research roadmap.

## Completed milestones — v0.1 through v1.0.0rc1

### Public repository and baseline (v0.1–v0.5.1)

- [x] Create a standalone public repository, without importing private training repository history or course code; publish under MIT.
- [x] Implement the synthetic tenant-boundary lab, strict evidence verification and negative tests; verify 7/7 synthetic fixtures.
- [x] Add local Ollama attack demonstrations with bounded repeated probes, output guard, and JSON/HTML reports omitting raw replies and canary values.
- [x] Extend the canary oracle for supported plaintext and encoded forms; state detection limits and possible false positives.
- [x] Add Python 3.11/3.12/3.13 offline CI and pin GitHub Actions to commit SHAs.
- [x] Perform earlier bounded Trivy secrets checks on the working tree and historical reachable commits; record scope and avoid claiming exhaustive coverage.

### Reproducibility, scenarios and agents (v0.6–v0.8.1)

- [x] Implement model/host/Git provenance collection and detached SHA-256 report manifests; provide a strict offline verifier (v0.6).
- [x] Reconstruct 20 synthetic FinanceBot scenarios covering 25 turns independently of the private course scaffold (v0.7).
- [x] Implement separate vulnerable/hardened fake-ledger targets, isolated state and model requests, multi-turn scenarios and simulated untrusted tool output (v0.8).
- [x] Treat unparseable agent JSON and transport errors as inconclusive/failing rather than as successful safety evidence (v0.8.1).
- [x] Record user-reported local Gemma3 agent experiment: 12/12 requests, 3 vulnerable unauthorized writes, 0 hardened writes, 0 errors/unparseable; `REVIEW_REQUIRED`. Results are bounded to that run.

### Detector quality and measurable benign behavior (v0.9–v0.9.1)

- [x] Add explicit synthetic benign-fee read correctness and a hand-labelled oracle confusion matrix.
- [x] Add Base32, percent-encoded and complete reversed-marker recognition with regression tests.
- [x] Verify 13 labelled synthetic fixtures: TP=9, TN=4, FP=0, FN=0; these are not production model error rates.
- [x] Record user-reported Gemma3 live experiment: 42/42 requests, benign correct 12/12, vulnerable unauthorized writes 7, hardened writes 0, vulnerable leaks 1, hardened leaks 0, 0 transport/unparseable errors; `REVIEW_REQUIRED`.

### CI, security checks and release candidate (v0.10–v1.0.0rc1)

- [x] Merge v0.10 DevSecOps gate in PR #8; verify Ruff, Bandit (medium/high), pip-audit on declared project metadata, wheel/sdist, archive validator and installed-wheel smoke test in CI.
- [x] Implement an unsigned deterministic source ZIP for the exact committed Git snapshot, detached per-file SHA-256 inventory, full archive verification and negative tamper tests.
- [x] Add a threat model, environment documentation and an AI-assisted security review with clearly stated scope/limitations.
- [x] Verify 96/96 maintainer-local unit tests and successful Ruff check for the v1.0 release-candidate branch (user-provided terminal transcript).
- [x] Verify GitHub Actions for PR #9 head `f9beda31a91d586cdf9ee015a4ee5aeac6add96a` (workflow `43034308211`): DevSecOps gate plus Python 3.11, 3.12 and 3.13 jobs PASS.
- [x] Run Trivy v0.76.2 filesystem `secret` scan at `f0e6a60`: no findings reported.
- [x] **Record scan coverage honestly:** Trivy `vuln,misconfig` identified no supported inputs, therefore result was **NOT SCANNED**, not a clean scan.
- [x] Merge release-candidate PR #9 into `main` as `e80f5cbbc884ee8aa644344ec6f3b52126a92125` (2026-11-11).

## Required to close the final v1.0.0 release

- [ ] Obtain a separate reviewer acceptance of code, trust boundaries and the AI-assisted review report, or explicitly document a maintainer acceptance with its independence limitation; resolve/disposition any material findings.
- [ ] Confirm source provenance and third-party attribution, including absence of nonpublic course materials in the published source snapshot. A bounded secrets scan alone does not establish this.
- [ ] Decide and record how dependency and configuration scanning applies to this standard-library-only project. Do not turn Trivy's `NOT SCANNED` into `PASS`; retain pip-audit's narrower CI evidence.
- [ ] Confirm `main` HEAD, release version and CI on the exact intended final commit; if code changes, rerun relevant tests/scanners and local Ollama probes where their claims depend on the revision.
- [ ] Set final package version to `1.0.0` consistently in packaging metadata, distribution validation and tests; build and verify wheel/sdist from that exact commit.
- [ ] Build and verify the **final committed-source ZIP and manifest**, record SHA-256 for both files and publish the corresponding artifacts with GitHub Release `v1.0.0` (avoid claiming a signed attestation).
- [ ] Verify the published tag, target commit, attached assets and their hashes; record final evidence in release documentation.
- [ ] Update the `Necraatall/Necraatall` profile README with a direct link and the actually published release status.

## Research backlog — v1.1+ (not a v1.0 completion metric)

- [ ] Independently label broader real-model samples and estimate false-positive/false-negative rates outside the narrow synthetic oracle fixtures.
- [ ] Study semantic, tool-mediated and other unrecognized exfiltration patterns, documenting residual detection limits.
- [ ] Perform deeper per-case human assessment and provenance/attribution curation for course-inspired scenarios without importing nonpublic material.
- [ ] Extend hardened target to realistic, separately authenticated write authorization and approval flows; current demo deliberately allows no writes.
- [ ] Optionally add Trivy scanning to CI with explicitly supported inputs and a meaningful scanner scope.
- [ ] Consider signed release provenance/attestation and stricter reproducible-build evidence.
- [ ] Modernize SHA-pinned GitHub Actions to a supported Node.js runtime and pin CI runner image if reproducibility requires it. The developer workstation uses Ubuntu 22.04; current CI uses `ubuntu-latest`, **not** a pinned 22.04 runner.

## Evidence interpretation

- **Completed implementation** is not equivalent to **certified safety** or complete independent verification.
- Historical Ollama observations, offline synthetic results and current commit-specific CI must not be conflated.
- The source-release manifest is unsigned; it detects mismatches against its recorded hashes but does not independently prove the author's identity.
- The research backlog is intentionally excluded from final v1.0 release readiness.
