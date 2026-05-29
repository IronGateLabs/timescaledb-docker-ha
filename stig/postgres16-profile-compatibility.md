# PostgreSQL 16 Validation Profile Compatibility

This note tracks compatibility signals for adapting the forked PostgreSQL STIG validation profile to the TimescaleDB HA PostgreSQL 16 image. It records repository metadata and identifier-level findings only; it does not copy benchmark prose.

## Summary

- PostgreSQL 16 traceability inventory count: 111 controls.
- PostgreSQL 16 source baseline: Crunchy Data Postgres 16 STIG V1R2, release 2, benchmark date 01 Apr 2026.
- Forked validation profile control file count: 113 controls.
- Forked validation profile baseline: Crunchy Data PostgreSQL STIG V3R1, profile version 3.1.0, benchmark date 24 Jul 2024.
- Direct control ID overlap: 0 controls.
- PostgreSQL 16 inventory IDs use the `V-261857` through `V-283674` range.
- The forked validation profile currently uses the older `V-233*` range plus `V-265871`.

## Compatibility Gaps

- The forked profile metadata and examples do not currently advertise PostgreSQL 16 support.
- The forked profile baseline version does not match the PostgreSQL 16 source baseline, so it must be treated as a legacy candidate profile rather than authoritative PostgreSQL 16 coverage.
- The forked profile examples include PostgreSQL 12 and PostgreSQL 14 input files, but no PostgreSQL 16 TimescaleDB HA input example.
- Several default paths in the forked profile metadata are PostgreSQL 12-style paths and do not match this image's `/home/postgres/pgdata/data`, `/home/postgres/pg_log`, and `/usr/lib/postgresql/16` layout.
- The forked profile's example approved package names include platform-specific package naming that does not match this Ubuntu-based image.
- Existing control filenames and tags cannot be treated as PostgreSQL 16 coverage without mapping old identifiers to PostgreSQL 16 identifiers or replacing controls with PostgreSQL 16-specific controls.

## Required Follow-up

- Build an identifier mapping between PostgreSQL 16 controls and any reusable forked profile controls.
- Decide whether PostgreSQL 16 work should be maintained as changes in the fork, a separate overlay profile, or both.
- Review control logic for PostgreSQL 16 paths, installed packages, extension locations, SQL behavior, authentication assumptions, log locations, and controls that require deployment context.
- Keep validation-profile edits separate from this image repository unless they are runner inputs, documented commands, or repository-owned validation glue.
