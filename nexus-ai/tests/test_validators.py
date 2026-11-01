import pytest

from src.utils.validators import (ValidationError, validate_max_tokens, validate_model,
                                  validate_prompt, validate_settings, validate_temperature,
                                  validate_title)


def test_prompt():
    assert validate_prompt("  hi ") == "hi"
    for bad in ("", "   ", None, "x" * 9000):
        with pytest.raises(ValidationError):
            validate_prompt(bad)


@pytest.mark.parametrize("v", [-0.1, 2.1, "abc", None])
def test_bad_temperature(v):
    with pytest.raises(ValidationError):
        validate_temperature(v)


@pytest.mark.parametrize("v", [10, 99999, "x"])
def test_bad_max_tokens(v):
    with pytest.raises(ValidationError):
        validate_max_tokens(v)


def test_model_and_title():
    assert validate_model("openai/gpt-4o-mini") == "openai/gpt-4o-mini"
    with pytest.raises(ValidationError):
        validate_model("bad model!")
    with pytest.raises(ValidationError):
        validate_title("x" * 200)


def test_settings_ok():
    out = validate_settings({"model": "a/b", "temperature": "0.5", "max_tokens": "256", "system_prompt": " hi "})
    assert out == {"model": "a/b", "temperature": 0.5, "max_tokens": 256, "system_prompt": "hi"}
