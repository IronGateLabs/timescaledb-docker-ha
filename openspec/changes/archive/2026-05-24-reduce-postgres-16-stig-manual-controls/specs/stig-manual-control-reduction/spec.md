## ADDED Requirements

### Requirement: Manual control reduction review
The project SHALL review every PostgreSQL 16 STIG control currently classified as manual, manual-only, or unmapped before changing its final traceability classification.

#### Scenario: Unmapped controls are reviewed
- **WHEN** a PostgreSQL 16 control has mapping status `unmapped`
- **THEN** the review records whether the control is mapped to reusable validation, replaced by overlay validation, deployment-owned, manual-only, or excepted using project-authored metadata

#### Scenario: Manual-only controls are reassessed
- **WHEN** a PostgreSQL 16 control has mapping status `manual_only`
- **THEN** the review records whether repository-owned implementation evidence or overlay validation can partially automate the control before preserving manual-only status

### Requirement: Review prioritization
The project MUST prioritize review work so higher-risk unknowns are resolved before lower-risk or already-reviewed manual controls.

#### Scenario: Severity mismatch candidates exist
- **WHEN** unmapped controls include legacy validation candidates with severity mismatches
- **THEN** those controls are reviewed before unmapped controls with no legacy candidate

#### Scenario: No-candidate controls remain
- **WHEN** unmapped controls have no legacy validation candidate
- **THEN** those controls are grouped by implementation topic and reviewed against repository-owned image, runtime, overlay, documentation, and deployment evidence

### Requirement: Mapping and traceability synchronization
The project SHALL keep detailed control mapping decisions and final traceability status synchronized after each reviewed batch.

#### Scenario: Mapping decisions change
- **WHEN** one or more controls are reclassified in the control mapping
- **THEN** the traceability inventory, mapping report, and candidate review summary are updated to reflect the reviewed counts

#### Scenario: Guardrails run after review
- **WHEN** a batch of mapping or traceability updates is completed
- **THEN** repository STIG metadata checks pass without local paths, secrets, or copied benchmark prose

### Requirement: Implementation claim evidence
The project MUST link implementation or validation claims to concrete repository-owned, deployment-owned, or manual evidence.

#### Scenario: Control is marked image-enforced or overlay-validated
- **WHEN** a control is classified as implemented or validated by this repository
- **THEN** the mapping references the relevant repository file, configuration behavior, overlay check, or validation output

#### Scenario: Control remains manual
- **WHEN** a reviewed control remains manual
- **THEN** the mapping records original project rationale explaining why repository automation is not currently defensible
