## Context

The current repository builds general-purpose TimescaleDB HA images through `Dockerfile` and `Makefile`, with runtime behavior driven by root entrypoint scripts and helper scripts under `scripts/`, `build_scripts/`, and `cicd/`. The target outcome is a PostgreSQL 16 STIG-hardened image equivalent in installed database scope to the existing `pg16-all` image, while preserving the current default image behavior.

The available STIG source package must be treated as reference material only. The repository may record control identifiers, implementation status, local rationale, validation commands, and exception status, but must not copy DISA prose or benchmark content into project files. A forked PostgreSQL STIG validation profile exists, but its current metadata and examples indicate coverage through earlier PostgreSQL releases, so PostgreSQL 16 compatibility must be verified before relying on it.

## Goals / Non-Goals

**Goals:**

- Add an opt-in PostgreSQL 16 STIG hardening path for a `pg16-all`-equivalent TimescaleDB HA image.
- Keep a machine-readable control traceability file that maps control IDs to image implementation, validation, deployment responsibility, and exception status.
- Provide a repeatable validation workflow using CINC Auditor/InSpec from a runner or container, without requiring a developer-managed Ruby installation.
- Identify and maintain PostgreSQL 16 compatibility changes in the forked validation profile, with upstream contribution as a later option.
- Separate image-enforced settings from deployment-time controls that depend on Kubernetes, users, networking, secrets, or organization policy.

**Non-Goals:**

- Do not replace the existing default TimescaleDB HA image behavior.
- Do not claim full STIG compliance solely from a Docker build.
- Do not vendor or redistribute DISA benchmark prose.
- Do not make the production database image depend on Ruby, CINC Auditor, or InSpec.

## Decisions

1. Use an opt-in STIG image mode instead of changing the default image.

   The Makefile should grow a dedicated build path, such as a `build-stig` target or `STIG_ENABLED=true` build argument, that produces a distinct tag suffix. This keeps existing consumers stable and allows hardening choices to be reviewed independently. Alternative considered: harden all `pg16-all` builds by default. That creates compatibility risk for existing deployments and makes rollback harder.

2. Store traceability as project-authored metadata, not copied STIG content.

   Add a concise YAML or CSV file under a neutral repository path such as `stig/` or `cicd/stig/`. Each row should use fields like `control_id`, `status`, `implemented_by`, `validated_by`, `deployment_responsibility`, and `notes`. Notes must be original project rationale, not STIG text. Alternative considered: checking in converted benchmark exports. That would create licensing and maintenance risk.

3. Implement hardening through layered PostgreSQL configuration and startup checks.

   STIG-specific configuration should be isolated in explicit fragments or scripts, then wired into entrypoint behavior only when STIG mode is selected. Build-time changes should cover packages, file layout, permissions, and bundled extensions. Runtime changes should cover PostgreSQL settings, audit/logging setup, and generated configuration that depends on environment variables. Alternative considered: baking a complete initialized data directory into the image. That conflicts with normal PostgreSQL container initialization and Kubernetes volume behavior.

4. Validate with a separate runner workflow.

   The image should expose enough configuration and test fixtures for CINC Auditor/InSpec to validate it from outside the database container. The validation profile work belongs in the forked baseline repository or an overlay, while this repository owns image build, sample inputs, and CI invocation. Prefer containerized or pinned CINC Auditor execution. Local Ruby may be useful for profile development but must not be a prerequisite for repository builds. Alternative considered: installing Ruby and InSpec into the database image. That increases attack surface and couples audit tooling to runtime.

5. Treat PostgreSQL 16 support as a compatibility audit, not a string replacement.

   The forked profile must be reviewed for PostgreSQL 16 paths, packages, extension locations, SQL behavior, role assumptions, authentication methods, logging settings, and deprecated controls. Controls that cannot be validated in a container or require organization-specific policy should be marked as manual or deployment responsibility in traceability. Alternative considered: simply changing profile metadata from PostgreSQL 15 to 16. That may produce false confidence and unstable results.

6. Gate classification and hardening behind explicit PostgreSQL 16 control mapping.

   PostgreSQL 16 control identifiers must be mapped before controls are marked automated, manual, deployment-owned, or excepted. The mapping should start with all controls unmapped, then record reviewed links to reusable legacy controls, overlay checks, deployment responsibilities, manual review, or exceptions. Alternative considered: classify directly in traceability while reviewing. That makes it too easy to mix unreviewed assumptions with implementation status.

7. Defer upstream validation-profile pull requests until the image work is verified.

   The forked PostgreSQL STIG validation profile can receive portable PostgreSQL 16 inputs or compatibility updates, but upstream PRs should wait until this repository's default-build check and final traceability pass are complete. This keeps upstream changes focused on reusable profile behavior and avoids mixing TimescaleDB HA image-specific implementation details into the baseline profile.

## Risks / Trade-offs

- PostgreSQL STIG controls may require host, Kubernetes, IAM, or organization policy context that an image cannot enforce -> classify each control by image, deployment, validation-only, manual, or exception responsibility.
- STIG hardening may conflict with TimescaleDB HA, Patroni, pgBackRest, or Kubernetes operator expectations -> test against normal initialization, replica/bootstrap behavior, and backup/restore scripts before treating the mode as usable.
- The validation profile may lag PostgreSQL 16 or contain Crunchy-specific assumptions -> maintain compatibility changes in a fork or overlay, document any assumptions, and defer upstream PRs until the local image and traceability work are verified.
- Authentication controls may not match common container defaults -> keep secrets, users, and network trust decisions deployment-owned unless the image can enforce them without breaking orchestration.
- Audit/logging settings can increase disk and performance overhead -> document operational impact and provide explicit enablement rather than silently changing default behavior.

## Migration Plan

1. Build a traceability inventory from allowed control identifiers and project-authored status fields.
2. Generate an initial PostgreSQL 16 control mapping with all controls unmapped.
3. Review the forked validation profile for PostgreSQL 16 assumptions and create a minimal PG16 input file for the TimescaleDB HA image.
4. Map controls to reusable validation logic, overlay checks, manual review, deployment ownership, or exceptions.
5. Add an opt-in STIG build/runtime mode and generate a local `pg16-all`-equivalent image tag for validation.
6. Run containerized CINC Auditor/InSpec validation against the image and update traceability with pass, fail, manual, or exception status.
7. Add CI checks once the local workflow is stable.
8. Roll back by disabling the STIG build/runtime mode or using the existing non-STIG image target.

## Open Questions

- Should the hardened image be a separate tag only, or should it also support runtime enablement through an environment variable?
- Which controls must be considered deployment-owned for the intended Kubernetes environment?
- Should validation profile changes live as a fork branch, an overlay profile, or a proposed upstream pull request? Current decision: use this repository's overlay for image-specific checks, keep any fork changes portable, and hold upstream PRs until final verification is complete.
- What is the acceptable baseline for authentication methods in development validation versus production deployment?
