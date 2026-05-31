## Why

The PostgreSQL 16 STIG traceability baseline now inventories all 111 V1R2 controls, but the recorded posture is largely candidate mapping rather than executed validation or real enforcement:

- 67 controls are classified `validation_only`, yet every one references only reusable legacy profile controls (`legacy:V-233xxx`) that are not vendored here and are never run. `cicd/run-stig-validation` executes only the repository overlay, whose controls all carry InSpec `impact 0.0` (non-enforcing). A `validation_only` status therefore currently means "a candidate mapping exists," not "validated against this image."
- At least two controls (V-261888, V-261892) are classified `image_enforced` even though the hardened image applies no corresponding configuration (no `pg_hba` rules, no role grants); they pass only from PostgreSQL defaults.
- The hardened image is opt-in and disabled by default (`STIG_ENABLED=false`), so there is no single validated STIG-hardened artifact.

To reach a defensible STIG posture for the TimescaleDB HA image, mapped validation must actually execute against the hardened image, enforcement claims must match what the image configures, and the result must be gated in CI.

## What Changes

- Execute reusable legacy validation against the hardened image: reference the forked Crunchy PostgreSQL STIG profile as a portable InSpec dependency (not vendored) with TimescaleDB HA PostgreSQL 16 inputs, so mapped controls gain executed evidence.
- Author a portable TimescaleDB HA PostgreSQL 16 input file that overrides legacy PG12-15 defaults with this image's data directory, log directory, binary path, and package names, using placeholders only.
- Give overlay controls that assert a STIG requirement a non-zero InSpec impact and a stable V-26xxxx control reference, so a failing check fails the run and maps to traceability.
- Correct enforcement classification: a control is `image_enforced` only when the hardened image applies a concrete, observable setting; audit all 20 current `image_enforced` controls and reclassify those that pass only from defaults.
- Extend image enforcement to image-enforceable controls currently deferred (TLS, `pg_hba` authentication methods, role-privilege baselines, FIPS-mode signaling) where the image can defensibly own them.
- Distinguish candidate-mapped from validated in traceability, and make the guardrails reject `legacy-only` references presented as coverage.
- Add a CI job that builds or launches the hardened image and runs the full validation, publishing per-control results.
- Decide and document the default-hardening posture: a clearly built and validated hardened artifact (for example a dedicated STIG tag) versus documenting the default image as unhardened.
- Preserve the existing default non-STIG image behavior; never copy DISA benchmark prose; keep all inputs portable.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `stig-control-traceability`: Status semantics distinguish executed validation and real image enforcement from candidate mappings.
- `stig-overlay-control-validation`: Overlay controls that assert requirements must enforce (non-zero impact) and map to STIG control identifiers.
- `stig-validation-workflow`: Mapped legacy validation must execute against the hardened image and run in CI.
- `stig-hardened-image-configuration`: Image-enforceable transport, authentication, role, and FIPS controls are enforced by the image, and a distinct validated hardened artifact is published.

## Impact

- Validation: `stig/validation-overlay/inspec.yml`, `stig/validation-overlay/controls/`, `cicd/run-stig-validation`, `cicd/start-stig-validation-target`, a new portable PostgreSQL 16 input file, and `scripts/stig/summarize_inspec_results.py`.
- Traceability and guardrails: `stig/postgres16-v1r2-traceability.json`, `stig/postgres16-control-mapping.json`, `stig/traceability.schema.json`, `cicd/check-stig-traceability`, `cicd/check-stig-mapping`.
- Image: `scripts/stig/apply_stig_config.sh` and related initialization fragments; `Dockerfile` and `Makefile` STIG targets.
- CI: a new validation job under `.github/workflows/` that runs against a built hardened image.
- The forked Crunchy profile is referenced as a portable dependency by pinned git ref; its controls are not vendored, and no DISA benchmark prose is copied.
