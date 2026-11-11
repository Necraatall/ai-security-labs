# Threat model — AI Security Labs v1.0 candidate

**Scope:** synthetic local agent experiments, local Ollama transport, GitHub CI and evidence. This is a model of *this repository*, not of banking infrastructure or arbitrary AI applications.

| Asset | Adversary / entry point | Trust boundary | Intended mitigation | Remaining risk |
| --- | --- | --- | --- | --- |
| Synthetic tenant/account state | Malicious end-user prompt | Model output → `FakeLedger.update_fee` | `HardenedTarget._authorized()` denies all untrusted writes in this demonstration | No genuine authenticated change path, no real customer system |
| Model system canary | Direct/multi-turn extraction | System prompt → untrusted output | Encoded/plaintext oracle, evidence without raw canary | Encoding/semantic transformations can evade finite oracle; public findings only for measured runs |
| Simulated retrieved rate card | Injected `notes` field | Untrusted retrieval → LLM | Trusted code, not retrieved text, decides whether to mutate state | The simulation inserts tool text as a `user` history item rather than a true function/tool role |
| Local Ollama request | Redirect/proxy/endpoint manipulation | Process → HTTP loopback | Local-only endpoint, redirect and proxy controls, bounded responses | Local malicious service/process and model binary remain trusted assumptions |
| CI dependency tooling | Registry compromise / vulnerable scanner | Remote package registry → runner | Explicit scanner versions, read-only checkout, security scans | Python package transitive dependencies not hash-locked; scans depend on vulnerability feeds |
| Published source | Modified/untracked files or artifact replacement | Git HEAD → release ZIP → consumer | Clean working tree, committed blobs, fixed ZIP encoding, per-file SHA-256 inventory | Manifest unsigned: attacker able to replace both artifacts can forge them |
| Experiment evidence | Altered report bytes | JSON/HTML → detached manifest | SHA-256 plus report identity checks | Model sampling/hardware not bitwise reproducible; manifest unsigned |

## Abuse scenarios / review priorities

1. Model claims that a retrieved document authorized a fee change. This must not grant `HardenedTarget` permission.
2. A legitimate fee lookup returns no fee. This must count as a failed benign task, even if no write occurred.
3. A model emits a marker in encoded form. Oracle tests require labelled TP/FP/TN/FN; zero failures on a small fixture set is not a safety guarantee.
4. An adversary tampers with a release ZIP or adds a different source file. Offline verification must fail.
5. A runner silently skips a tool or exits before scanning. Do not report those tools as passed without a completed GitHub job log.
6. An adversary replaces both source ZIP and unsigned manifest. **Not prevented**; release authenticity needs a trusted signed Git tag or signing/attestation workflow.

## Assumptions and acceptance boundary

- No financial credentials, customer data, bank APIs or real money exist in the laboratory.
- Red-team `VulnerableTarget` is intentionally unsafe; its findings are expected and should be recorded, not suppressed.
- The repository must not import third-party course code, course Git history or private attack transcripts.
- CI checks and local Ollama evidence belong to different scopes. Both must be separately reported.
- Code review findings remain distinct from a fully independent second reviewer. The author of the release changes cannot certify independence.
