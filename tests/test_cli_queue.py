from typer.testing import CliRunner

from teho_automation.cli import app


def test_list_requests_uses_csv_when_supabase_missing(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    queue_file = data_dir / "company_queue.csv"
    queue_file.write_text(
        "company_name,slug,status,priority,requested_at\n"
        "Acme Corp,acme-corp,queued,5,2025-01-01T00:00:00\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)

    runner = CliRunner()
    result = runner.invoke(app, ["list-requests"])
    assert result.exit_code == 0
    assert "Acme Corp" in result.stdout


def test_process_queue_dry_run_uses_csv(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    queue_file = data_dir / "company_queue.csv"
    queue_file.write_text(
        "company_name,slug,status,priority,requested_at\n"
        "Beta Ltd,beta-ltd,queued,5,2025-01-02T00:00:00\n",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)

    runner = CliRunner()
    result = runner.invoke(app, ["process-queue", "--dry-run", "--limit", "1"])
    assert result.exit_code == 0
    assert "Processing Beta Ltd" in result.stdout
