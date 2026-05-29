# PostgreSQL 16 Manual Control Reduction Review

This review artifact is generated from committed project metadata. It uses control identifiers and project-authored review prompts only; do not add benchmark prose, local source paths, or secrets.

## Current Counts

### Mapping Status

| Status | Count |
| --- | --- |
| mapped | 60 |
| manual_only | 2 |
| unmapped | 0 |
| replaced_by_overlay | 18 |
| deployment_owned | 31 |
| exception | 0 |

### Automation Status

| Status | Count |
| --- | --- |
| automated | 0 |
| partially_automated | 78 |
| manual | 2 |
| not_yet_assessed | 0 |
| deployment_owned | 31 |
| exception | 0 |

### Traceability Status

| Status | Count |
| --- | --- |
| image_enforced | 18 |
| deployment_owned | 31 |
| validation_only | 60 |
| manual | 2 |
| exception | 0 |
| not_yet_reviewed | 0 |

## Severity-Mismatch Unmapped Controls

| Control ID | STIG ID | Severity | Candidate IDs | Candidate SRG IDs | Review Prompt |
| --- | --- | --- | --- | --- | --- |

## Reviewed Severity-Mismatch Decisions

| Control ID | STIG ID | Mapping Status | Automation Status | Container Validation | Deployment Responsibility | Project Rationale |
| --- | --- | --- | --- | --- | --- | --- |
| V-261858 | CD16-00-000200 | mapped | partially_automated | partial | undetermined | Reviewed severity-mismatch candidate; reusable audit configuration and log validation logic remains applicable to PostgreSQL 16 with repository inputs. Treat as validation-only until implementation ownership is separately confirmed. |
| V-261859 | CD16-00-000300 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; security update timing depends on image rebuild, release, and deployment patch policy rather than a stable container runtime assertion. |
| V-261861 | CD16-00-000500 | deployment_owned | deployment_owned | partial | identity_and_access | Reviewed severity-mismatch candidate; authentication integration depends on deployment identity architecture, with only partial pg_hba method validation possible from the container. |
| V-261864 | CD16-00-000800 | mapped | partially_automated | partial | identity_and_access | Reviewed severity-mismatch candidate; reusable pg_hba authentication-method validation applies to PostgreSQL 16, while final approved method selection remains deployment-owned. |
| V-261865 | CD16-00-000900 | deployment_owned | deployment_owned | not_supported | identity_and_access | Reclassified to deployment-owned after executed validation: host-based authentication topology (pg_hba local and replication rules) is rendered by Patroni and provided at deployment, not by the image. |
| V-261882 | CD16-00-002700 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; real-time audit failure alerting depends on deployment logging and monitoring integration outside the image boundary. |
| V-261883 | CD16-00-002800 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; audit storage exhaustion behavior and retention policy depend on deployment log management outside the image boundary. |
| V-261886 | CD16-00-003200 | deployment_owned | deployment_owned | not_supported | identity_and_access | Reviewed severity-mismatch candidate; authorization and tracking of software installation account access is an operational access-control responsibility outside this image. |
| V-261894 | CD16-00-004100 | mapped | partially_automated | partial | undetermined | Reviewed severity-mismatch candidate; reusable audit logging validation for configuration and access-restriction events remains applicable to PostgreSQL 16 with repository log inputs. |
| V-261896 | CD16-00-004400 | deployment_owned | deployment_owned | not_supported | organization_policy | Reassessed manual-only control; FIPS-validated cryptographic module use depends on base platform and runtime cryptographic configuration outside the database image. |
| V-261901 | CD16-00-005200 | mapped | partially_automated | partial | undetermined | Reviewed severity-mismatch candidate; reusable pgaudit event validation remains applicable to PostgreSQL 16 with repository audit log inputs. |
| V-261926 | CD16-00-008000 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; FIPS mode for cryptographic hash validation depends on host and base platform configuration outside the database image. |
| V-261927 | CD16-00-008100 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; classified-data cryptography requirements depend on deployment classification, TLS policy, and platform cryptographic configuration outside the image. |
| V-261939 | CD16-00-009500 | mapped | partially_automated | partial | identity_and_access | Reviewed severity-mismatch candidate; reusable password encryption and role password validation applies to PostgreSQL 16, and the STIG image fragment sets SCRAM password encryption. |
| V-261946 | CD16-00-010200 | deployment_owned | deployment_owned | partial | secrets | Reviewed severity-mismatch candidate; TLS key material placement and permissions depend on deployment-provided TLS assets, with only partial validation possible when those inputs are supplied. |
| V-261961 | CD16-00-011700 | deployment_owned | deployment_owned | not_supported | organization_policy | Reassessed manual-only control; concurrent session correlation requires deployment monitoring and user activity policy beyond static image validation. |
| V-261966 | CD16-00-012300 | deployment_owned | deployment_owned | not_supported | organization_policy | Reviewed severity-mismatch candidate; FIPS-validated cryptographic operation requirements depend on base platform and OpenSSL FIPS configuration outside the database image. |

## No-Candidate Unmapped Controls

| Control ID | STIG ID | Topic | Severity | CCI Refs | Review Prompt |
| --- | --- | --- | --- | --- | --- |

## Manual-Only Controls

| Control ID | STIG ID | Severity | Legacy IDs | Container Validation | Review Prompt |
| --- | --- | --- | --- | --- | --- |
| V-261934 | CD16-00-009000 | medium | none | not_supported | Reassess for concrete overlay, deployment, or manual evidence. |
| V-261954 | CD16-00-011000 | medium | none | not_supported | Reassess for concrete overlay, deployment, or manual evidence. |

