## Why

The project needs a reproducible way to build and validate a PostgreSQL 16 STIG-hardened TimescaleDB HA image equivalent in scope to `timescale/timescaledb-ha:pg16-all`. Existing community baseline work appears to target earlier PostgreSQL versions, so PostgreSQL 16 applicability, gaps, and image-specific implementation details need to be established before code changes.

## What Changes

- Define a PostgreSQL 16 STIG implementation plan for the TimescaleDB HA Docker image, including which requirements are implemented in the image, which require deployment-time configuration, and which are documented exceptions.
- Establish a traceability model from STIG control identifiers to implementation, validation, and exception status without copying DISA STIG prose into this repository or related validation-profile work.
- Review the forked PostgreSQL STIG baseline for PostgreSQL 16 compatibility and identify updates needed for image validation.
- Add or adapt image configuration, runtime scripts, documentation, and CI checks needed to support STIG hardening while preserving the current non-STIG image behavior unless a STIG mode is explicitly selected.
- Provide a reproducible validation workflow that does not depend on a developer's personal machine setup; local Ruby or CINC/InSpec installations may be used for development, but CI and documentation should define portable execution.

## Capabilities

### New Capabilities

- `stig-control-traceability`: Covers how PostgreSQL 16 STIG controls are mapped to image implementation status, validation checks, deployment responsibilities, and documented exceptions.
- `stig-hardened-image-configuration`: Covers the Docker image and runtime configuration required to enable PostgreSQL 16 STIG hardening for a `pg16-all`-equivalent TimescaleDB HA image.
- `stig-validation-workflow`: Covers the reproducible audit workflow for validating the hardened image, including compatibility review of the forked baseline and required runner/tooling behavior.

### Modified Capabilities

None.

## Impact

- Affected repository areas may include `Dockerfile`, `Makefile`, root entrypoint scripts, `scripts/`, `build_scripts/`, `cicd/`, and documentation.
- The validation work may require coordinated changes in a forked PostgreSQL STIG baseline repository, especially if its profile metadata, inputs, controls, or examples assume PostgreSQL versions earlier than 16.
- The hardened image may need additional PostgreSQL settings, audit/logging behavior, file-permission checks, authentication guidance, and documented deployment inputs.
- Any required Ruby, CINC Auditor, or InSpec tooling must be documented as a reproducible runner dependency or containerized workflow rather than assumed to be installed locally.
