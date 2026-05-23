# PostgreSQL 16 Control Mapping Report

This report summarizes identifier-level mapping between the PostgreSQL 16 traceability inventory and the forked validation profile. It does not include benchmark prose.

## Current Result

- PostgreSQL 16 controls in traceability: 111.
- Legacy validation profile controls observed during generation: 113.
- Direct control ID overlap: 0.
- Candidate links by matching normalized `stig_id` suffix: 94.
- Candidate links with severity mismatch: 17.
- PostgreSQL 16 controls with no legacy candidate by `stig_id` suffix: 17.
- Current confirmed mapping status: 61 `mapped`, 16 `manual_only`, 34 `unmapped`.
- Current automation status: 61 `partially_automated`, 16 `manual`, 34 `not_yet_assessed`.
- Traceability status after final classification: 61 `validation_only`, 50 `manual`.
- Remaining unmapped controls: 17 severity mismatches and 17 with no legacy candidate.

## Interpretation

The forked validation profile cannot be treated as PostgreSQL 16 coverage by filename or control ID. The normalized `stig_id` suffix is useful for triage, but it is only a candidate signal. Reuse still requires a control-by-control logic review, especially where severity changed or no candidate exists.

Final traceability classification is conservative:

- controls with a reviewed legacy profile mapping are `validation_only` and must not be treated as image-enforced by this repository;
- controls without a reusable PostgreSQL 16 mapping or overlay check are `manual`;
- no controls are marked `image_enforced`, `deployment_owned`, or `exception` without a project-owned implementation, deployment dependency, or exception rationale.

## Next Review Step

Review controls by `stig_id`, SRG/CCI metadata, and implementation topic, not by numeric `V-*` ID alone. Update `stig/postgres16-control-mapping.json` only with project-authored notes and portable references. Promote individual controls out of `manual` or `validation_only` only after PostgreSQL 16 logic is reviewed and the implementation owner is known.
