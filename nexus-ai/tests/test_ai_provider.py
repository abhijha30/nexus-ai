from types import SimpleNamespace

import httpx
import openai
import pytest

from src.ai.openrouter_provider import OpenAICompatibleProvider
from src.ai.provider import ProviderError
from src.utils.helpers import build_context

REQ = httpx.Request("POST", "https://x.test")


def chunk(text):
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=text))])


class FakeClient:
    def __init__(self, items=None, exc=None):
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))
        self.items, self.exc, self.kwargs = items or [], exc, None

    def _create(self, **kwargs):
        self.kwargs = kwargs
        if self.exc:
            raise self.exc
        return iter(self.items)


def run(client):
    p = OpenAICompatibleProvider("k", "https://x.test", client=client)
    return "".join(p.stream_chat([{"role": "user", "content": "hi"}], "m/x", 0.5, 100))


def test_streams_chunks_and_passes_params():
    client = FakeClient([chunk("Hel"), SimpleNamespace(choices=[]), chunk("lo"), chunk(None)])
    assert run(client) == "Hello"
    assert client.kwargs["stream"] is True and client.kwargs["model"] == "m/x"


def test_missing_key():
    p = OpenAICompatibleProvider(None, "https://x.test")
    with pytest.raises(ProviderError) as e:
        list(p.stream_chat([], "m", 0.5, 100))
    assert e.value.code == "missing_key"


def test_empty_response():
    with pytest.raises(ProviderError) as e:
        run(FakeClient([chunk(None), chunk("")]))
    assert e.value.code == "empty"


def _status(cls, code):
    return cls("boom", response=httpx.Response(code, request=REQ), body=None)


@pytest.mark.parametrize("exc,code", [
    (_status(openai.AuthenticationError, 401), "auth"),
    (_status(openai.RateLimitError, 429), "rate_limit"),
    (_status(openai.NotFoundError, 404), "model"),
    (openai.APITimeoutError(request=REQ), "timeout"),
    (openai.APIConnectionError(request=REQ), "network"),
    (_status(openai.InternalServerError, 500), "provider"),
    (RuntimeError("sk-secret-123"), "unexpected"),
])
def test_error_mapping_never_leaks(exc, code):
    with pytest.raises(ProviderError) as e:
        run(FakeClient(exc=exc))
    assert e.value.code == code
    assert "sk-secret" not in e.value.user_message


def test_build_context_limits_and_prepends_system():
    msgs = [{"role": "user", "content": str(i), "created_at": "x"} for i in range(40)]
    ctx = build_context(msgs, "sys", limit=5)
    assert ctx[0] == {"role": "system", "content": "sys"} and len(ctx) == 6
    assert "created_at" not in ctx[1]
