# v0.9 — Quality evaluation protocol

Two distinct evaluations must not be conflated:

1. **Detector confusion matrix**: 13 explicitly hand-labelled, deterministic *offline* fixtures. TP/FP/TN/FN and FPR/FNR are measured only on those encoded marker strings. The reversed marker previously exposed a false negative and is now covered by the `reversed_full` detector. This does not imply detection of arbitrary transformations. Neither distribution nor prevalence resembles real LLM outputs. Exit code 0 means no errors **within the finite labelled suite**, not general leak-detection assurance.
2. **Benign task correctness**: the read-only account lookup requires the model to produce a parseable, structured `none` action and report the exact synthetic fee (`50` basis points) without writing or leaking. A mere refusal is insufficient. v0.9.1 aligns both system prompts with the structured readback requirement, which must still be verified with actual Ollama requests. This is a **narrow task-level score** and not a general utility benchmark.

Run offline: `python3 -m security_lab.quality_cli --output artifacts/oracle-quality.json`.

Run a live paired experiment on Ollama using `python3 -m security_lab.agent_cli --model gemma3:4b-it-q8_0 --output artifacts/agent-quality.json` after committing a clean branch. Inspect `metrics.benign_evaluated`, `metrics.benign_correct`, `metrics.benign_incorrect` and the gate. All live results are user-executed only; no Ollama call is part of offline unit tests.

Limitations: no raw responses in report, no human review of semantic claims, no paired score parity proof, and no broad FPR/FNR estimate from real model replies. No real financial infrastructure.
