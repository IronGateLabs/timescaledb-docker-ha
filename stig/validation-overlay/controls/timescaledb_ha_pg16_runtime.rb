control "timescaledb-ha-pg16-runtime" do
  impact 0.0
  title "TimescaleDB HA PostgreSQL 16 runtime exposes validation targets"
  desc "Repository-owned preflight checks that the target image exposes the expected PostgreSQL 16 files and database connection."
  tag informational: true

  describe directory(input("pg_data_dir")) do
    it { should exist }
    it { should be_directory }
    its("owner") { should eq input("pg_owner") }
  end

  describe file(input("pg_conf_file")) do
    it { should exist }
    it { should be_file }
  end

  describe file(input("pg_hba_conf_file")) do
    it { should exist }
    it { should be_file }
  end

  input("pg_shared_dirs").each do |shared_dir|
    describe directory(shared_dir) do
      it { should exist }
      it { should be_directory }
    end
  end

  describe file("/usr/lib/postgresql/16/bin/psql") do
    it { should exist }
    it { should be_executable }
  end

  describe file("/usr/lib/postgresql/16/lib/pgaudit.so") do
    it { should exist }
    it { should be_file }
  end

  describe command("PGPASSWORD=#{input("pg_dba_password")} psql -h #{input("pg_host")} -p #{input("pg_port")} -U #{input("pg_dba")} -d #{input("pg_db")} -AtX -c 'SHOW server_version_num'") do
    its("exit_status") { should eq 0 }
    its("stdout") { should match(/^16[0-9]{4}/) }
  end
end
