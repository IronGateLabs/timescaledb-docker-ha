# Legacy STIG Profile Runner

This thin InSpec profile executes the forked Crunchy PostgreSQL STIG validation
profile against the hardened TimescaleDB HA PostgreSQL 16 image. It exists so the
reusable `legacy:V-233xxx` mappings recorded in `stig/postgres16-v1r2-traceability.json`
can actually run and produce per-control results, rather than remaining candidate
(paper) mappings.

## What it does

- Declares a single commit-pinned dependency on the forked profile
  (`IronGateLabs/crunchy-data-postgresql-stig-baseline`) and `include_controls` it.
  The forked profile is referenced, never copied into this repository, and no DISA
  benchmark prose is vendored here.
- Inputs are supplied at run time from `stig/inputs_timescaledb_ha_pg16_example.yml`,
  which maps the forked profile's expected inputs to this image's paths, package
  names, and runtime layout.

## How to run

The repository overlay run is unchanged. To run the legacy profile in addition:

```sh
# 1. Build and start a disposable hardened target (heavy; builds the STIG image)
make build-stig
STIG_PG_PASSWORD=… cicd/start-stig-validation-target

# 2. Run the legacy profile against it
STIG_PG_PASSWORD=… STIG_TARGET_CONTAINER=ts-stig-validation make validate-stig-legacy
```

Results are written to `.build/stig-validation/timescaledb-ha-pg16-legacy.json`.

## Requirements and caveats

- **Network egress is required**: the CINC Auditor/InSpec runner fetches the pinned
  dependency commit at execution time. The repository overlay (`validate-stig-overlay`)
  does not require network and is unaffected.
- **Not authoritative yet**: the forked profile targets PostgreSQL 10–15; many controls
  must be verified against PostgreSQL 16 behavior before a result is treated as authoritative
  coverage. Executed results inform, but do not by themselves promote, a control's
  traceability status. See the `execute-postgres-16-stig-validation` change for the
  per-control verification task.
