# Input audit — candidate ZIP (no source files copied)

The input ZIP contained **10 candidate files** under `_review_only` across lessons 03, 04, 05 and 08. These files were **reviewed as reference material**, not incorporated into v0.1.

| Candidate | Preliminary finding | Decision |
| --- | --- | --- |
| 03/attacks/my_attacks.py | Custom-looking attack suite, tied to local chatbot HTTP contract | Withhold pending authorship and dependency review |
| 03/finance_chatbot.py | Depends on `utils.llm_client`, FastAPI and course context | Withhold |
| 03/bonusy_lekce03.py | References local model API and repo-specific fixture paths | Withhold |
| 04/guarded_travel_bot.py | Standalone guardrail code; needs ownership and threat model review | Withhold |
| 04/bonusy/run_bonuses.py | Needs `offline`, NeMo guardrails and other demo resources | Withhold |
| 04/bonusy/travel_presidio.py | Needs spaCy, Presidio and `guarded_travel_bot` | Withhold |
| 05/legal_rag_secure.py | Explicitly describes a lesson scaffold; imports missing `legal_rag` | Withhold |
| 05/test_legal_security.py | Course acceptance tests, imports missing `legal_rag` | Withhold |
| 08/run_homework.py | Requires PyRIT and modules from course redteam target | Withhold |
| 08/REPORT_Milan_lekce08.md | Student-labeled empirical report; real environment not rerun | Withhold pending evidence/provenance review |

The v0.1 project independently implements a small tenant-authorization and synthetic evaluation contract using only the Python standard library. It **does not claim** to have preserved capabilities of all 10 candidate files. Any future reuse must include a file-by-file provenance and license decision, dependency isolation, secret scan, and demonstrated tests.


    ## v0.2 update
    No original course Python files were copied. Four new minimal attack prompts use
    generic categories observed in the user's prior exercises, not the original prompt text.
    The original multi-turn suite and reports remain reference-only. Provenance and
    licensing audit of all ten candidates remains pending.

## v0.3 provenance note

This release implements new generic test primitives derived from the previously agreed goals. No original course source or Git history has been included. The user's original FinanceBot work is *not yet integrated*. Detailed review of original/teacher/student provenance, attribution and copyright remains a release blocker.
