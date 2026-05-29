## Purpose

Define repository-owned STIG overlay validation for portable PostgreSQL 16 image and runtime evidence.

## Requirements

### Requirement: Overlay checks validate portable repository evidence
The project SHALL use repository-owned validation overlay checks only when the check can verify concrete, portable evidence from the hardened target image or PostgreSQL runtime.

#### Scenario: Runtime setting is validated
- **WHEN** a control can be evaluated by querying PostgreSQL runtime state or configuration
- **THEN** the overlay check validates the concrete setting without relying on host-specific paths or private environment assumptions

#### Scenario: Filesystem or package evidence is validated
- **WHEN** a control can be evaluated from container filesystem state, installed packages, permissions, or generated configuration files
- **THEN** the overlay check validates that evidence through the existing external validation runner

### Requirement: Overlay checks avoid false compliance
The project MUST NOT add overlay checks that pass only by assuming organization policy, deployment behavior, or human process evidence.

#### Scenario: Control depends on external policy
- **WHEN** a control depends on Kubernetes policy, identity configuration, networking boundaries, secrets, certificates, backup policy, audit retention, or organization process
- **THEN** the control is classified as deployment-owned or manual rather than covered by a placeholder overlay check

#### Scenario: Required evidence is unavailable to the runner
- **WHEN** the validation runner cannot observe the evidence needed for a control
- **THEN** the overlay marks the limitation in mapping metadata instead of asserting pass/fail coverage

### Requirement: Overlay validation results feed traceability
The project SHALL connect overlay checks to mapping and traceability status through stable control references and validation summaries.

#### Scenario: Overlay check replaces unmapped status
- **WHEN** an overlay check provides the primary validation path for a previously unmapped control
- **THEN** the mapping records `replaced_by_overlay`, references the overlay check, and updates automation and validation ownership fields

#### Scenario: Overlay check supplements legacy mapping
- **WHEN** an overlay check supplements reusable legacy validation for a PostgreSQL 16 control
- **THEN** the mapping records both validation references without treating either one as copied benchmark content

### Requirement: Overlay workflow remains reproducible
The project MUST run overlay validation through the existing containerized CINC Auditor or InSpec workflow.

#### Scenario: Overlay behavior changes
- **WHEN** a repository-owned overlay check is added or modified
- **THEN** the documented STIG validation workflow can run the check without requiring local Ruby tooling or audit tooling inside the database image
