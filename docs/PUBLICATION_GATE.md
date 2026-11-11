# Publication gate — Private → Public

Evidence cutoff: 2026-11-11. The entries below distinguish user-executed scans from independent CI results.

| Control | State | Evidence / limitation |
| --- | --- | --- |
| Independent repository history | PASS (user evidence) | New Git root at `090f1a5`; no course history imported. `git rev-list --all` returned 3 commits at audit time. |
| Offline unit tests | PASS | User ran 43/43 tests; six GitHub CI jobs succeeded on Python 3.11, 3.12 and 3.13 for PR #1. |
| Synthetic security evaluation | PASS | User ran 7/7 fixtures and strict evidence validation; this does not prove LLM safety. |
| Real Ollama experiment | PASS WITH SECURITY FINDINGS | User-reported Gemma run: 12 model requests, six observed plaintext/encoded marker exposures before output guard, six blocked, zero errors; local report not yet committed. |
| Course content / provenance | PASS FOR INCLUDED CONTENT, LIMITED | `docs/SOURCE_AUDIT.md` documents candidate files withheld. Original course modules, reports, and Git history were not incorporated. No claim of independent authorship for the original course. |
| Secret scan, working tree | PASS (user evidence) | Trivy 0.76.2, `fs --scanners secret`, exit 0, no findings. |
| Secret scan, reachable commits | PASS (user evidence) | Trivy 0.76.2 scanned exports of `cef87ab`, `15c594a`, `090f1a5`; exit 0 and no findings. Does not cover unreachable Git objects, remote-only refs, or all possible secrets. |
| GitHub Actions dependency pinning | IMPLEMENTED, PENDING CI | Checkout pinned to `11bd719...` (v4.2.2); setup-python pinned to `a26af69...` (v5.6.0). Verify in PR CI. |
| License | MIT PROPOSED FOR RELEASE | `LICENSE` copyright 2026 Necraatall; user selected MIT. Verify rights to all included independently authored files. |
| Final publication approval | PENDING | Visibility must remain Private until post-merge CI, final diff review, and explicit user instruction to make Public. |

**Decision: NO-GO until new PR checks pass and final release approval is given.**
