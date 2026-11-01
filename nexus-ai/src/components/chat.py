"""Message rendering: welcome screen, message list, copy button."""
import json

import streamlit as st
import streamlit.components.v1 as components

SUGGESTIONS = [
    ("Explain a hard idea", "Explain how transformers work in machine learning, simply."),
    ("Write some code", "Write a Python function that finds duplicate files in a folder."),
    ("Plan my week", "Help me plan a focused work week with deep-work blocks."),
    ("Draft a message", "Draft a polite email asking for a deadline extension."),
]


def render_welcome() -> None:
    st.markdown(
        '<div class="nx-hero"><div class="nx-badge"></div>'
        "<h1>Ask Nexus anything</h1>"
        "<p>Answers, code, and ideas, streamed live.</p>"
        '<span class="nx-tag">Pick a starter or type below</span></div>',
        unsafe_allow_html=True,
    )
    cols = st.columns(2)
    for i, (label, prompt) in enumerate(SUGGESTIONS):
        with cols[i % 2].container(key=f"sugg_{i}"):
            if st.button(label, key=f"sugg_btn_{i}", use_container_width=True):
                st.session_state.queued_prompt = prompt
                st.rerun()


def copy_button(text: str) -> None:
    """Small iframe button; uses the Clipboard API with a textarea fallback."""
    payload = json.dumps(text).replace("</", "<\\/")
    components.html(
        f"""<style>body{{margin:0;padding:2px 4px 6px 2px}}button{{display:inline-flex;align-items:center;gap:7px;font:700 13px 'Space Grotesk',system-ui,sans-serif;
color:#000;background:#FFD93D;border:2px solid #000;border-radius:8px;padding:6px 12px;cursor:pointer;box-shadow:3px 3px 0 #000;transition:transform .08s,box-shadow .08s}}
button:hover{{transform:translate(2px,2px);box-shadow:1px 1px 0 #000}}button:active{{transform:translate(3px,3px);box-shadow:none}}svg{{width:15px;height:15px}}</style>
<button id="b" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg><span id="t">Copy response</span></button>
<script>
const t={payload};const b=document.getElementById('b'),l=document.getElementById('t');
b.onclick=async()=>{{try{{await navigator.clipboard.writeText(t)}}catch(e){{
const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();document.execCommand('copy');a.remove()}}
l.textContent='Copied!';setTimeout(()=>l.textContent='Copy response',1500)}};
</script>""",
        height=48,
    )


def render_messages(messages: list[dict]) -> None:
    for m in messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m["role"] == "assistant":
                copy_button(m["content"])
