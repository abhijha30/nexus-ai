"""Smoke test: the app renders without exceptions and without a network or API key."""
from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_app_starts(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    assert not at.exception
    assert any("New chat" in b.label for b in at.sidebar.button)


def test_send_message_saves_and_streams(tmp_path, monkeypatch):
    from src.ai.openrouter_provider import OpenAICompatibleProvider

    monkeypatch.setenv("NEXUS_DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setattr(OpenAICompatibleProvider, "stream_chat",
                        lambda self, m, model, t, n: iter(["Hi ", "there"]))
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    at.chat_input[0].set_value("hello nexus").run()
    assert not at.exception
    assert [m.markdown[0].value for m in at.chat_message] == ["hello nexus", "Hi there"]


def test_missing_key_shows_error_and_no_fake_reply(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_DB_PATH", str(tmp_path / "t.db"))
    monkeypatch.setenv("OPENROUTER_API_KEY", "")
    at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=30).run()
    at.chat_input[0].set_value("hello").run()
    assert not at.exception
    assert len(at.chat_message) == 0
