# stig-hardened-image-configuration Specification

## Purpose
TBD - created by archiving change add-postgres-16-stig-hardening. Update Purpose after archive.
## Requirements
### Requirement: Opt-in STIG image mode
The build system SHALL provide an explicit opt-in path for producing a PostgreSQL 16 STIG-hardened `pg16-all`-equivalent TimescaleDB HA image without changing the default non-STIG image behavior.

#### Scenario: Default build remains unchanged
- **WHEN** a user runs the existing non-STIG build targets
- **THEN** the image is built with the same default behavior and tagging conventions as before this change

#### Scenario: STIG build is selected
- **WHEN** a user selects the STIG build path
- **THEN** the build produces a distinct image variant or tag that can be validated independently from the default image

### Requirement: STIG configuration isolation
The image SHALL isolate STIG-specific PostgreSQL configuration, scripts, and checks from general-purpose runtime logic.

#### Scenario: STIG mode applies hardening
- **WHEN** the hardened image or runtime mode initializes PostgreSQL
- **THEN** STIG-specific configuration is applied through explicit configuration fragments or scripts

#### Scenario: Non-STIG mode bypasses hardening
- **WHEN** STIG mode is not selected
- **THEN** STIG-specific configuration fragments and startup checks do not alter PostgreSQL runtime behavior

### Requirement: TimescaleDB HA compatibility
The hardened image MUST preserve required TimescaleDB HA, Patroni, pgBackRest, extension, and PostgreSQL 16 behavior for the `pg16-all`-equivalent scope.

#### Scenario: Hardened image starts successfully
- **WHEN** the hardened image is launched with the documented validation inputs
- **THEN** PostgreSQL starts successfully with TimescaleDB and expected bundled extensions available

#### Scenario: HA behavior is not silently broken
- **WHEN** hardening changes affect authentication, logging, file permissions, backup, restore, or replica setup
- **THEN** the implementation includes validation or documentation covering the affected HA behavior

### Requirement: Image-enforceable controls are enforced by the image
The hardened image SHALL apply the configuration for transport security, host-based authentication methods, role-privilege baselines, and FIPS-mode signaling that the image can defensibly own, rather than deferring these to deployment when the image can set them. Controls the image cannot own SHALL remain `deployment_owned` with project-authored rationale.

#### Scenario: Transport and authentication are configured
- **WHEN** the hardened image initializes PostgreSQL
- **THEN** it applies the TLS, host-based authentication, role-privilege, and FIPS-signaling settings the image can own, and an overlay check observes each one

#### Scenario: Control cannot be owned by the image
- **WHEN** a control depends on certificates, secrets, networking, or organization policy supplied at deployment
- **THEN** it remains `deployment_owned` with rationale rather than being claimed as image-enforced

### Requirement: A distinct validated hardened artifact is published
The project SHALL define and document the default-hardening posture: either a clearly built and validated hardened image artifact (for example a dedicated STIG-hardened tag) or explicit documentation that the default published image is not hardened.

#### Scenario: Hardened artifact is identified
- **WHEN** a consumer wants the STIG-hardened TimescaleDB HA image
- **THEN** the documentation identifies the specific built, validated artifact and how it differs from the default image

