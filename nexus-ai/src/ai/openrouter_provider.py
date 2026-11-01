"""OpenRouter via the OpenAI-compatible SDK. Any OpenAI-compatible service works by
changing base_url (see OpenAICompatibleProvider)."""
import json
import logging
import urllib.error
import urllib.request
from typing import Iterator

import openai

from src.ai.provider import ChatProvider, ProviderError
from src.config.settings import FALLBACK_MODELS, OPENROUTER_BASE_URL

log = logging.getLogger(__name__)

MISSING_KEY = (
    "No API key found. Add OPENROUTER_API_KEY to a local .env file, or to Streamlit "
    "secrets when deployed (see README)."
)


class OpenAICompatibleProvider(ChatProvider):
    def __init__(self, api_key, base_url, client=None, extra_headers=None, timeout=60.0):
        self.api_key = api_key
        self._client = client
        if client is None and api_key:
            self._client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url,
                timeout=timeout,
                max_retries=1,
                default_headers=extra_headers or {},
            )

    def stream_chat(self, messages, model, temperature, max_tokens) -> Iterator[str]:
        if not self._client:
            raise ProviderError(MISSING_KEY, "missing_key")
        received = False
        try:
            stream = self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in stream:
                if not getattr(chunk, "choices", None):
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    received = True
                    yield delta
        except ProviderError:
            raise
        except openai.AuthenticationError:
            raise ProviderError("The API key was rejected. Check that it is correct and active.", "auth")
        except openai.RateLimitError:
            raise ProviderError("Rate limit reached. Wait a moment and try again.", "rate_limit")
        except openai.APITimeoutError:
            raise ProviderError("The model took too long to respond. Try again.", "timeout")
        except openai.APIConnectionError:
            raise ProviderError("Can't reach the AI service. Check your internet connection.", "network")
        except (openai.NotFoundError, openai.BadRequestError):
            raise ProviderError(
                "This model isn't available or the request was rejected. Pick another model in Settings.",
                "model",
            )
        except openai.APIStatusError as exc:
            log.warning("provider status error: %s", exc.status_code)
            if exc.status_code == 402:
                raise ProviderError("Not enough credits for this model. Choose a free model or add credits.", "credits")
            raise ProviderError(f"The AI service returned an error ({exc.status_code}). Try again shortly.", "provider")
        except Exception as exc:  # never leak internals
            log.error("unexpected provider failure: %s", type(exc).__name__)
            raise ProviderError("Something went wrong talking to the AI service.", "unexpected")
        if not received:
            raise ProviderError("The model returned an empty response. Try again or switch models.", "empty")


def create_provider(api_key: str | None) -> OpenAICompatibleProvider:
    return OpenAICompatibleProvider(
        api_key,
        OPENROUTER_BASE_URL,
        extra_headers={"X-Title": "Nexus AI"},
    )


def fetch_models(timeout: float = 8.0) -> list[str]:
    """Public model list from OpenRouter; falls back to a static list offline."""
    try:
        with urllib.request.urlopen(f"{OPENROUTER_BASE_URL}/models", timeout=timeout) as resp:
            data = json.load(resp)
        ids = sorted({m["id"] for m in data.get("data", []) if m.get("id")})
        return ids or FALLBACK_MODELS
    except Exception as exc:
        log.info("model list fetch failed: %s", type(exc).__name__)
        return FALLBACK_MODELS


def check_connection(api_key: str | None, timeout: float = 8.0) -> tuple[bool, str]:
    if not api_key:
        return False, MISSING_KEY
    req = urllib.request.Request(
        f"{OPENROUTER_BASE_URL}/auth/key", headers={"Authorization": f"Bearer {api_key}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return True, "Connected. Your API key is valid."
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return False, "The API key was rejected."
        return False, f"The service returned an error ({exc.code})."
    except Exception:
        return False, "Can't reach OpenRouter. Check your internet connection."
