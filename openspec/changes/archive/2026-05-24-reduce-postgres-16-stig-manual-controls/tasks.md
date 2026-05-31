## 1. Review Preparation

- [x] 1.1 Snapshot current STIG mapping and traceability counts for `mapped`, `manual_only`, `unmapped`, `validation_only`, `manual`, `deployment_owned`, `image_enforced`, and `exception`
- [x] 1.2 Create a working review list for the 17 severity-mismatch unmapped controls using identifiers and project-authored notes only
- [x] 1.3 Create a working review list for the 17 no-candidate unmapped controls using identifiers and project-authored notes only
- [x] 1.4 Create a working review list for the 16 `manual_only` controls and their current candidate context
- [x] 1.5 Confirm guardrail checks catch local paths, secrets, and copied prose in any new review artifacts introduced by this change

## 2. Severity-Mismatch Control Review

- [x] 2.1 Review each severity-mismatch control against the local reference material and candidate legacy validation logic without copying benchmark prose
- [x] 2.2 Classify each severity-mismatch control as `mapped`, `replaced_by_overlay`, `deployment_owned`, `manual_only`, or `exception`
- [x] 2.3 Record project-authored rationale for each severity-mismatch decision in the control mapping
- [x] 2.4 Add follow-up overlay tasks for severity-mismatch controls that have concrete repository-owned validation evidence
- [x] 2.5 Run STIG metadata guardrails after the severity-mismatch batch

## 3. No-Candidate Control Review

- [x] 3.1 Group no-candidate unmapped controls by implementation topic using identifiers, CCI references, and project-authored topic labels
- [x] 3.2 Review each no-candidate control against repository-owned image configuration, runtime behavior, overlay capability, documentation, and deployment boundaries
- [x] 3.3 Classify each no-candidate control as `replaced_by_overlay`, `deployment_owned`, `manual_only`, or `exception`
- [x] 3.4 Record project-authored rationale for each no-candidate decision in the control mapping
- [x] 3.5 Run STIG metadata guardrails after the no-candidate batch

## 4. Manual-Only Reassessment

- [x] 4.1 Review each `manual_only` control for concrete repository-owned evidence that can support partial overlay validation
- [x] 4.2 Keep controls as `manual_only` only when automation is not defensible from image, runtime, overlay, or deployment evidence
- [x] 4.3 Reclassify controls as `replaced_by_overlay` or `deployment_owned` when review identifies a better ownership boundary
- [x] 4.4 Record project-authored rationale for every retained or changed `manual_only` control
- [x] 4.5 Run STIG metadata guardrails after the manual-only reassessment batch

## 5. Overlay Validation Implementation

- [x] 5.1 Add or extend overlay checks for controls with concrete PostgreSQL runtime evidence
- [x] 5.2 Add or extend overlay checks for controls with concrete container filesystem, package, permission, or generated configuration evidence
- [x] 5.3 Ensure overlay checks do not assert controls that depend on organization policy, private deployment configuration, or human process evidence
- [x] 5.4 Link each new or changed overlay check from the corresponding control mapping entry
- [x] 5.5 Run the containerized STIG overlay validation workflow after overlay behavior changes

## 6. Deployment-Owned Classification

- [x] 6.1 Reclassify controls that depend on Kubernetes, operator behavior, pod security, service exposure, or runtime scheduling as deployment-owned
- [x] 6.2 Reclassify controls that depend on identity, networking, certificate lifecycle, secrets, backup retention, log retention, or organization policy as deployment-owned
- [x] 6.3 Extend schema and guardrail responsibility categories if existing enums cannot represent reviewed deployment responsibilities
- [x] 6.4 Update documentation or reports so deployment-owned controls remain visible and separate from failed, manual, and unreviewed controls

## 7. Synchronization and Reporting

- [x] 7.1 Synchronize traceability from reviewed control mapping decisions
- [x] 7.2 Regenerate or update the control mapping report with final reviewed counts
- [x] 7.3 Update the candidate mapping review summary so completed review categories are no longer presented as unresolved
- [x] 7.4 Ensure validation summaries distinguish pass, fail, manual, deployment-owned, exception, and unreviewed controls
- [x] 7.5 Verify no committed STIG artifact contains local source paths, secrets, or copied benchmark prose

## 8. Final Verification

- [x] 8.1 Run `cicd/check-stig-mapping`
- [x] 8.2 Run `cicd/check-stig-traceability`
- [x] 8.3 Run `cicd/check-stig-workflow`
- [x] 8.4 Run the containerized STIG validation workflow when overlay checks were added or changed
- [x] 8.5 Run `openspec validate reduce-postgres-16-stig-manual-controls --strict`
- [x] 8.6 Record final counts and remaining manual/deployment-owned rationale in the change notes or report
