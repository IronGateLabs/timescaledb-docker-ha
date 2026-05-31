## ADDED Requirements

### Requirement: Reproducible validation runner
The project SHALL document and automate PostgreSQL 16 STIG validation through a reproducible CINC Auditor or InSpec runner workflow that does not require Ruby tooling inside the database image.

#### Scenario: Validation runs outside the database image
- **WHEN** a user validates the hardened image
- **THEN** the audit tooling runs from a separate runner environment or container and connects to the target database using documented inputs

#### Scenario: Local Ruby is unavailable or unsuitable
- **WHEN** a developer does not have a suitable local Ruby environment
- **THEN** the documented validation workflow still provides a containerized or pinned runner path

### Requirement: PostgreSQL 16 profile compatibility review
The project MUST verify that the forked PostgreSQL STIG validation profile supports PostgreSQL 16 before treating results as authoritative.

#### Scenario: Profile metadata or inputs lag PostgreSQL 16
- **WHEN** profile metadata, examples, inputs, paths, package names, or SQL assumptions reference only earlier PostgreSQL versions
- **THEN** the compatibility gap is tracked and resolved in the fork, an overlay, or documented as a limitation

#### Scenario: Control cannot be automated in container validation
- **WHEN** a control requires host, organization, or deployment context not available to the validation runner
- **THEN** the validation workflow records the control as manual, deployment-owned, or excepted in traceability

### Requirement: Validation artifacts
The project SHALL produce validation inputs and results that can be reviewed without exposing secrets or local machine paths.

#### Scenario: Validation inputs are committed
- **WHEN** sample validation inputs are added to the repository
- **THEN** they contain portable placeholders and repository-relative examples rather than personal paths, passwords, or host-specific values

#### Scenario: Validation results are generated
- **WHEN** validation is run locally or in CI
- **THEN** results identify pass, fail, skipped, manual, and exception outcomes in a form that can update the traceability inventory
