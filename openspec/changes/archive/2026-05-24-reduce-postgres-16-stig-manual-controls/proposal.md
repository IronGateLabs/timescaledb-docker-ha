## Why

The PostgreSQL 16 STIG traceability baseline now accounts for all 111 controls, but 50 controls remain classified as `manual` because they do not yet have confirmed PostgreSQL 16 validation coverage or a project-owned implementation decision. The next step is to reduce that manual surface by reviewing the remaining controls, adding overlay validation where practical, and explicitly separating deployment-owned or true manual requirements from controls this repository can automate.

## What Changes

- Review the 34 `unmapped` PostgreSQL 16 controls, prioritizing the 17 severity-mismatch legacy candidates before controls with no legacy candidate.
- Reassess the 16 `manual_only` controls to determine whether they truly require human evidence or whether repository-owned overlay checks can cover part of the requirement.
- Add or extend validation overlay checks for controls that can be validated from the hardened image, PostgreSQL runtime state, container filesystem, or documented test inputs.
- Reclassify controls as `mapped`, `replaced_by_overlay`, `deployment_owned`, `manual_only`, or `exception` only after project-authored review notes justify the decision.
- Synchronize `stig/postgres16-control-mapping.json`, `stig/postgres16-v1r2-traceability.json`, reports, and documentation so the remaining manual count reflects reviewed decisions rather than unknown coverage.
- Preserve the existing default non-STIG image behavior and the opt-in STIG build/validation workflow.

## Capabilities

### New Capabilities

- `stig-manual-control-reduction`: Covers review and reclassification of PostgreSQL 16 controls currently marked manual or unmapped.
- `stig-overlay-control-validation`: Covers repository-owned overlay validation checks used to replace or supplement reusable legacy validation profile mappings.
- `stig-deployment-control-classification`: Covers explicit classification of controls that the Docker image cannot enforce because they depend on Kubernetes, identity, networking, secrets, certificates, backup policy, audit retention, or organization policy.

### Modified Capabilities

None.

## Impact

- Affected files include `stig/postgres16-control-mapping.json`, `stig/postgres16-v1r2-traceability.json`, `stig/postgres16-control-mapping-report.md`, `stig/postgres16-candidate-mapping-review.md`, and related STIG documentation.
- Validation overlay work may affect `stig/validation-overlay/controls/`, `stig/validation-overlay/inspec.yml`, `cicd/run-stig-validation`, `cicd/check-stig-mapping`, `cicd/check-stig-traceability`, and summary scripts under `scripts/stig/`.
- Some reviewed controls may identify deployment responsibilities rather than code changes; those decisions must be captured as project-authored metadata without copying benchmark prose.
- Any new validation must remain portable, avoid local paths or secrets, and run through the existing containerized CINC Auditor/InSpec workflow.
