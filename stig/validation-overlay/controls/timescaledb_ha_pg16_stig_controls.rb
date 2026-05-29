require "shellwords"

PSQL_QUERY = lambda do |context, sql|
  password = Shellwords.escape(context.input("pg_dba_password").to_s)
  host = Shellwords.escape(context.input("pg_host").to_s)
  port = Shellwords.escape(context.input("pg_port").to_s)
  user = Shellwords.escape(context.input("pg_dba").to_s)
  database = Shellwords.escape(context.input("pg_db").to_s)
  escaped_sql = Shellwords.escape(sql)

  context.command("PGPASSWORD=#{password} psql -h #{host} -p #{port} -U #{user} -d #{database} -AtX -v ON_ERROR_STOP=1 -c #{escaped_sql}")
end

control "timescaledb-ha-pg16-audit-settings" do
  impact 0.5
  title "TimescaleDB HA PostgreSQL 16 audit settings are enabled"
  desc "Repository-owned checks for audit-related PostgreSQL settings applied by opt-in STIG mode."
  tag stig_controls: %w[V-261866 V-261925 V-261938 V-261942 V-261943 V-261945 V-261952 V-261953 V-261962 V-261963]

  describe PSQL_QUERY.call(self, "SHOW shared_preload_libraries;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/pgaudit/) }
  end

  describe PSQL_QUERY.call(self, "SHOW pgaudit.log;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/ddl/) }
    its("stdout") { should match(/role/) }
    its("stdout") { should match(/read/) }
    its("stdout") { should match(/write/) }
  end

  describe PSQL_QUERY.call(self, "SHOW pgaudit.log_catalog;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aoff\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW pgaudit.log_parameter;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aon\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW pgaudit.log_statement_once;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aoff\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW logging_collector;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aon\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW log_statement;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Addl\s*\z/) }
  end
end

control "timescaledb-ha-pg16-audit-identity-fields" do
  impact 0.5
  title "TimescaleDB HA PostgreSQL 16 audit logs include identity context"
  desc "Repository-owned checks for log prefix fields applied by opt-in STIG mode."
  tag stig_controls: %w[V-261871]

  describe PSQL_QUERY.call(self, "SHOW log_line_prefix;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/%m/) }
    its("stdout") { should match(/%u/) }
    its("stdout") { should match(/%d/) }
    its("stdout") { should match(/%r/) }
  end
end

control "timescaledb-ha-pg16-audit-log-permissions" do
  impact 0.5
  title "TimescaleDB HA PostgreSQL 16 audit log files are restricted"
  desc "Repository-owned checks for audit log directory and PostgreSQL log file mode."
  tag stig_controls: %w[V-261875 V-261876]

  describe directory(input("pg_audit_log_dir")) do
    it { should exist }
    it { should be_directory }
    its("owner") { should eq input("pg_owner") }
    its("mode") { should cmp "0700" }
  end

  describe PSQL_QUERY.call(self, "SHOW log_file_mode;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\A0600\s*\z/) }
  end
end

control "timescaledb-ha-pg16-connection-audit-settings" do
  impact 0.5
  title "TimescaleDB HA PostgreSQL 16 connection auditing is enabled"
  desc "Repository-owned checks for connection and disconnection logging applied by opt-in STIG mode."
  tag stig_controls: %w[V-261960]

  describe PSQL_QUERY.call(self, "SHOW log_connections;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aon\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW log_disconnections;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aon\s*\z/) }
  end
end

control "timescaledb-ha-pg16-external-executable-access" do
  impact 0.0
  title "TimescaleDB HA PostgreSQL 16 external program execution is not delegated"
  desc "Informational observation only: V-261888 is deployment-owned. The hardened image applies no role-membership policy, so this confirms the default PostgreSQL state rather than image enforcement."
  tag stig_controls: %w[V-261888]
  tag informational: true

  describe PSQL_QUERY.call(self, "SELECT count(*) FROM pg_auth_members m JOIN pg_roles r ON r.oid = m.roleid WHERE r.rolname = 'pg_execute_server_program';") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\A0\s*\z/) }
  end
end

control "timescaledb-ha-pg16-password-storage" do
  impact 0.7
  title "TimescaleDB HA PostgreSQL 16 password storage uses SCRAM"
  desc "Repository-owned runtime checks for PostgreSQL password hashing configuration and stored role metadata."
  tag stig_controls: %w[V-261891]

  describe PSQL_QUERY.call(self, "SHOW password_encryption;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Ascram-sha-256\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SELECT count(*) FROM pg_authid WHERE rolcanlogin AND rolpassword IS NOT NULL AND rolpassword NOT LIKE 'SCRAM-SHA-256$%';") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\A0\s*\z/) }
  end
end

control "timescaledb-ha-pg16-password-authentication-transport" do
  impact 0.0
  title "TimescaleDB HA PostgreSQL 16 host authentication avoids cleartext methods"
  desc "Informational observation only: V-261892 is deployment-owned. The hardened image authors no pg_hba rules, so this confirms the observed authentication state rather than image enforcement."
  tag stig_controls: %w[V-261892]
  tag informational: true

  describe PSQL_QUERY.call(self, "SELECT count(*) FROM pg_hba_file_rules WHERE type IN ('host', 'hostssl', 'hostnossl') AND auth_method IN ('password', 'md5', 'trust');") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\A0\s*\z/) }
  end
end

control "timescaledb-ha-pg16-time-settings" do
  impact 0.5
  title "TimescaleDB HA PostgreSQL 16 time settings are UTC-compatible"
  desc "Repository-owned runtime checks for PostgreSQL time settings and timestamp precision."
  tag stig_controls: %w[V-261867 V-261921 V-261922]

  describe PSQL_QUERY.call(self, "SHOW timezone;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\AUTC\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SHOW log_timezone;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\AUTC\s*\z/) }
  end

  describe PSQL_QUERY.call(self, "SELECT CASE WHEN length(to_char(clock_timestamp(), 'YYYY-MM-DD HH24:MI:SS')) = 19 THEN 'ok' ELSE 'unexpected' END;") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/\Aok\s*\z/) }
  end
end
