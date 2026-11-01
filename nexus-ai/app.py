"""Nexus AI — Streamlit entry point."""
import logging

import streamlit as st

from src.ai.openrouter_provider import create_provider, fetch_models
from src.ai.provider import ProviderError
from src.components.chat import render_messages, render_welcome
from src.components.chat_input import render_chat_input
from src.components.settings import settings_dialog
from src.components.sidebar import render_sidebar
from src.components.styles import inject_css
from src.config.settings import APP_NAME, DEFAULT_SETTINGS, get_api_key
from src.database import conversations as db
from src.database.db import DatabaseError, init_db
from src.utils.helpers import build_context, make_title
from src.utils.validators import ValidationError, validate_prompt, validate_settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

st.set_page_config(page_title=APP_NAME, page_icon="✦", layout="wide", initial_sidebar_state="auto")


@st.cache_resource
def _setup() -> bool:
    init_db()
    return True


@st.cache_data(ttl=3600, show_spinner=False)
def _models() -> list[str]:
    return fetch_models()  # public list, safe to share across sessions


def _init_state() -> None:
    ss = st.session_state
    ss.setdefault("active_id", None)
    ss.setdefault("messages", [])
    ss.setdefault("settings", dict(DEFAULT_SETTINGS))
    ss.setdefault("queued_prompt", None)
    ss.setdefault("flash_error", None)


def handle_prompt(raw: str) -> None:
    ss = st.session_state
    try:
        prompt = validate_prompt(raw)
        settings = validate_settings(ss.settings)
    except ValidationError as exc:
        ss.flash_error = str(exc)
        st.rerun()

    api_key = get_api_key()
    if not api_key:
        ss.flash_error = "No API key found. Add OPENROUTER_API_KEY to .env (local) or Streamlit secrets (cloud)."
        st.rerun()

    try:
        if ss.active_id is None:
            ss.active_id = db.create_conversation(make_title(prompt))["id"]
        ss.messages.append(db.add_message(ss.active_id, "user", prompt))
    except (DatabaseError, ValidationError) as exc:
        ss.flash_error = str(exc)
        st.rerun()

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(
                create_provider(api_key).stream_chat(
                    build_context(ss.messages, settings["system_prompt"]),
                    settings["model"], settings["temperature"], settings["max_tokens"],
                )
            )
            ss.messages.append(db.add_message(ss.active_id, "assistant", reply))
        except ProviderError as exc:
            ss.flash_error = exc.user_message
        except DatabaseError as exc:
            ss.flash_error = str(exc)
    st.rerun()  # refresh sidebar order + copy buttons


def main() -> None:
    inject_css()
    try:
        _setup()
    except DatabaseError as exc:
        st.error(str(exc))
        st.stop()
    _init_state()
    render_sidebar(lambda: settings_dialog(_models()))

    ss = st.session_state
    typed = render_chat_input()  # always rendered so it stays pinned to the bottom
    prompt, ss.queued_prompt = typed or ss.queued_prompt, None

    if ss.messages:
        render_messages(ss.messages)
    elif not prompt:
        render_welcome()

    if ss.flash_error:
        st.markdown(f'<div class="nx-error">{ss.flash_error}</div>', unsafe_allow_html=True)
        ss.flash_error = None
    if prompt:
        handle_prompt(prompt)


main()
