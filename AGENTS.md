# Repository Guidelines

## Project Structure & Module Organization

This repository builds the `timescale/timescaledb-ha` Docker image for Kubernetes. The main build definition is `Dockerfile`, with orchestration in `Makefile`. Runtime entrypoints live at the root (`docker-entrypoint.sh`, `timescaledb_entrypoint.sh`, `pgbackrest_entrypoint.sh`). Build helpers are in `build_scripts/`, image validation and CI helpers are in `cicd/`, installed SQL and operational scripts are in `scripts/`, and architecture-specific package sources are in `sources/`. Update extension releases in `build_scripts/versions.yaml`.

## Build, Test, and Development Commands

- `make help`: list supported Make targets and short descriptions.
- `make` or `make fast`: build a faster developer image with a reduced extension set.
- `make build`: build the local release image using the default PostgreSQL major version.
- `PG_MAJOR=17 PLATFORM=amd64 make build`: build for a specific PostgreSQL major and architecture.
- `make build-oss`: build an OSS-only image.
- `./cicd/lint-sh "SC2148,SC2034,SC1091,SC2153,SC1090,SC2097,SC2098,SC2043"`: run the same ShellCheck exclusions used by CI.
- `make check`: run containerized install checks; requires Docker and expected image tags.

## Coding Style & Naming Conventions

Most code is Bash, SQL, YAML, and small Python utilities. Keep shell scripts Bash-compatible, use `set -e` or `set -e -o pipefail` where appropriate, quote variable expansions, and prefer helpers in `build_scripts/shared.sh` and `cicd/shared.sh`. Shell indentation commonly uses tabs inside functions; Make recipes must use tabs. Use lowercase, hyphenated filenames for executable scripts unless matching an upstream name; use uppercase Make variables such as `PG_MAJOR`.

## Testing Guidelines

CI validates shell scripts with ShellCheck and images through Docker-based smoke/install checks. Add or update checks in `cicd/install_checks` and `cicd/shared.sh` when changing installed packages, extensions, or expected files. For entrypoint or image-content changes, build locally and run `make check` or a container smoke test before opening a PR.

## Commit & Pull Request Guidelines

Recent history uses short imperative summaries, often with prefixes such as `feat:` and `chore:`; examples include `feat: introduce timescaledb v2.27.1` and `chore: add tsdb 2.27.0 to versions`. Keep commits focused on one release, dependency bump, or behavior change. PRs should describe image impact, list changed versions or packages, link issues, and include build/check commands or CI verification.

## Security & Configuration Tips

Do not commit registry credentials, GitHub tokens, or local Docker metadata. Keep GitHub Actions pinned by SHA when editing workflows. Avoid changing default image tags, registry names, or release labeling behavior unless the release process is part of the change.
