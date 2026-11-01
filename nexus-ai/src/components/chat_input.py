import streamlit as st

from src.utils.validators import MAX_PROMPT


def render_chat_input() -> str | None:
    """Returns the submitted text once per submission (Enter sends, Shift+Enter adds a line)."""
    return st.chat_input("Message Nexus…  (Shift+Enter for a new line)", max_chars=MAX_PROMPT)
