# Control Mapping Review Workflow

Use this workflow to turn candidate mappings into confirmed project decisions. Do not copy benchmark prose into review notes.

## Review Inputs

- `stig/postgres16-v1r2-traceability.json`: PostgreSQL 16 control IDs and metadata.
- `stig/postgres16-control-mapping.json`: current mapping state.
- `stig/postgres16-candidate-mapping-review.md`: high-priority candidate review list.
- Local validation-profile checkout: used as reference only.
- Local STIG source package: used as reference only.

## Decision Rules

- Use `mapped` only after reviewing that a legacy control's logic still applies to the PostgreSQL 16 control.
- Use `replaced_by_overlay` when this repository's overlay check is the better validation path.
- Use `manual_only` when the control depends on human review or organization-specific evidence.
- Use `deployment_owned` when Kubernetes, identity, networking, secrets, or organization policy must implement the control.
- Use `exception` only with project-authored rationale.
- Leave `unmapped` when the review is incomplete.

## Update Command

```console
scripts/stig/update_control_mapping.py \
  stig/postgres16-control-mapping.json \
  V-261857 \
  --mapping-status mapped \
  --legacy-control-ids V-233511 \
  --automation-status partially_automated \
  --container-validation partial \
  --validation-owner validation_profile \
  --notes "Project-authored rationale only."
```

Validate after each batch:

```console
cicd/check-stig-mapping
cicd/check-stig-traceability
```
