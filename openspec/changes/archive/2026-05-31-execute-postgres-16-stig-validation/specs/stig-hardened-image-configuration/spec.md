## ADDED Requirements

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
