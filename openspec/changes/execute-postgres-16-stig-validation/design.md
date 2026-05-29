## Context

The `add-postgres-16-stig-hardening` and `reduce-postgres-16-stig-manual-controls` changes inventoried all 111 PostgreSQL 16 V1R2 controls and reduced the manual surface to two. However an audit found the recorded posture is largely candidate mapping rather than executed validation or real enforcement (see proposal). This change closes that gap so the TimescaleDB HA image has a defensible, reproducible STIG posture.

## Goals

- Executed validation evidence for controls currently mapped only to an unrun legacy profile.
- Enforcement classifications that match what the hardened image actually configures.
- A CI-gated validation run against a built hardened image.
- A clearly identified, validated hardened artifact.

## Non-goals

- Copying DISA U_CD benchmark prose or the Crunchy profile controls into this repository.
- Hardening the default (non-STIG) image or changing its behavior.
- Upstream contributions to the forked profile (deferred per `stig/upstream-profile-contribution.md` until local verification completes).

## Key decisions

1. **Reference, do not vendor.** The forked Crunchy PostgreSQL STIG profile is consumed as a portable InSpec dependency (pinned git ref). Image-specific glue stays in the repository overlay. This keeps the legacy controls runnable without duplicating them and without coupling to a local checkout path.
2. **Inputs are portable.** A single TimescaleDB HA PostgreSQL 16 input file maps this image's real layout (data dir, log dir, binary path, package names) to the profile's expected inputs using placeholders, so the legacy controls evaluate correctly without false path or package failures.
3. **Status honesty.** Traceability gains a clear boundary between candidate-mapped (a defensible mapping exists) and validated (a check ran against this image). Guardrails enforce that boundary so coverage cannot silently regress to paper.
4. **Enforce what the image can own.** TLS, `pg_hba` authentication, role-privilege baselines, and FIPS signaling are applied by the hardened image where defensible; everything genuinely external stays deployment-owned with rationale.

## Open questions

- Profile dependency source: pin to the forked repository's git ref, or publish the profile to a shared InSpec location? (Default: pinned git ref to the fork.)
- FIPS-mode signaling depends on the base image and host crypto policy; determine how much the container can assert versus what stays deployment-owned.
- Whether to ship a dedicated STIG-hardened image tag in the release pipeline or keep the STIG build opt-in and documented.
