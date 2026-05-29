## 1. Baseline and Inputs

- [ ] 1.1 Snapshot current traceability counts (image_enforced, validation_only, deployment_owned, manual, exception) as the starting point for this change
- [ ] 1.2 Author a portable TimescaleDB HA PostgreSQL 16 InSpec input file that overrides legacy PG12-15 defaults with this image's data directory, log directory, binary path, and package names, using placeholders only
- [ ] 1.3 Confirm the input file contains no host-specific paths, hostnames, or secrets and passes the review-artifact guardrail

## 2. Execute Mapped Legacy Validation

- [ ] 2.1 Reference the forked Crunchy PostgreSQL STIG profile as a portable InSpec dependency (pinned git ref) without vendoring its controls into this repository
- [ ] 2.2 Wire the dependency into `cicd/run-stig-validation` so the mapped legacy controls execute against the hardened image alongside the repository overlay
- [ ] 2.3 Run the combined validation against a launched hardened image and capture per-control results
- [ ] 2.4 Verify per-control PostgreSQL 16 behavior for the legacy-mapped controls before treating any as authoritative coverage

## 3. Correct Enforcement Classification

- [x] 3.1 Audit all 20 controls currently classified `image_enforced` against `scripts/stig/apply_stig_config.sh` and the hardened image configuration
- [x] 3.2 Reclassify controls that pass only from PostgreSQL defaults (including V-261888 and V-261892) to `deployment_owned`, `validation_only`, or `manual` with project-authored rationale
- [x] 3.3 Update `stig/postgres16-control-mapping.json` and traceability to record the corrected ownership

Notes: the audit (adversarially verified) confirmed only V-261888 and V-261892 were falsely labeled `image_enforced` (no `pg_hba`/role enforcement in the image); both reclassified to `deployment_owned`, leaving 18 `image_enforced` / 24 `deployment_owned`. The audit also flagged 5 "unsuccessful access/privilege" controls (V-261922, V-261943, V-261945, V-261953, V-261963) where image enforcement is genuine but the overlay under-validates — addressed under section 4 (non-zero impact / failed-attempt assertions), not a reclassification.

## 4. Overlay Enforcement and Mapping

- [ ] 4.1 Give overlay controls that assert a STIG requirement a non-zero InSpec impact
- [ ] 4.2 Tag each asserting overlay control with its V-26xxxx control identifier so results map to traceability
- [ ] 4.3 Label remaining preflight or input-shape checks as informational and exclude them from coverage counts
- [ ] 4.4 Re-run the overlay and confirm a deliberately failing check fails the run

## 5. Extend Image Enforcement

- [ ] 5.1 Identify image-enforceable controls currently deferred to deployment (TLS, `pg_hba` authentication methods, role-privilege baselines, FIPS-mode signaling)
- [ ] 5.2 Add isolated STIG configuration fragments that apply these settings only in the hardened image or runtime mode
- [ ] 5.3 Add overlay checks that observe each newly enforced setting
- [ ] 5.4 Reclassify the newly enforced controls to `image_enforced` with executed validation evidence

## 6. Guardrails and Status Semantics

- [ ] 6.1 Extend `cicd/check-stig-traceability` to reject legacy-only validation references presented as validated coverage
- [ ] 6.2 Update the traceability schema and status semantics to distinguish candidate-mapped from executed/validated
- [ ] 6.3 Reclassify the legacy-only `validation_only` controls to candidate-mapped except those proven by an executed run
- [ ] 6.4 Ensure validation summaries distinguish executed pass/fail from candidate, manual, deployment-owned, and exception

## 7. CI Integration

- [ ] 7.1 Add a CI job that builds or launches the hardened image and runs the full STIG validation
- [ ] 7.2 Publish per-control results as a CI artifact mappable to control identifiers
- [ ] 7.3 Gate the job so STIG configuration, overlay, or input changes trigger validation

## 8. Default-Hardening Posture

- [ ] 8.1 Decide whether to publish a distinct validated hardened artifact (for example a STIG tag) or document the default image as unhardened
- [ ] 8.2 Document the chosen posture, how to obtain the hardened artifact, and how it differs from the default image
- [ ] 8.3 Confirm the default non-STIG image behavior is unchanged

## 9. Final Verification

- [ ] 9.1 Run `cicd/check-stig-mapping`
- [ ] 9.2 Run `cicd/check-stig-traceability`
- [ ] 9.3 Run `cicd/check-stig-workflow`
- [ ] 9.4 Run the containerized STIG validation workflow against the hardened image and record final per-control results
- [ ] 9.5 Update traceability with final executed pass, fail, candidate, manual, deployment-owned, and exception statuses
- [ ] 9.6 Run `openspec validate execute-postgres-16-stig-validation --strict` and resolve any reported issues
- [ ] 9.7 Verify no committed STIG artifact contains local paths, secrets, or copied benchmark prose
