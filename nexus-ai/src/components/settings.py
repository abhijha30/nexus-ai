import streamlit as st

from src.ai.openrouter_provider import check_connection
from src.config.settings import DEFAULT_SETTINGS, get_api_key
from src.database import conversations as db
from src.database.db import DatabaseError
from src.utils.validators import ValidationError, validate_settings


def _status_chip(ok: bool, text: str) -> None:
    st.markdown(
        f'<span class="nx-status"><span class="nx-dot {"" if ok else "off"}"></span>{text}</span>',
        unsafe_allow_html=True,
    )


@st.dialog("Settings", width="large")
def settings_dialog(models: list[str]) -> None:
    current = st.session_state.settings
    key = get_api_key()

    st.markdown("**Connection**")
    _status_chip(bool(key), "API key found" if key else "No API key")
    if st.button("Test connection", key="test_conn"):
        with st.spinner("Checking…"):
            ok, msg = check_connection(key)
        (st.success if ok else st.error)(msg)

    with st.form("settings_form", border=False):
        options = models if current["model"] in models else [current["model"], *models]
        model = st.selectbox("Model", options, index=options.index(current["model"]))
        custom = st.text_input("Custom model ID (optional)", placeholder="provider/model-name",
                               help="Overrides the list above if filled in.")
        c1, c2 = st.columns(2)
        temperature = c1.slider("Temperature", 0.0, 2.0, float(current["temperature"]), 0.05,
                                help="Lower is focused, higher is more creative.")
        max_tokens = c2.number_input("Max response tokens", 64, 8192, int(current["max_tokens"]), 64)
        system_prompt = st.text_area("System prompt", current["system_prompt"], height=140)
        saved = st.form_submit_button("Save settings", type="primary", use_container_width=True)

    if saved:
        try:
            st.session_state.settings = validate_settings({
                "model": custom.strip() or model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "system_prompt": system_prompt,
            })
            st.rerun()
        except ValidationError as exc:
            st.error(str(exc))

    if st.button("Reset to defaults", use_container_width=True, key="reset_settings"):
        st.session_state.settings = dict(DEFAULT_SETTINGS)
        st.rerun()

    with st.expander("Danger zone"):
        sure = st.checkbox("I understand this deletes every chat permanently")
        if st.button("Clear all chat history", disabled=not sure, use_container_width=True, key="clear_all"):
            try:
                db.clear_all()
            except DatabaseError as exc:
                st.error(str(exc))
                return
            st.session_state.active_id = None
            st.session_state.messages = []
            st.rerun()
