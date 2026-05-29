# stig-control-traceability Specification

## Purpose
TBD - created by archiving change add-postgres-16-stig-hardening. Update Purpose after archive.
## Requirements
### Requirement: Control traceability inventory
The project SHALL maintain a machine-readable PostgreSQL 16 STIG traceability inventory using project-authored metadata and control identifiers only.

#### Scenario: Inventory records implementation status
- **WHEN** a PostgreSQL 16 STIG control is evaluated for the image
- **THEN** the inventory records its control identifier, status, implementation owner, validation owner, and notes without copying benchmark prose

#### Scenario: Inventory separates image and deployment responsibilities
- **WHEN** a control depends on deployment policy, Kubernetes configuration, user management, network boundaries, or secrets
- **THEN** the inventory marks the control as deployment-owned, manual, or exception instead of image-enforced

### Requirement: Traceability drives implementation scope
The project MUST use the traceability inventory to determine which hardening work belongs in this repository and which work belongs in deployment documentation or the validation profile.

#### Scenario: Image-enforceable control is identified
- **WHEN** a control can be satisfied by Docker build content, file permissions, bundled scripts, or PostgreSQL runtime configuration
- **THEN** the inventory links the control to the repository file or validation check expected to implement it

#### Scenario: Non-image control is identified
- **WHEN** a control cannot be satisfied by the container image alone
- **THEN** the inventory records the external dependency or exception rationale needed for review

### Requirement: PostgreSQL 16 control mapping
The project SHALL maintain a PostgreSQL 16 control mapping that links each traceability control to reusable validation controls, overlay checks, manual review, deployment responsibility, or exception status before final classification.

#### Scenario: Initial mapping is generated
- **WHEN** the PostgreSQL 16 traceability inventory exists
- **THEN** the mapping records every PostgreSQL 16 control and starts unmapped controls as not yet assessed

#### Scenario: Mapping prevents unsupported classification
- **WHEN** a control has not been reviewed against legacy validation controls, overlay checks, or deployment context
- **THEN** the control remains unmapped and not yet assessed rather than being marked automated, manual, deployment-owned, or excepted

#### Scenario: Reviewed mapping is recorded
- **WHEN** a control is reviewed and a validation or implementation responsibility is known
- **THEN** the mapping records the reviewed legacy control, overlay check, manual review, deployment responsibility, or exception reference using project-authored metadata only

