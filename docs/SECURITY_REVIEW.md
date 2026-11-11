# Security review — v1.0-rc1 (preliminary, non-independent)

**Reviewed source identifier:** PR #9 head `f0e6a6044c2f8b2146bf705078daa044fa6d8c3d`, 2026-11-11.

**Scope:** static source and trust-boundary inspection for `security_lab/agent_targets.py`, `security_lab/core.py`, `security_lab/oracle.py`, `security_lab/ollama.py`, `scripts/release_bundle.py`, GitHub CI and available synthetic tests. This document is an AI-assisted review, **not** a blind independent assessment, formal penetration test or complete provenance audit. GitHub CI evidence is distinguished from reconstructed local test execution.

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| SR-01 | INFORMATIVE | Hardened target denies unauthorized synthetic writes in code using `_authorized()`; the intentionally vulnerable target grants them. The hardened demo implements no legitimate authenticated write flow. | Expected demo design; not production-ready authorization. |
| SR-02 | LOW | Simulated tool-output injection is passed as user-history text, not as a native structured tool-role message. | Disclose the fidelity limitation; advanced tool integration outside v1.0 scope. |
| SR-03 | MEDIUM | Both source ZIP and detached manifest are unsigned. A party that replaces both can produce a self-consistent forged pair; manifest commit field alone is not a trusted source attestation. | **OPEN for independent acceptance**; verify the published GitHub SHA against an independent trusted reference; signing/attestation future work. |
| SR-04 | MEDIUM | Finite canary oracle handles only recognized strings and selected encodings. General semantic leakage, transformed output, and tool side effects may bypass detection. | Documented limitation; avoid general claims of security or zero false negatives. |
| SR-05 | LOW | Trivy 0.76.2 secret scan on `f0e6a60` found no issues; Trivy `vuln,misconfig` found zero supported files, so nothing was scanned. | Report `NOT SCANNED`, not PASS. CI's pip-audit has no declared runtime dependency graph beyond project metadata. |
| SR-06 | LOW | CI uses `ubuntu-latest`, whereas maintainer development host is Ubuntu 22.04. SHA-pinned older GitHub Actions target deprecated Node.js 20 and runner forces Node.js 24. | Runtime mismatch and compatibility warnings documented. No invented Ubuntu/Node compatibility assurance. |
| SR-07 | LOW | Local Ollama HTTP is constrained to loopback, disallows proxies and redirects and caps response bytes. This does not protect against a malicious local process or compromised Ollama runtime. | Explicit trust assumption. |

**No proven critical/high exploit** was identified within the inspected code paths. That does **not** imply full absence of such defects outside the inspected scope. A distinct reviewer must validate this assessment before the release acceptance gate is checked.

## Evidence

- GitHub PR #9 commit `f0e6a60`, Actions run `43028293678`: four jobs PASS, including DevSecOps gate, Python 3.11/3.12/3.13.
- Maintainer transcript: `python3 -m unittest discover -s tests -v` **96/96 PASS**; local exact source Trivy v0.76.2 secret scan with no detected findings; vuln/misconfig: zero eligible input files.
- Tests and tools are bounded by their scopes. Full model re-execution on this PR revision, a blind second opinion, and the final public release asset are **NOT RUN / NOT PUBLISHED**.

## Release acceptance (still open)

1. Obtain a separate reviewer verdict on actual final changed code and acceptance of SR-03/SR-04 limitations.
2. Confirm attribution/provenance and any source-sharing restrictions.
3. Run all CI gates on the final commit after documentation changes and merge only on PASS.
4. Build deterministic source ZIP from the final accepted commit, verify, record SHA-256, attach to GitHub Release and check uploaded bytes.

**Verdict:** REVIEW_COMPLETED_WITH_LIMITATIONS / INDEPENDENT_ACCEPTANCE_PENDING. **Final release: NO-GO until acceptance.**
