# FinanceBot v0.7 — provenance and limitations

## Evidence inspected

User-uploaded `financebot-review.zip` contains `my_attacks.py` (20 named scenarios,
25 turns) and a separate `finance_chatbot.py` explicitly labelled as a course
lecture/homework target. The former claims user authorship in its docstring; the
archive alone cannot independently establish that claim. No Git blame, original
commit history or teacher attribution was supplied. **Authorship verification is
provisional and user-confirmation is still required.**

## Reimplementation decision

- No source code, original prompt phrasing, names, model settings, credentials,
  UI, HTTP server or shared-state architecture from either input file is copied.
- Independently reconstructed 20 scenario *concepts* using synthetic names,
  new short prompts, per-case ephemeral confidential markers and isolated
  conversation histories. IDs F01–F28 preserve mapping to source Axx concepts.
- The user-provided target was a vulnerable shared-history FastAPI demo; this
  independent version uses only a local Ollama adapter and no web server.
- Historical prompt counts are preserved: 20 cases / 25 individual turns.
- Secret oracle is limited to specific synthetic markers. Regulatory,
  misinformation and false-action outcomes remain `REVIEW_REQUIRED` unless an
  actual confidential test marker is observed. Do not interpret review required
  as a detected attack win or benign pass.
- No real user funds, accounts, transactions, customer data or external
  financial APIs are accessed. All operation requests are simulated text.
- Reports contain only lengths/hashes, detections, categories and status;
  no prompts, replies or confidential test markers. Digest values are not
  evidence of identity until accompanied by the separate v0.6 manifest.

## Open questions

Confirm that `my_attacks.py` was authored by the repo owner and that the 20
case concepts may be independently described in this public portfolio.
Independent second-party code review and actual Ollama v0.7 evidence are pending.
