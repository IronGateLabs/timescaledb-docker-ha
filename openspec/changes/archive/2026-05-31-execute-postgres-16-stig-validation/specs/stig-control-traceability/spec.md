## ADDED Requirements

### Requirement: Status reflects executed validation
A control SHALL be classified `validation_only` only when its referenced validation has been executed against the hardened image or runtime. A control whose only validation reference is an unexecuted reusable legacy profile control SHALL be recorded as candidate-mapped rather than as validated coverage.

#### Scenario: Legacy mapping is not executed
- **WHEN** a control's validation reference points only to legacy profile controls that the validation workflow does not run against this image
- **THEN** the control is recorded as candidate-mapped rather than `validation_only`, and the gap is visible in mapping metadata and validation summaries

#### Scenario: Validation is executed against the image
- **WHEN** the referenced validation runs against the hardened image and produces a pass or fail result
- **THEN** the control records the executed validation reference and may be classified `validation_only`

### Requirement: Enforcement claims match image configuration
A control SHALL be classified `image_enforced` only when the hardened image applies a concrete setting that a validation check can observe. Controls that pass only from PostgreSQL default state SHALL NOT be classified `image_enforced`.

#### Scenario: Image applies no enforcing configuration
- **WHEN** a control is marked `image_enforced` but the hardened image initialization sets no corresponding configuration
- **THEN** the control is reclassified to `deployment_owned`, `validation_only`, or `manual` according to where the requirement is actually owned

#### Scenario: Image enforcement is observable
- **WHEN** the hardened image applies a concrete setting for a control
- **THEN** an overlay check observes that setting and the control retains `image_enforced` status

### Requirement: Guardrails reject paper coverage
The traceability guardrails SHALL reject legacy-only validation references presented as executed coverage.

#### Scenario: Guardrail evaluates a validated control
- **WHEN** `cicd/check-stig-traceability` evaluates a control classified as validated
- **THEN** the check fails if the control's only validation evidence is an unexecuted legacy reference
