# Execute the forked Crunchy PostgreSQL STIG validation profile against the
# hardened TimescaleDB HA PostgreSQL 16 target. The profile is pinned by commit
# in inspec.yml and referenced as a dependency rather than copied into this
# repository.
#
# This makes the reusable legacy controls run and produce per-control results,
# converting the candidate `legacy:V-233xxx` traceability mappings into executed
# evidence. Per-control PostgreSQL 16 behavior MUST be verified before any result
# is treated as authoritative coverage; until then these results inform, but do
# not by themselves promote, a control's traceability status.
include_controls 'crunchy-data-postgresql-stig-baseline'
