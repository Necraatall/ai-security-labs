# Reproducibility contract — v0.6

## Evidence sources

- Ollama `GET /api/version`: runtime server version, locally supplied by Ollama.
- Ollama `GET /api/tags`: exactly matching **installed model tag**, its SHA-256 digest.
  Different or ambiguous tag names are rejected. This does not verify the publisher.
- Git: exact local `HEAD` commit; dirty tracked worktree rejected before any LLM call.
  Untracked and ignored files are not checked, so record external configuration separately.
- Coarse environment: OS, OS release, architecture, Python implementation/version,
  loopback port. No hostname, account name, IP of external network or environment vars.
- Request contract: repeats, `temperature=0`, `num_predict=256`, independent single-turn
  probes, random 96-bit marker per repetition, fixed local attack cases (from Git commit).
- Report digests: SHA-256 of JSON and HTML exact file bytes in a detached manifest.

## Verification

Run `python3 -m scripts.verify_repro_bundle artifacts/repro-manifest.json artifacts/comparison.json artifacts/comparison.html`.
Exit 0 indicates integrity and schema consistency for the supplied local files.
Report and manifest must be preserved together. There is no digital signature,
trusted timestamp, chain of custody or signature over this manifest.

## Limits and acceptance

- Model digest and Ollama version are captured before probe execution, not rechecked
  atomically during inference. Do not change the installed tag during a run.
- Model output may vary despite `temperature=0` due to version/hardware/runtime effects.
- No full environment image, lockfile for Ollama, GPU driver/firmware fingerprint or seed
  is preserved. Consequently this is **traceability**, not bit-for-bit reproducibility.
- If metadata cannot be obtained, or a tracked source file is uncommitted, the CLI exits
  **2** and does not start probes; no fabricated metadata is used.
- Real local acceptance needs an actual Ollama run with the merged v0.6 source,
  a reported exit status, and successful offline manifest verification.
- Keep local `artifacts/` private unless deliberately reviewed for public distribution.
