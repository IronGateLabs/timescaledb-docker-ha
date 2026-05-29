## ADDED Requirements

### Requirement: Mapped legacy validation executes against the hardened image
When a control's validation references a reusable legacy profile control, the validation workflow SHALL execute that profile against the hardened image using portable PostgreSQL 16 inputs before the control counts as validated. The legacy profile SHALL be referenced as a portable dependency rather than copied into the repository, and inputs SHALL contain no host-specific paths or secrets.

#### Scenario: Legacy profile is included in a run
- **WHEN** the STIG validation workflow runs against the hardened image
- **THEN** it executes the referenced legacy profile controls with TimescaleDB HA PostgreSQL 16 inputs and records per-control results

#### Scenario: Inputs remain portable
- **WHEN** a validation input file is added or changed
- **THEN** it uses placeholder or image-relative values only and contains no local filesystem paths, hostnames, or secrets

### Requirement: Validation runs in CI against a built hardened image
Continuous integration SHALL build or launch the hardened image and run the STIG validation, publishing per-control pass, fail, manual, deployment-owned, and exception results that can be mapped back to traceability.

#### Scenario: CI validation job runs on change
- **WHEN** STIG image configuration, overlay controls, or validation inputs change
- **THEN** a CI job builds or launches the hardened image, runs validation, and publishes a result artifact mappable to control identifiers
