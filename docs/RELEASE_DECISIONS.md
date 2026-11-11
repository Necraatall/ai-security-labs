# Release decisions — v1.0.0

## SR-03 — Additional source archive distribution

The optional `source-release.zip` and `source-release-manifest.json`
were created, published and verified against SHA-256 for v1.0.0.
The owner decided to discontinue distributing these additional,
unsigned assets to reduce the number of artifacts to maintain and
the risk of misplaced trust in a detached unsigned manifest.

**Asset removal is pending confirmation.** Removing the additional
assets does not conceal the public source code, replace GitHub's
automatic source archives, or establish authenticity of the Git tag.
The implementation of the bundle generator may remain in the source
repository.

## SR-04 — Detector limitations and performance tradeoff

**Disposition: ACCEPTED_RISK (v1.0.0 synthetic demonstration).**

The deterministic detector recognizes defined synthetic markers and
selected encodings. Unknown prompt injections, transformations,
semantic leakage and external tool side effects may go undetected.
Additional semantic and multi-stage checks could improve coverage,
but introduce extra latency, computation cost and potential false
positives. They are deliberately not enabled by default in v1.0.0.
Future optional controls should be evaluated with measurable
detection accuracy and performance overhead.

This acceptance is not proof of comprehensive AI security or an
independent security audit.
