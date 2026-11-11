# Publication gate — Private → Public

| Control | State | Evidence |
| --- | --- | --- |
| Independent Git root, no imported course history | PASS per user's initial Git log | Initial commit `090f1a5` was created with `git init`; **full Git history not independently scanned** |
| Offline unit tests | PASS (local build) | v0.4 test execution report; CI run still NOT RUN |
| Synthetic evaluation and structural evidence gate | PASS (local build) | Standard-library synthetic checks; no LLM calls |
| Real local model exercise | USER-REPORTED PASS WITH FINDINGS | `docs/LOCAL_EVIDENCE.md`; baseline model leaked in 6 requests |
| Provenance of original homework code | PENDING | Not copied; no confirmation of detailed provenance required if not reused |
| Sensitive file/content inspection | PARTIAL | Current extracted tree inspected by local filename/string pattern checks; Git history and GitHub secret scanning NOT RUN |
| CI on GitHub | NOT RUN | `.github/workflows/quality.yml` prepared but must run after push |
| Pinned GitHub Actions dependencies | OPEN | Action tags use major versions; replace with reviewed SHA pins before strict release |
| License / reuse rights | OPEN | No license selected; decide terms for independently authored code |
| Public release approval | NOT GIVEN | Explicit separate approval required |

**Decision:** NO-GO for changing visibility to Public until remaining checks and authorization are complete. This document is a release checklist, not proof that all controls are met.
