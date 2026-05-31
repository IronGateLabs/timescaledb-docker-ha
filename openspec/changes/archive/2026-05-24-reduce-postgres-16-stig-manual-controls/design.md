## Context

The current PostgreSQL 16 STIG baseline records 111 controls in traceability and has repository guardrails for traceability, mapping, and validation workflow metadata. The conservative final classification from the previous change leaves 61 controls as `validation_only` and 50 controls as `manual`; within the mapping file, 34 controls are still `unmapped` and 16 are `manual_only`.

The local unclassified STIG source package is available as reference material for review, but it must not be copied into this repository. Repository artifacts may include control identifiers, rule identifiers, severities, CCI references, project-authored rationale, validation references, and implementation evidence. They must not include benchmark prose, local filesystem paths, secrets, or machine-specific assumptions.

This change is a review and reduction pass. The goal is not merely to lower the manual count, but to make each remaining manual classification intentional and defensible while validating which controls are actually implemented by this repository's STIG image mode, overlay checks, or deployment guidance.

## Goals / Non-Goals

**Goals:**

- Review all 34 `unmapped` controls and decide whether each can be mapped to existing validation logic, replaced by a repository-owned overlay check, assigned to deployment ownership, classified as true manual evidence, or documented as an exception.
- Reassess all 16 `manual_only` controls for possible partial automation through overlay checks or repository-owned evidence.
- Validate implementation claims against repository behavior: STIG configuration scripts, Docker image build inputs, runtime PostgreSQL settings, container filesystem state, validation overlay controls, and documented deployment responsibilities.
- Keep traceability and mapping synchronized so control status reflects reviewed implementation and validation evidence.
- Preserve the existing opt-in STIG behavior and avoid changing default non-STIG image behavior.

**Non-Goals:**

- Do not import, vendor, or quote STIG benchmark prose into this repository.
- Do not claim full STIG compliance from a Docker image alone.
- Do not require Ruby, CINC Auditor, InSpec, or validation-profile tooling inside the database image.
- Do not automate controls that require organization-specific human evidence unless the automation can validate a concrete repository-owned or deployment-owned signal.
- Do not encode local absolute paths, local usernames, credentials, tokens, or source package locations into committed artifacts.

## Decisions

1. Review from identifiers and local reference material, not copied benchmark text.

   The review process may consult the local source package to understand a control, but committed artifacts must remain project-authored and identifier-level. Notes should explain the repository decision in original language, such as "validated by overlay check for configured setting" or "deployment-owned because certificate issuance is outside the image." Alternative considered: extract titles or check text into review files for convenience. That would violate the repository content boundary and increase licensing and leakage risk.

2. Treat `unmapped` as unknown, not manual.

   The 34 `unmapped` controls should be reviewed first because they still represent incomplete analysis. Severity-mismatch candidates get priority since they have possible reusable validation logic but need stricter review before reuse. Controls with no legacy candidate should be grouped by topic and checked against repository implementation points. Alternative considered: leave all 34 as manual. That preserves a conservative status, but it does not answer whether this repository already implements or can validate them.

3. Use overlay checks only for concrete, portable evidence.

   A repository-owned overlay check is appropriate when it can verify a stable signal from the validation target, such as a PostgreSQL setting, loaded extension, audit/logging configuration, file permission, package/runtime presence, or documented test input. Overlay checks should not assert organization policy by assumption. Alternative considered: write placeholder overlay checks for every manual control. That would create false confidence and brittle validation.

4. Separate implementation ownership from validation ownership.

   A control may be implemented by image configuration, deployment policy, documentation, or manual process, while validation may be performed by the forked profile, repository overlay, manual review, or deployment evidence. Mapping and traceability updates should record these separately. Alternative considered: use a single status field as the source of truth. That loses important detail for controls that are implemented outside the image but can still be partially validated.

5. Make deployment-owned controls explicit instead of leaving them manual.

   Controls depending on Kubernetes admission policy, network segmentation, external identity, secrets management, certificate lifecycle, backup retention, log retention, or organizational audit process should move to `deployment_owned` when the dependency is clear. The notes should identify the responsibility category without prescribing a specific private environment. Alternative considered: keep deployment dependencies as manual. That makes the manual count less useful and hides work that belongs outside this image repository.

6. Synchronize traceability from reviewed mapping decisions.

   The mapping file should drive detailed review state, while traceability should summarize the resulting implementation and validation classification. After each batch, run the existing synchronization/check scripts and update reports so counts remain consistent. Alternative considered: edit traceability directly during review. That risks divergence between the detailed mapping and final status.

## Risks / Trade-offs

- Misclassifying policy controls as image-enforced -> Require concrete repository-owned evidence before using `image_enforced` or `replaced_by_overlay`.
- Reusing legacy validation logic incorrectly for PostgreSQL 16 -> Review SQL, paths, packages, version assumptions, and severity changes before promoting a candidate mapping.
- Committing source package prose or local paths by accident -> Keep guardrail checks in the workflow and extend them if new review artifacts are added.
- Overlay checks may pass in local validation but fail in Kubernetes deployments -> Limit overlay checks to portable image/runtime facts and classify environment-specific controls as deployment-owned.
- Manual count may remain high after review -> Treat a smaller, better-justified manual set as success when automation is not defensible.

## Migration Plan

1. Preserve the completed baseline change as the starting point and keep existing non-STIG build behavior unchanged.
2. Review the 17 severity-mismatch unmapped controls and update mapping decisions in small batches.
3. Review the 17 no-candidate unmapped controls by implementation topic and decide whether each needs overlay validation, deployment ownership, true manual evidence, or exception rationale.
4. Reassess the 16 `manual_only` controls for possible partial overlay validation.
5. Add overlay checks only where repository-owned validation evidence is concrete and portable.
6. Synchronize traceability from mapping decisions, regenerate reports, and run STIG metadata guardrails after each batch.
7. Run the containerized validation workflow against the hardened image when overlay behavior changes.
8. Roll back a bad classification by reverting the affected mapping/traceability/report updates and removing any corresponding overlay check.

## Open Questions

- Which PostgreSQL 16 controls should be considered high-priority for overlay automation because they map directly to existing STIG image configuration?
- Should deployment-owned classifications use only the existing responsibility enum, or do we need additional categories for certificates, backup retention, or audit retention?
- Do any existing guardrails need to scan new review notes beyond the current mapping and traceability files?
- Should final evidence include validation JSON summaries only, or also a compact project-authored review report by control topic?
