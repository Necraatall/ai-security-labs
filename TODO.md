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
- [ ] Independently review and selectively reimplement *user-authored* FinanceBot cases with documented provenance; do not copy course scaffold or other students' code.
- [ ] Add separate vulnerable and hardened targets with independent requests, multi-turn scenarios and tool-mediated attack coverage.
- [ ] Measure benign task correctness and false-positive/false-negative rates, beyond marker leakage alone.
- [ ] Extend the oracle beyond currently supported Base64, hex, Unicode escapes and partial token detection; add regression coverage.
- [ ] Evaluate optional Ruff, dependency/security scanning and package-build checks as additional CI quality gates.
- [ ] Collect independent review, broader threat-model evidence and full release reproducibility bundle for a future mature release.

## Scope boundaries

- The original training repository remains private and unchanged.
- Trivy scan success is not proof that no undiscovered secrets exist.
- `NO_BLOCKING_EVIDENCE` is not a model-safety certification.
