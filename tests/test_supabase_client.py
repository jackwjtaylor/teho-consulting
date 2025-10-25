from types import SimpleNamespace

from teho_automation import supabase_client


def test_insert_briefing_request_without_env(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    result = supabase_client.insert_briefing_request({"slug": "test-company"})
    assert result.success is False
    assert "Supabase not configured" in result.message or result.message == ""


def test_set_portal_user_access_without_env(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    result = supabase_client.set_portal_user_access("user@example.com", "acme")
    assert result.success is False
    assert "Supabase not configured" in result.message


def test_set_portal_user_access_updates_metadata(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-key")
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    captured = {}

    class DummyResponse:
        def __init__(self, status_code: int, payload: dict | None = None):
            self.status_code = status_code
            self._payload = payload or {}
            self.text = "dummy"
            self.content = b"{}" if payload is not None else b""

        def json(self):  # pragma: no cover - simple helper
            return self._payload

    def fake_get(url, params=None, headers=None, timeout=None):
        captured["get_url"] = url
        captured["get_params"] = params
        captured["get_headers"] = headers
        return DummyResponse(
            200,
            {
                "users": [
                    {
                        "id": "user-123",
                        "user_metadata": {"existing": "value"},
                        "app_metadata": {},
                    }
                ]
            },
        )

    def fake_patch(url, json=None, headers=None, timeout=None):
        captured["patch_url"] = url
        captured["patch_json"] = json
        captured["patch_headers"] = headers
        return DummyResponse(200, {"id": "user-123"})

    monkeypatch.setattr(supabase_client, "requests", SimpleNamespace(get=fake_get, patch=fake_patch))

    result = supabase_client.set_portal_user_access(
        "user@example.com",
        "acme-co",
        client_id="user-123",
    )

    assert result.success is True
    assert "Portal access updated" in result.message
    assert captured["get_params"] == {"email": "user@example.com"}
    assert captured["patch_url"].endswith("/auth/v1/admin/users/user-123")
    assert captured["patch_json"]["user_metadata"]["client_slug"] == "acme-co"
    assert captured["patch_json"]["user_metadata"]["client_id"] == "user-123"


def test_log_outreach_event_requires_fields(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-key")
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    class DummyClient:
        def table(self, name):  # pragma: no cover - simple inline helper
            raise AssertionError("should not be called when fields missing")

    monkeypatch.setattr(supabase_client, "_build_client", lambda: None)
    result = supabase_client.log_outreach_event({})
    assert result.success is False


def test_log_outreach_event_inserts(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_KEY", "service-key")
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    captured = {}

    class DummyTable:
        def insert(self, data):
            captured["data"] = data
            return DummyExec()

    class DummyExec:
        def execute(self):
            return SimpleNamespace(data={})

    class DummyClient:
        def table(self, name):
            captured["table"] = name
            return DummyTable()

    monkeypatch.setattr(supabase_client, "_build_client", lambda: DummyClient())

    payload = {
        "client_slug": "acme",
        "contact_email": "alex@example.com",
        "event_type": "sent",
        "channel": "email",
        "notes": "first touch",
    }

    result = supabase_client.log_outreach_event(payload)
    assert result.success is True
    assert captured["table"] == "outreach_events"
    assert captured["data"]["client_slug"] == "acme"
    assert captured["data"]["notes"] == "first touch"


def test_fetch_automation_runs_without_env(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.setenv("DOTENV_PATH", "/dev/null")

    result = supabase_client.fetch_automation_runs(["requested"], limit=5)
    assert result.success is False
    assert "Supabase not configured" in result.message or result.message == ""


def test_update_automation_run_calls_supabase(monkeypatch):
    captured = {}

    class DummyQuery:
        def __init__(self):
            captured["executed"] = False

        def eq(self, column, value):
            captured["eq"] = (column, value)
            return self

        def execute(self):
            captured["executed"] = True
            return SimpleNamespace(data={"id": "run-1"})

    class DummyTable:
        def update(self, patch):
            captured["patch"] = patch
            return DummyQuery()

    class DummyClient:
        def table(self, name):
            captured["table"] = name
            return DummyTable()

    monkeypatch.setattr(supabase_client, "_build_client", lambda: DummyClient())

    result = supabase_client.update_automation_run(
        "run-1",
        status="in_progress",
        payload={"attempts": 1},
    )

    assert result.success is True
    assert captured["table"] == "automation_runs"
    assert captured["eq"] == ("id", "run-1")
    assert captured["patch"]["status"] == "in_progress"
    assert captured["patch"]["payload"]["attempts"] == 1
    assert "updated_at" in captured["patch"]
    assert captured["executed"] is True
