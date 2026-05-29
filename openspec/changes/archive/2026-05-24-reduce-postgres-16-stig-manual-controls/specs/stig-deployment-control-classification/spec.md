## ADDED Requirements

### Requirement: Deployment-owned control classification
The project SHALL classify controls as deployment-owned when the Docker image cannot enforce the control and implementation depends on the runtime deployment environment.

#### Scenario: Kubernetes or operator control is identified
- **WHEN** a control depends on Kubernetes manifests, admission policy, operator behavior, pod security, service exposure, or runtime scheduling
- **THEN** the mapping records deployment ownership with the closest supported deployment responsibility category

#### Scenario: Identity, networking, or secrets control is identified
- **WHEN** a control depends on external identity, user provisioning, network segmentation, TLS certificate issuance, secret storage, or credential rotation
- **THEN** the mapping records deployment ownership instead of image enforcement

### Requirement: Deployment-owned status includes project-authored rationale
The project MUST record why each deployment-owned control is outside the image boundary without copying benchmark prose or encoding private environment details.

#### Scenario: Control moves from manual to deployment-owned
- **WHEN** review determines that a manual control is deployment-owned
- **THEN** traceability records deployment ownership, validation ownership, deployment responsibility, and original project rationale

#### Scenario: Existing responsibility enums are insufficient
- **WHEN** a deployment-owned control does not fit the existing responsibility categories
- **THEN** the project updates the schema and guardrails before using a new category

### Requirement: Deployment-owned controls remain reviewable
The project SHALL keep deployment-owned controls visible in reports and validation summaries so external implementation work is not hidden.

#### Scenario: Report counts are updated
- **WHEN** controls are reclassified as deployment-owned
- **THEN** the control mapping report separates deployment-owned counts from manual, unmapped, validation-only, and image-enforced counts

#### Scenario: Validation workflow encounters deployment-owned control
- **WHEN** validation summarizes controls that require deployment evidence
- **THEN** the result identifies them separately from failed or unreviewed controls

### Requirement: Image boundary is preserved
The project MUST preserve the current opt-in STIG image behavior and avoid changing non-STIG defaults while classifying deployment-owned controls.

#### Scenario: Deployment guidance changes
- **WHEN** documentation or metadata identifies deployment-owned responsibilities
- **THEN** default non-STIG image build and runtime behavior remain unchanged
