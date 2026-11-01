"""Neobrutalist design system (inspired by neobrutalism.dev) with Lucide icons.

Streamlit can't mount React components, so Lucide icon paths are embedded as CSS masks.
"""
import urllib.parse

import streamlit as st

ICONS = {
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "sliders": '<path d="M21 4h-7"/><path d="M10 4H3"/><path d="M21 12h-9"/><path d="M8 12H3"/><path d="M21 20h-5"/><path d="M12 20H3"/><path d="M14 2v4"/><path d="M8 10v4"/><path d="M16 18v4"/>',
    "trash": '<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><path d="M10 11v6"/><path d="M14 11v6"/>',
    "ellipsis": '<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "bot": '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
    "rotate": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/>',
}


def _uri(name: str) -> str:
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000" '
           f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')
    return "data:image/svg+xml," + urllib.parse.quote(svg)


def icon_rule(selector: str, name: str, size: int = 18) -> str:
    u = _uri(name)
    return (f'{selector}::before{{content:"";display:block;flex:none;width:{size}px;height:{size}px;'
            f'background:currentColor;-webkit-mask:url("{u}") center/contain no-repeat;'
            f'mask:url("{u}") center/contain no-repeat}}')


ICON_RULES = [
    (".st-key-new_chat button", "plus", 18),
    (".st-key-open_settings button", "sliders", 18),
    (".st-key-test_conn button", "zap", 18),
    (".st-key-reset_settings button", "rotate", 18),
    (".st-key-clear_all button", "trash", 18),
    (".st-key-confirm_del button", "trash", 18),
    ('[class*="st-key-dl_"] button', "trash", 18),
    ('[class*="st-key-sv_"] button', "check", 18),
    ('[class*="st-key-pop_"] button', "ellipsis", 20),
    (".st-key-sugg_0 button", "bulb", 22),
    (".st-key-sugg_1 button", "code", 22),
    (".st-key-sugg_2 button", "calendar", 22),
    (".st-key-sugg_3 button", "mail", 22),
    (".nx-logo", "zap", 22),
    (".nx-badge", "zap", 46),
    ('[data-testid="stChatMessageAvatarUser"]', "user", 20),
    ('[data-testid="stChatMessageAvatarAssistant"]', "bot", 20),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
:root{--bg:#272933;--card:#353849;--side:#1F212B;--text:#F5F5F5;--muted:#A9ADBC;--bd:#000;
--main:#8B5CF6;--blue:#5294FF;--yellow:#FFD93D;--mint:#7EE8B1;--pink:#FF8FB1;--red:#FF5C5C;--user:#4C3F8F;
--r:10px;--sh:4px 4px 0 var(--bd);--sh-s:2px 2px 0 var(--bd)}
html,body,.stApp,.stMarkdown,.stMarkdown p,button p,label,input,textarea,[data-baseweb]{font-family:'Space Grotesk',system-ui,sans-serif}
code,pre,[data-testid="stCode"] *{font-family:'JetBrains Mono',ui-monospace,monospace!important}
.stApp{color:var(--text);font-weight:500;background-color:var(--bg);
 background-image:radial-gradient(rgba(255,255,255,.075) 1.3px,transparent 1.4px);background-size:24px 24px}
header[data-testid="stHeader"]{background:transparent}
#MainMenu,footer,[data-testid="stAppDeployButton"],[data-testid="stStatusWidget"]{display:none!important}
.block-container{max-width:880px;padding:2.2rem 1.25rem 7.5rem}
[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"]{background:transparent!important}
h1,h2,h3{font-weight:700;letter-spacing:-.02em}

/* sidebar */
section[data-testid="stSidebar"]{background:var(--side);border-right:3px solid var(--bd)}
[data-testid="stSidebarUserContent"]{padding-top:.8rem}
[data-testid="stSidebarCollapseButton"] button,[data-testid="stExpandSidebarButton"],[data-testid="stSidebarCollapsedControl"] button{
 background:var(--yellow)!important;color:#000!important;border:2px solid var(--bd)!important;border-radius:8px!important;box-shadow:var(--sh-s)}
[data-testid="stExpandSidebarButton"] *,[data-testid="stSidebarCollapseButton"] *{color:#000!important}
.nx-brand{display:flex;align-items:center;gap:.75rem;margin:.1rem 0 1.1rem}
.nx-logo{width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:var(--yellow);color:#000;
 border:2px solid var(--bd);border-radius:8px;box-shadow:var(--sh-s);transform:rotate(-5deg)}
.nx-brand b{font-size:1.3rem;font-weight:700;letter-spacing:-.02em;display:block;line-height:1.1}
.nx-brand span{display:block;font-size:.78rem;color:var(--muted)}
.nx-label{font-weight:700;font-size:.85rem;margin:1.1rem 0 .5rem;display:inline-block;background:var(--mint);color:#000;
 border:2px solid var(--bd);border-radius:6px;padding:.05rem .5rem;box-shadow:var(--sh-s)}

/* buttons */
.stButton>button,[data-testid="stPopover"]>button{display:inline-flex;align-items:center;justify-content:center;gap:.55rem;
 min-height:2.7rem;font-weight:700;color:var(--text)!important;background:var(--card)!important;
 border:2px solid var(--bd)!important;border-radius:8px!important;box-shadow:var(--sh)!important;
 transition:transform .08s,box-shadow .08s}
.stButton>button p{color:inherit!important;font-weight:700}
.stButton>button:hover,[data-testid="stPopover"]>button:hover{transform:translate(2px,2px);box-shadow:var(--sh-s)!important}
.stButton>button:active,[data-testid="stPopover"]>button:active{transform:translate(4px,4px);box-shadow:none!important}
.stButton>button:focus-visible{outline:3px solid var(--yellow);outline-offset:2px}
[data-testid="stBaseButton-primary"]{background:var(--main)!important;color:#fff!important}
[data-testid="stPopover"]>button [data-testid="stIconMaterial"]{display:none}
[class*="st-key-pop_"] button{padding:0!important;min-width:2.5rem}
.st-key-confirm_del button,[class*="st-key-dl_"] button{background:var(--red)!important;color:#000!important}
[class*="st-key-sv_"] button{background:var(--mint)!important;color:#000!important}
.st-key-new_chat button{background:var(--yellow)!important;color:#000!important}

/* chat rows */
[class*="st-key-row_"] .stButton>button,[class*="st-key-active_"] .stButton>button{justify-content:flex-start;text-align:left;box-shadow:var(--sh-s)!important;min-height:2.5rem}
[class*="st-key-row_"] .stButton>button p,[class*="st-key-active_"] .stButton>button p{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
[class*="st-key-active_"] .stButton>button{background:var(--yellow)!important;color:#000!important}
[class*="st-key-row_"] [data-testid="stPopover"]>button,[class*="st-key-active_"] [data-testid="stPopover"]>button{box-shadow:var(--sh-s)!important;min-height:2.5rem}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]{flex-direction:row!important;flex-wrap:nowrap!important;gap:.5rem}
section[data-testid="stSidebar"] [data-testid="stColumn"]{min-width:0!important}

/* inputs */
.stTextInput input,.stTextArea textarea,.stNumberInput input,[data-baseweb="select"]>div{background:var(--card)!important;color:var(--text)!important;
 border:2px solid var(--bd)!important;border-radius:8px!important;box-shadow:var(--sh-s)}
.stTextInput input:focus,.stTextArea textarea:focus{box-shadow:4px 4px 0 var(--main)!important}
[data-testid="stChatInput"]{background:var(--card);border:2px solid var(--bd);border-radius:12px;box-shadow:var(--sh);transition:box-shadow .1s}
[data-testid="stChatInput"]:focus-within{box-shadow:6px 6px 0 var(--main)}
[data-testid="stChatInput"] textarea{font-size:1rem;font-weight:500}
[data-testid="stChatInput"] button{background:var(--yellow)!important;color:#000!important;border:2px solid var(--bd)!important;border-radius:8px!important}
[data-testid="stChatInput"] button *{color:#000!important}
[data-testid="stExpander"] details{border:2px solid var(--bd);border-radius:8px;background:var(--card);box-shadow:var(--sh-s)}
[data-testid="stAlert"]{border:2px solid var(--bd);border-radius:8px;box-shadow:var(--sh-s)}
hr{border-color:var(--bd)!important;border-width:2px 0 0!important;opacity:1!important}
div[role="dialog"]{background:var(--card)!important;border:3px solid var(--bd)!important;border-radius:12px!important;box-shadow:8px 8px 0 var(--bd)!important}
[data-baseweb="popover"]>div{border:2px solid var(--bd)!important;border-radius:8px!important;box-shadow:var(--sh)}

/* messages */
[data-testid="stChatMessage"]{background:var(--card);border:2px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:1rem 1.1rem;margin-bottom:1.1rem;gap:.9rem}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]){background:var(--user)}
[data-testid="stChatMessage"] .stMarkdown{overflow-wrap:anywhere;line-height:1.65}
[data-testid="stChatMessageAvatarUser"],[data-testid="stChatMessageAvatarAssistant"]{width:2.4rem;height:2.4rem;border-radius:8px;border:2px solid var(--bd);
 box-shadow:var(--sh-s);display:flex;align-items:center;justify-content:center;color:#000;flex:none}
[data-testid="stChatMessageAvatarUser"]{background:var(--pink)}
[data-testid="stChatMessageAvatarAssistant"]{background:var(--mint)}
[data-testid="stChatMessageAvatarUser"]>*,[data-testid="stChatMessageAvatarAssistant"]>*{display:none}
[data-testid="stCode"] pre,.stMarkdown pre{background:#0E1016!important;border:2px solid var(--bd);border-radius:8px;box-shadow:var(--sh-s);overflow-x:auto;max-width:100%}
.stMarkdown :not(pre)>code{background:var(--yellow);color:#000;border:1.5px solid var(--bd);border-radius:5px;padding:.05rem .35rem}
.stMarkdown table{display:block;overflow-x:auto}
.stMarkdown th{background:var(--yellow);color:#000;border:2px solid var(--bd)}.stMarkdown td{border:2px solid var(--bd)}
.nx-error{background:var(--red);color:#000;font-weight:700;border:2px solid var(--bd);border-radius:var(--r);box-shadow:var(--sh);padding:.85rem 1.1rem}
.nx-status{display:inline-flex;align-items:center;gap:.5rem;padding:.3rem .8rem;border:2px solid var(--bd);border-radius:999px;background:var(--card);box-shadow:var(--sh-s);font-weight:700;font-size:.85rem}
.nx-dot{width:11px;height:11px;border-radius:50%;background:var(--mint);border:2px solid var(--bd)}.nx-dot.off{background:var(--red)}

/* hero */
.nx-hero{text-align:center;padding:1.6rem 0 1.6rem}
.nx-badge{width:88px;height:88px;margin:0 auto 1.6rem;display:flex;align-items:center;justify-content:center;background:var(--yellow);color:#000;
 border:3px solid var(--bd);border-radius:14px;box-shadow:7px 7px 0 var(--bd);transform:rotate(-6deg)}
.nx-hero h1{font-size:3.3rem;line-height:1.02;margin:0 0 .9rem;padding:0;text-shadow:4px 4px 0 var(--main)}
.nx-hero p{color:var(--muted);margin:0 0 1rem;font-size:1.08rem}
.nx-tag{display:inline-block;background:var(--mint);color:#000;font-weight:700;font-size:.85rem;border:2px solid var(--bd);border-radius:6px;padding:.2rem .7rem;box-shadow:var(--sh-s);transform:rotate(2deg)}
[class*="st-key-sugg_"] .stButton>button{height:auto;min-height:4.4rem;padding:.9rem 1.1rem;justify-content:flex-start;text-align:left;color:#000!important;font-size:1.02rem}
[class*="st-key-sugg_"] .stButton>button p{white-space:normal}
.st-key-sugg_0 button{background:var(--yellow)!important}.st-key-sugg_1 button{background:var(--mint)!important}
.st-key-sugg_2 button{background:var(--pink)!important}.st-key-sugg_3 button{background:#9CC1FF!important}

@media (max-width:640px){
 :root{--sh:3px 3px 0 var(--bd)}
 .block-container{padding:1.2rem .75rem 7rem}
 .nx-hero h1{font-size:2.2rem}.nx-badge{width:70px;height:70px}
 [data-testid="stChatMessage"]{padding:.75rem .8rem}
 .stButton>button{min-height:2.9rem}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""


def inject_css() -> None:
    icons = "".join(icon_rule(sel, name, size) for sel, name, size in ICON_RULES)
    st.markdown(f"<style>{CSS}{icons}</style>", unsafe_allow_html=True)
