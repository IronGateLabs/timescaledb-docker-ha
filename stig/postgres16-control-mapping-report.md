# PostgreSQL 16 Control Mapping Report

This report summarizes identifier-level mapping between the PostgreSQL 16 traceability inventory, the forked validation profile, repository-owned overlay checks, and reviewed deployment/manual decisions. It does not include benchmark prose.

## Current Result

- PostgreSQL 16 controls in traceability: 111.
- Legacy validation profile controls observed during generation: 113.
- Direct control ID overlap: 0.
- Candidate links by matching normalized `stig_id` suffix: 94.
- Candidate links with severity mismatch: 17.
- PostgreSQL 16 controls with no legacy candidate by `stig_id` suffix: 17.
- Current confirmed mapping status: 60 `mapped`, 18 `replaced_by_overlay`, 31 `deployment_owned`, 2 `manual_only`, 0 `unmapped`.
- Current automation status: 78 `partially_automated`, 31 `deployment_owned`, 2 `manual`, 0 `not_yet_assessed`.
- Traceability status after reviewed classification: 60 `validation_only`, 18 `image_enforced`, 31 `deployment_owned`, 2 `manual`.
- Of the 60 `validation_only` controls, 39 are `validation_state: executed` (their mapped legacy profile checks passed against the hardened image in the CI validation run) and 21 are `validation_state: candidate` (pending a portable legacy-check fix before the executed result is trustworthy). The remaining candidates are blocked by legacy-check portability issues (PostgreSQL 16 catalog/role-wording assumptions and two outright check bugs) to be addressed in the forked profile, not by the image.
- Remaining unmapped controls: 0.
- Remaining manual-only controls: 2.

## Interpretation

The forked validation profile cannot be treated as PostgreSQL 16 coverage by filename or control ID. The normalized `stig_id` suffix is useful for triage, but it is only a candidate signal. Reviewed reusable mappings remain `validation_only` unless this repository also owns the implementation evidence.

Reviewed traceability classification is conservative:

- controls with a reviewed legacy profile mapping are `validation_only` and must not be treated as image-enforced by this repository;
- controls with portable repository-owned PostgreSQL runtime, generated configuration, package, or filesystem evidence are `image_enforced` and linked to overlay checks;
- a control is `image_enforced` only when the hardened image fragment applies a concrete, observable setting; `V-261888` and `V-261892` were reclassified to `deployment_owned` because the image authors no role grants or host-based authentication rules for them and they passed only from PostgreSQL default state;
- controls that depend on Kubernetes, identity, networking, secrets, certificates, backup/log retention, patch timing, or organization policy are `deployment_owned`;
- controls without defensible repository-owned or deployment-owned automation remain `manual`;
- no controls are marked `exception`.

## Remaining Review Surface

All previously unmapped controls have been reviewed. The remaining manual-only controls are `V-261934` and `V-261954`; both require system-specific behavioral or data-model evidence that is not available from the generic image. Deployment-owned controls remain visible in traceability and reports so external implementation work is not hidden.
