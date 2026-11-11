# v1.0 release candidate — verification contract

The v1.0 source bundle is created from **the exact committed Git HEAD**, not from local uncommitted source files. The ZIP has sorted entries, fixed timestamps and no compression; identical commit bytes yield identical release ZIP bytes. The detached manifest records the commit SHA, each committed file SHA-256 and the ZIP SHA-256. Any source file modification, non-ignored untracked file, symlink, missing file, forged inventory or archive modification must make creation or verification fail.

## Commands (after committing the v1.0 changes)

```bash
python3 -m unittest discover -s tests -v
python3 -m scripts.release_bundle create --repo . \
  --archive artifacts/source-release.zip \
  --manifest artifacts/source-release-manifest.json
python3 -m scripts.release_bundle verify \
  --archive artifacts/source-release.zip \
  --manifest artifacts/source-release-manifest.json
sha256sum artifacts/source-release.zip artifacts/source-release-manifest.json
```

`artifacts/` is Git-ignored. Do **not** publish private model conversations, local secrets or full environmental fingerprints. A release ZIP can be uploaded as a GitHub release asset only after CI and review.

## Evidence checklist

| Gate | Acceptance |
| --- | --- |
| Unit, Ruff, Bandit, pip-audit, wheel and sdist | Actual GitHub CI results for the exact PR or release commit; no unexecuted checks counted as PASS |
| Source bundle | `create`/`verify` succeeds for the clean released commit, SHA-256 and manifest retained |
| Local agent test | Explicit model name/digest, Ollama version, count of legitimate tasks and incidents, `gate` and limitations |
| Model reproducibility | Previous `compare_cli` has a separate detached manifest; source release manifest must not be substituted for it |
| Independent security review | Another reviewer checks trust boundaries and actual diff; unresolved findings receive severity and disposition |
| Publication provenance | Review confirms no imported instructor/student code or unauthorized data |

## Important limits

- A ZIP SHA-256 demonstrates integrity *relative to the detached manifest*, not provenance or authenticity when the manifest can also be replaced.
- The source bundle is deterministic, but rebuilds may not produce bitwise-identical Python wheels, model output or hardware runtime behavior.
- The reviewer and release owner must independently validate the published GitHub commit and attached asset before claiming a final release.
- A clean offline detector fixture set does not establish a production false-positive/negative rate.

**Current release status: CANDIDATE / NOT YET INDEPENDENTLY ACCEPTED.**
