"""Input validation. Each function returns the cleaned value or raises ValidationError."""
import re


class ValidationError(ValueError):
    """Raised with a message that is safe to show to the user."""


MAX_PROMPT = 8000
MAX_TITLE = 80
MAX_SYSTEM_PROMPT = 4000


def validate_prompt(text) -> str:
    text = (text or "").strip()
    if not text:
        raise ValidationError("Type a message before sending.")
    if len(text) > MAX_PROMPT:
        raise ValidationError(f"Messages are limited to {MAX_PROMPT} characters.")
    return text


def validate_title(title) -> str:
    title = " ".join((title or "").split())
    if not title:
        raise ValidationError("Chat name can't be empty.")
    if len(title) > MAX_TITLE:
        raise ValidationError(f"Chat name must be {MAX_TITLE} characters or fewer.")
    return title


def validate_temperature(value) -> float:
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValidationError("Temperature must be a number.")
    if not 0.0 <= value <= 2.0:
        raise ValidationError("Temperature must be between 0 and 2.")
    return value


def validate_max_tokens(value) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Max tokens must be a whole number.")
    if not 64 <= value <= 8192:
        raise ValidationError("Max tokens must be between 64 and 8192.")
    return value


def validate_system_prompt(text) -> str:
    text = (text or "").strip()
    if len(text) > MAX_SYSTEM_PROMPT:
        raise ValidationError(f"System prompt is limited to {MAX_SYSTEM_PROMPT} characters.")
    return text


def validate_model(model) -> str:
    model = (model or "").strip()
    if not model or not re.fullmatch(r"[\w.\-:/]+", model):
        raise ValidationError("Choose a valid model ID, for example openai/gpt-4o-mini.")
    return model


def validate_settings(settings: dict) -> dict:
    return {
        "model": validate_model(settings.get("model")),
        "temperature": validate_temperature(settings.get("temperature")),
        "max_tokens": validate_max_tokens(settings.get("max_tokens")),
        "system_prompt": validate_system_prompt(settings.get("system_prompt")),
    }
