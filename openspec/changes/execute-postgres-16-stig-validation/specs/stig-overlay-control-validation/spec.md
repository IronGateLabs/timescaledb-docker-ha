## ADDED Requirements

### Requirement: Asserting overlay controls enforce and map to STIG identifiers
An overlay control that asserts a STIG requirement SHALL carry a non-zero InSpec impact and reference the corresponding PostgreSQL 16 STIG control identifier, so that a failing check fails the validation run and maps back to traceability. Informational preflight checks MAY remain at `impact 0.0` but SHALL be labeled informational and SHALL NOT be counted as control coverage.

#### Scenario: Overlay control asserts a requirement
- **WHEN** an overlay control provides the validation path for a PostgreSQL 16 STIG control
- **THEN** the control declares a non-zero impact and tags the V-26xxxx control identifier so a failure fails the run and updates traceability

#### Scenario: Overlay check is informational
- **WHEN** an overlay control performs an input-shape or preflight check rather than asserting a STIG requirement
- **THEN** it is labeled informational, may remain `impact 0.0`, and is excluded from control coverage counts
