# Publication record — v0.5 (2026-11-11)

**Actual status: PUBLIC.** This document records the observed release process; it is no longer a prepublication NO-GO checklist. Evidence described as user-reported was executed on the user's machine, not independently reproduced here.

| Release control | Result | Evidence / scope |
| --- | --- | --- |
| Git repository boundary | PASS (user evidence) | Independent Git root `090f1a5` with no imported course history; three reachable commits at audit time |
| Tests | PASS (user evidence) | Local 43/43 unit tests; 7/7 synthetic fixtures; evidence validator PASS |
| GitHub CI | PASS (user evidence) | PR #1 and PR #2 each had six successful checks across Python 3.11–3.13 |
| Local Ollama demonstration | PASS WITH SECURITY FINDINGS | 12 requests, six unprotected baseline canary leaks, six same-response output blocks, zero transport errors; not a general security proof |
| Source provenance | LIMITED REVIEW | Only independently created portfolio lab files included; candidate course/student source withheld per `SOURCE_AUDIT.md`; independent forensic authorship audit not claimed |
| Working tree secret scan | PASS (user evidence) | Trivy 0.76.2 `fs --scanners secret`, exit 0, zero findings |
| Reachable commit snapshots | PASS (user evidence) | Trivy 0.76.2 scanned exported commits `090f1a5`, `15c594a`, `cef87ab`; no findings. Excludes unreachable Git objects and unknown detection gaps |
| GitHub Actions dependencies | IMPLEMENTED, CI PASS | SHA-pinned `actions/checkout` v4.2.2 and `actions/setup-python` v5.6.0 in PR #2 |
| License | MIT | `LICENSE` added in merged PR #2 |
| Publication | COMPLETE (user evidence) | PR #2 merged into `main` (`d6488c3`); `gh repo view` returned `isPrivate: false` on 2026-11-11 |

**Release conclusion:** public portfolio baseline published. Open research, source-review and reproducibility improvements remain in `TODO.md`. The lab is not a certification of model safety and does not establish independent hardened-target security.
