# Project status and TODO — public v0.5

**Publication completed on 2026-11-11; development is ongoing.** The open items below are real scope, not checkboxes to mark complete for cosmetic reasons.

## Completed and evidenced

- [x] Independent repository with no imported course Git history (initial commit `090f1a5`).
- [x] Synthetic tenant lab, 7/7 fixtures, and 43/43 local unit tests (v0.4/v0.5).
- [x] Optional Ollama experiment, bounded repeated probes, and JSON/HTML reports without raw model replies.
- [x] Extended canary oracle for supported plaintext/encoded/fragment cases; limitations documented.
- [x] Same-response output guard demonstration and honest distinction from an independent hardened target.
- [x] Real local Gemma experiment reported by user: 12 requests, six detected baseline leaks, six output blocks, no transport errors.
- [x] GitHub Actions offline checks on Python 3.11, 3.12, 3.13; PR #2: six successful checks.
- [x] Pin GitHub Actions dependencies to reviewed commit SHA values (PR #2).
- [x] Add MIT license and publication documentation (PR #2).
- [x] User-reported Trivy 0.76.2 scan of working tree and three reachable commit snapshots: zero findings (bounded scope).
- [x] Public visibility verified via GitHub CLI (`isPrivate: false`, 2026-11-11).

## Open — enhancements and research (do not misrepresent as finished)

- [ ] **v0.6:** Verify real local Ollama run and archived SHA-256 manifest; implementation/offline tests prepared. Capture model digest, Ollama version, coarse host environment, exact clean Git commit and report hashes. Full binary/runtime reproducibility is not claimed.
- [x] Independently reconstruct 20 FinanceBot scenario concepts without course scaffold (v0.7 offline implementation).
- [ ] Confirm original case authorship, run v0.7 on actual Ollama and add human-reviewed verdicts for non-secret goals.
- [x] v0.8: Add separate synthetic vulnerable and hardened state-mutation targets, independent requests, multi-turn scenarios and untrusted tool-output injection (offline tests).
- [ ] Validate v0.8 paired targets on local Ollama and independently review behavior/limitations.
- [x] v0.9: Measure narrow benign synthetic fee-read correctness and oracle confusion matrix against hand-labelled offline fixtures.
- [ ] Measure live model false positives/false negatives with independently labelled model responses; expand beyond narrow fee-read correctness.
- [x] v0.9: Add Base32 and fully percent-encoded marker detection with regression tests.
- [ ] Extend beyond supported encodings, including known reversed-marker blind spot and more realistic transformed/tool-mediated leaks.
- [ ] Evaluate optional Ruff, dependency/security scanning and package-build checks as additional CI quality gates.
- [ ] Collect independent review, broader threat-model evidence and full release reproducibility bundle for a future mature release.

## Scope boundaries

- The original training repository remains private and unchanged.
- Trivy scan success is not proof that no undiscovered secrets exist.
- `NO_BLOCKING_EVIDENCE` is not a model-safety certification.

- [ ] v0.9.1: Verify live benign correctness per target after prompt/schema alignment and attach results (pending user-run Ollama).
- [ ] v0.9.1: Record remaining detector limitations, including arbitrary encodings and semantic leakage.

- [x] v0.10 implementation: CI jobs for Ruff, Bandit, dependency metadata audit,
  wheel/sdist verification and isolated wheel import (CI execution pending).
- [ ] v0.10 verify new GitHub Actions job end-to-end and address real findings.
