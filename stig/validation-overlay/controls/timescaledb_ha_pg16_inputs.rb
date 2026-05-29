control "timescaledb-ha-pg16-inputs" do
  impact 0.0
  title "TimescaleDB HA PostgreSQL 16 validation inputs are image-compatible"
  desc "Repository-owned preflight checks for runner inputs used with the TimescaleDB HA PostgreSQL 16 image."
  tag informational: true

  describe input("pg_version") do
    it { should match(/^16(\.|$|\.x$)/) }
  end

  describe input("pg_data_dir") do
    it { should eq "/home/postgres/pgdata/data" }
  end

  describe input("pg_log_dir") do
    it { should eq "/home/postgres/pg_log" }
  end

  describe input("pg_audit_log_dir") do
    it { should eq "/home/postgres/pg_log" }
  end

  describe input("pg_conf_file") do
    it { should eq "/home/postgres/pgdata/data/postgresql.conf" }
  end

  describe input("pg_hba_conf_file") do
    it { should eq "/home/postgres/pgdata/data/pg_hba.conf" }
  end

  describe input("pg_ident_conf_file") do
    it { should eq "/home/postgres/pgdata/data/pg_ident.conf" }
  end

  describe input("pg_shared_dirs") do
    it { should include "/usr/lib/postgresql/16" }
    it { should include "/usr/lib/postgresql/16/bin" }
    it { should include "/usr/lib/postgresql/16/lib" }
    it { should include "/usr/share/postgresql/16" }
  end

  describe input("pgaudit_installation") do
    it { should eq "/usr/lib/postgresql/16/lib" }
  end

  describe input("approved_packages") do
    it { should include "postgresql-16" }
    it { should include "postgresql-client-16" }
    it { should include "postgresql-16-pgaudit" }
  end

  describe input("approved_ext") do
    it { should include "plpgsql" }
    it { should include "pgaudit" }
    it { should include "timescaledb" }
  end
end
