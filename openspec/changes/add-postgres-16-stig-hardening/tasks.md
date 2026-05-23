## 1. Traceability Inventory

- [x] 1.1 Define the traceability file schema with fields for control ID, status, implementation owner, validation owner, deployment responsibility, and project-authored notes
- [x] 1.2 Create the initial PostgreSQL 16 control inventory using identifiers only and no copied benchmark prose
- [x] 1.3 Classify each control as image-enforced, deployment-owned, validation-only, manual, exception, or not yet reviewed
- [x] 1.4 Add a lightweight check that rejects personal paths, secrets, or copied benchmark prose patterns in committed traceability artifacts

## 2. Validation Profile Compatibility

- [x] 2.1 Review the forked PostgreSQL STIG validation profile metadata, inputs, examples, paths, packages, SQL assumptions, and control tags for PostgreSQL 16 gaps
- [x] 2.2 Create a PostgreSQL 16 TimescaleDB HA validation input example with portable placeholders only
- [x] 2.3 Update or overlay validation controls that assume pre-PostgreSQL 16 paths, package names, extension locations, or SQL behavior
- [x] 2.4 Define the PostgreSQL 16 control mapping schema and checker
- [x] 2.5 Generate the initial PostgreSQL 16 control mapping with all controls unmapped or directly matched
- [x] 2.6 Review mappings by control topic and link reusable legacy controls or overlay checks where defensible
- [x] 2.7 Record controls that cannot be automated in container validation as manual, deployment-owned, or exception in mapping and traceability

## 3. Hardened Image Build Path

- [x] 3.1 Add an opt-in STIG build mode or target that produces a distinct PostgreSQL 16 `pg16-all`-equivalent image variant
- [x] 3.2 Keep existing non-STIG build targets and default image behavior unchanged
- [x] 3.3 Add isolated STIG configuration fragments or scripts for PostgreSQL settings, auditing, logging, and file permissions
- [x] 3.4 Wire STIG configuration into initialization only when the hardened image or runtime mode is selected
- [x] 3.5 Verify required TimescaleDB, PostgreSQL 16, Patroni, pgBackRest, and bundled extension behavior still works in the hardened variant

## 4. Reproducible Validation Workflow

- [x] 4.1 Add a runner workflow for CINC Auditor or InSpec that runs outside the database image
- [x] 4.2 Provide a containerized or pinned runner path so validation does not require a local Ruby installation
- [x] 4.3 Add commands to launch the hardened image with documented validation inputs
- [x] 4.4 Generate validation output that can be mapped back to traceability statuses
- [x] 4.5 Ensure validation examples do not include local filesystem paths, host-specific values, or secrets

## 5. CI and Documentation

- [x] 5.1 Document how to build the STIG image variant and how it differs from the default image
- [x] 5.2 Document the boundary between image-enforced controls and deployment-owned controls
- [x] 5.3 Add CI checks for traceability format, shell changes, and the reproducible validation command once stable
- [x] 5.4 Document how forked validation-profile changes can be proposed upstream without including local-only assumptions

## 6. Final Verification

- [x] 6.1 Run the default build or existing checks to confirm non-STIG behavior is unchanged
- [x] 6.2 Build the STIG PostgreSQL 16 image variant and run smoke checks
- [x] 6.3 Run the reproducible validation workflow against the hardened image
- [x] 6.4 Update traceability with final pass, fail, manual, deployment-owned, and exception statuses
- [x] 6.5 Run `openspec validate add-postgres-16-stig-hardening --strict` and resolve any reported issues

Verification notes:

- `make latest` completed successfully with `STIG_ENABLED=false`, validating the normal non-STIG latest-image path.
- `make fast` was attempted first and failed while compiling TimescaleDB 2.17.0 for PostgreSQL 17 with a build jobserver error; that failure occurred outside STIG mode and was not used as the final non-STIG verification signal.
- Final traceability classification is conservative: 61 controls are `validation_only` through forked-profile mapping candidates, and 50 controls are `manual`.
