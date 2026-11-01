import streamlit as st

from src.config.settings import APP_NAME
from src.database import conversations as db
from src.database.db import DatabaseError
from src.utils.helpers import time_ago
from src.utils.validators import ValidationError


def new_chat() -> None:
    st.session_state.active_id = None
    st.session_state.messages = []


def open_chat(conv_id: str) -> None:
    st.session_state.active_id = conv_id
    st.session_state.messages = db.get_messages(conv_id)


@st.dialog("Delete this chat?")
def confirm_delete(conv_id: str, title: str) -> None:
    st.write(f"“{title}” and all of its messages will be permanently deleted.")
    a, b = st.columns(2)
    if a.button("Cancel", use_container_width=True, key="cancel_del"):
        st.rerun()
    if b.button("Delete", use_container_width=True, key="confirm_del"):
        try:
            db.delete_conversation(conv_id)
            if st.session_state.active_id == conv_id:
                new_chat()
        except DatabaseError as exc:
            st.error(str(exc))
            return
        st.rerun()


def _row(conv: dict) -> None:
    active = conv["id"] == st.session_state.active_id
    with st.container(key=f"{'active' if active else 'row'}_{conv['id']}"):
        c1, c2 = st.columns([6, 1.3])
        if c1.button(conv["title"], key=f"open_{conv['id']}", use_container_width=True,
                     help=f"Updated {time_ago(conv['updated_at'])}"):
            open_chat(conv["id"])
            st.rerun()
        with c2.container(key=f"pop_{conv['id']}"), st.popover("\u200b", use_container_width=True):
            name = st.text_input("Rename", value=conv["title"], key=f"rn_{conv['id']}")
            if st.button("Save name", key=f"sv_{conv['id']}", use_container_width=True):
                try:
                    db.rename_conversation(conv["id"], name)
                    st.rerun()
                except ValidationError as exc:
                    st.warning(str(exc))
            if st.button("Delete chat", key=f"dl_{conv['id']}", use_container_width=True):
                confirm_delete(conv["id"], conv["title"])


def render_sidebar(open_settings) -> None:
    with st.sidebar:
        st.markdown(
            f'<div class="nx-brand"><div class="nx-logo"></div><div><b>{APP_NAME}</b>'
            "<span>Your AI workspace</span></div></div>",
            unsafe_allow_html=True,
        )
        if st.button("New chat", type="primary", use_container_width=True, key="new_chat"):
            new_chat()
            st.rerun()
        query = st.text_input("Search chats", key="search", placeholder="Search chats",
                              label_visibility="collapsed")
        st.markdown('<div class="nx-label">Chats</div>', unsafe_allow_html=True)
        try:
            convs = db.list_conversations(query)
        except DatabaseError as exc:
            st.error(str(exc))
            convs = []
        if not convs:
            st.caption("No matching chats." if query else "Your chats will appear here.")
        for conv in convs:
            _row(conv)
        st.divider()
        if st.button("Settings", use_container_width=True, key="open_settings"):
            open_settings()
        with st.expander("About"):
            st.caption(
                "Nexus AI streams answers from models on OpenRouter. Chats are stored locally "
                "in SQLite on the machine running the app."
            )
