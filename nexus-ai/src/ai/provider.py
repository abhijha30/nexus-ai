"""Provider interface. Add a new provider by subclassing ChatProvider."""
from abc import ABC, abstractmethod
from typing import Iterator


class ProviderError(Exception):
    """An AI request failed. `user_message` is safe to display (never contains secrets)."""

    def __init__(self, user_message: str, code: str = "error"):
        super().__init__(user_message)
        self.user_message = user_message
        self.code = code


class ChatProvider(ABC):
    @abstractmethod
    def stream_chat(
        self, messages: list[dict], model: str, temperature: float, max_tokens: int
    ) -> Iterator[str]:
        """Yield text chunks. Raise ProviderError on any failure."""
