# PostgreSQL 16 Control Mapping Report

This report summarizes identifier-level mapping between the PostgreSQL 16 traceability inventory, the forked validation profile, repository-owned overlay checks, and reviewed deployment/manual decisions. It does not include benchmark prose.

## Current Result

- PostgreSQL 16 controls in traceability: 111.
- Legacy validation profile controls observed during generation: 113.
- Direct control ID overlap: 0.
- Candidate links by matching normalized `stig_id` suffix: 94.
- Candidate links with severity mismatch: 17.
- PostgreSQL 16 controls with no legacy candidate by `stig_id` suffix: 17.
- Current confirmed mapping status: 50 `mapped`, 24 `replaced_by_overlay`, 32 `deployment_owned`, 3 `exception`, 2 `manual_only`, 0 `unmapped`.
- Current automation status: 74 `partially_automated`, 32 `deployment_owned`, 3 `exception`, 2 `manual`, 0 `not_yet_assessed`.
- Traceability status after reviewed classification: 50 `validation_only` (all 50 `executed`, 0 `candidate`), 24 `image_enforced`, 32 `deployment_owned`, 3 `exception`, 2 `manual`.
- Six controls the hardened image directly sets (client_min_messages, statement_timeout, log_hostname, the `%c`/`%a`/`%s` log-prefix fields, and pgaudit.log_catalog → V-261862/910/913/932/941/950) were moved from forked-profile validation to `image_enforced` with repository-owned overlay checks, so their validation no longer depends on the external profile.
- All 50 `validation_only` controls are `validation_state: executed` — their mapped legacy profile checks passed against the hardened image in the CI validation run; there are no remaining `candidate` controls. Every one of the 111 V1R2 controls is now affirmatively classified: 24 `image_enforced`, 50 executed `validation_only`, 32 `deployment_owned`, 3 documented `exception`, 2 `manual`.
- Getting there required: 14 PostgreSQL 16 / Debian / SCRAM portability fixes to the forked Crunchy profile (pinned via the `pg16-portability-2` tag); image hardening (`client_min_messages`, `statement_timeout`, `log_hostname`, the `%c`/`%a`/`%s` log-prefix fields, `pgaudit.log_catalog`, and `ALLOW_ADDING_EXTENSIONS=false` for immutable `root:root 0755` bin/lib); hardening the Spilo `log_file_mode` to `0600`; clearing stale build-time logs in the disposable validation target; reclassifying TLS (`ssl`) and the bootstrap-superuser/pgaudit-policy controls to `deployment_owned` and documented `exception`; and moving six image-set controls to `image_enforced` with repository-owned overlay checks.
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
