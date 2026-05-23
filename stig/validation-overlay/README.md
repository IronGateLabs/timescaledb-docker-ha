# TimescaleDB HA PostgreSQL 16 STIG Overlay

This overlay is repository-owned validation glue for the PostgreSQL 16 TimescaleDB HA image. It does not replace a PostgreSQL 16 STIG validation profile and does not include copied STIG benchmark prose.

Use it to validate image-specific assumptions before adapting or upstreaming changes to the forked PostgreSQL STIG baseline:

- PostgreSQL 16 paths match this image layout.
- The runner connects to the expected database endpoint.
- Approved package and extension inputs use Ubuntu/TimescaleDB HA names rather than older package naming.
- Audit extension paths and log paths are configured for this image.

Example runner input:

```console
stig/inputs_timescaledb_ha_pg16_example.yml
```

Run the overlay from a containerized CINC Auditor/InSpec runner:

```console
export STIG_PG_PASSWORD='replace-with-local-test-password'
make start-stig-validation-target
export STIG_TARGET_CONTAINER=ts-stig-validation
make validate-stig-overlay
make summarize-stig-validation
docker rm --force ts-stig-validation
```

The target container is validated through Docker transport, so file checks and `psql` commands execute inside the database container while the audit tooling stays outside the image. The generated JSON report is written to `.build/stig-validation/timescaledb-ha-pg16-overlay.json`.

This overlay is intentionally small. PostgreSQL 16 STIG control implementation remains tracked in `stig/postgres16-v1r2-traceability.json`.
