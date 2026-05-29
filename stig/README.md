# STIG Traceability

This directory contains project-authored traceability metadata for PostgreSQL 16 STIG hardening work. It may include control identifiers, rule identifiers, severity, CCI references, implementation status, validation status, and local rationale.

Do not copy benchmark prose into this repository. Avoid titles, descriptions, discussion text, check text, fix text, or any content copied from the source STIG package.

## Build Scope

The STIG image path is opt-in. `make build-stig` sets `PG_MAJOR=16`, includes the same PostgreSQL major-version scope as a `pg16-all` image, enables `STIG_ENABLED=true`, and tags the local image with the `pg16-all-stig` suffix. Existing non-STIG build targets remain unchanged.

The image-owned hardening is limited to files and settings the container can enforce directly: PostgreSQL configuration fragments, audit/logging defaults, preload libraries, and file permissions created during initialization. Kubernetes policy, network access, users beyond the local test role, secrets, certificate issuance, backup policy, and organization-specific audit retention remain deployment-owned and must be tracked as such in traceability.

Generate the initial inventory from a local XCCDF file:

```console
scripts/stig/generate_traceability.py path/to/source-xccdf.xml stig/postgres16-v1r2-traceability.json
```

Validate the committed metadata:

```console
cicd/check-stig-traceability
cicd/check-stig-mapping
```

Build the opt-in PostgreSQL 16 STIG image variant:

```console
make build-stig
```

On arm64 development hosts, build a native validation image to avoid emulated container behavior:

```console
PLATFORM=arm64 make build-stig
```

Start a disposable local validation target and run the repository-owned overlay with a containerized CINC Auditor/InSpec runner:

```console
export STIG_PG_PASSWORD='replace-with-local-test-password'
make start-stig-validation-target
export STIG_TARGET_CONTAINER=ts-stig-validation
make validate-stig-overlay
make summarize-stig-validation
docker rm --force ts-stig-validation
```

By default, the validation target lets Docker select the platform for `STIG_IMAGE`. Set `STIG_PLATFORM=linux/amd64` or `STIG_PLATFORM=linux/arm64` only when a specific image platform must be forced.
The disposable target stays alive for 3600 seconds by default; set `STIG_TARGET_SLEEP` if a longer validation/debugging window is needed.

The runner uses Docker transport, mounts the repository read-only, writes JSON output under `.build/stig-validation/`, and does not require Ruby on the host. Override `CINC_AUDITOR_IMAGE`, `STIG_IMAGE`, `STIG_INPUTS`, or `STIG_PROFILE` to test a pinned runner image, a different local tag, or a forked profile path that has first been made portable.

Run repository guardrails:

```console
cicd/check-stig-workflow
```

Use `stig/upstream-profile-contribution.md` before proposing forked validation-profile changes upstream.

Status values:

- `not_yet_reviewed`: control has not been classified.
- `image_enforced`: this image implements the control directly.
- `deployment_owned`: the deployment environment must implement the control.
- `validation_only`: the control is validated here but implemented elsewhere.
- `manual`: the control needs manual review.
- `exception`: the control has a documented exception rationale.

Generate a first-pass control mapping from the traceability inventory:

```console
scripts/stig/generate_control_mapping.py \
  stig/postgres16-v1r2-traceability.json \
  stig/postgres16-control-mapping.json \
  --legacy-controls-dir path/to/legacy-profile/controls
```

The mapping file starts controls as `unmapped` until a reviewer links them to reusable validation controls, overlay checks, manual review, deployment responsibility, or an exception. Candidate legacy controls are only review hints; they are not confirmed mappings.
