# Development environment and CI runtime

## Local host

The maintainer reports **Ubuntu 22.04 LTS** as the development OS. Ubuntu `22.06` is not the release name. Local Python tooling and optional Ollama are explicitly separate from the CI environment. A successful local test is evidence for the reported machine, not proof of every OS version.

## GitHub Actions

At PR #9 (`f0e6a60`) `.github/workflows/quality.yml` uses **`runs-on: ubuntu-latest`**, not `ubuntu-22.04`. GitHub warns that `ubuntu-latest` is migrating to Ubuntu 26. Therefore the statement “the project uses the same Ubuntu version locally and in CI” is **not currently true**. Pinning the CI runner should be a separate tested change, not a documentation-only assertion.

The workflow pins `actions/checkout` to commit `11bd71901bbe5b1630ceea73d27597364c9af683` (v4.2.2) and `actions/setup-python` to commit `a26af69be951a213d495a4c3e4e4022e16d87065` (v5.6.0). These action revisions target **Node.js 20**. On 2026-11-11 the GitHub runner warned that it **forces Node.js 24**. The application itself is Python-based and does **not** declare Node.js 20 as its runtime requirement.

SHA-pinning was chosen for reviewable action identity; it is **not evidence** that Node.js 20 is optimal for library interoperability. Node.js 20 is deprecated in this Actions context and should be migrated using tested, up-to-date SHA pins. Avoid disabling warnings or suppressing failures.

## Verified scope

PR #9 GitHub run `43028293678`: DevSecOps gate and Python 3.11/3.12/3.13 checks passed. No real Ollama run, Trivy vulnerability scan or host-parity check occurs inside this workflow. External tools, vulnerability feeds and CI runner labels may change over time.
