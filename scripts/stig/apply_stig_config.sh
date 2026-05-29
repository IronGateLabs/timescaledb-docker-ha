#!/usr/bin/env bash

set -euo pipefail

if [ "${STIG_ENABLED:-false}" != "true" ]; then
	echo "STIG configuration not enabled; skipping"
	exit 0
fi

: "${PGDATA:?PGDATA is required}"
: "${PGLOG:=/home/postgres/pg_log}"

postgresql_conf="${PGDATA}/postgresql.conf"
stig_conf="${PGDATA}/stig-postgresql.conf"

install -d -m 0700 "${PGDATA}" "${PGLOG}"

if ! grep -Eq "^[[:space:]]*include_if_exists[[:space:]]*=[[:space:]]*'stig-postgresql.conf'" "${postgresql_conf}"; then
	printf "\ninclude_if_exists = 'stig-postgresql.conf'\n" >>"${postgresql_conf}"
fi

cat >"${stig_conf}" <<'EOF'
# Project-owned STIG hardening fragment for the opt-in STIG image mode.
password_encryption = 'scram-sha-256'
logging_collector = 'on'
log_destination = 'stderr,csvlog'
log_directory = '/home/postgres/pg_log'
log_filename = 'postgresql-%a.log'
log_file_mode = '0600'
log_connections = 'on'
log_disconnections = 'on'
log_statement = 'ddl'
log_hostname = 'on'
log_line_prefix = '%m [%p] %u@%d %a %r %c %s '
client_min_messages = 'error'
timezone = 'UTC'
log_timezone = 'UTC'
shared_preload_libraries = 'timescaledb,pgaudit'
pgaudit.log = 'ddl,role,read,write'
pgaudit.log_catalog = 'on'
pgaudit.log_parameter = 'on'
pgaudit.log_statement_once = 'off'
EOF

chmod 0600 "${stig_conf}"
chmod 0700 "${PGDATA}" "${PGLOG}"

echo "STIG configuration written to ${stig_conf}"
