## ADDED Requirements

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
