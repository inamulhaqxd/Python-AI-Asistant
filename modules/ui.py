# modules/ui.py
# Shared UI components — professional white theme

import streamlit as st


def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    *, *::before, *::after { box-sizing: border-box; }

    html, body, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f9f9fb !important;
        color: #111827;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 0 2.5rem 3rem 2.5rem !important;
        max-width: 1180px !important;
    }

    /* Header */
    .app-header {
        background: #111827;
        padding: 22px 36px;
        margin: -1rem -2.5rem 0 -2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .app-header-left { display: flex; flex-direction: column; gap: 2px; }
    .app-header-title {
        color: #ffffff;
        font-size: 1.25em;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    .app-header-sub {
        color: #6b7280;
        font-size: 0.8em;
        font-weight: 400;
    }
    .app-header-badge {
        background: #1f2937;
        border: 1px solid #374151;
        color: #9ca3af;
        font-size: 0.75em;
        padding: 4px 12px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Navbar */
    .navbar {
        background: #ffffff;
        border-bottom: 1px solid #e5e7eb;
        margin: 0 -2.5rem;
        padding: 0 2.5rem;
        display: flex;
        gap: 0;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Override all Streamlit button defaults inside navbar */
    div[data-testid="stHorizontalBlock"] .stButton > button {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
        color: #6b7280 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875em !important;
        font-weight: 500 !important;
        padding: 14px 8px !important;
        box-shadow: none !important;
        transition: color 0.15s, border-color 0.15s !important;
        width: 100% !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        color: #111827 !important;
        border-bottom: 2px solid #d1d5db !important;
        background: transparent !important;
    }
    div[data-testid="stHorizontalBlock"] .stButton > button[kind="primary"] {
        color: #111827 !important;
        border-bottom: 2px solid #111827 !important;
        font-weight: 600 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* Page body */
    .page-body { padding: 32px 0 0 0; }

    /* Page title */
    .page-title {
        font-size: 1.4em;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }
    .page-sub {
        font-size: 0.875em;
        color: #6b7280;
        margin-bottom: 24px;
    }

    /* Model tag */
    .model-tag {
        display: inline-block;
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        color: #374151;
        font-size: 0.75em;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 4px;
        margin-bottom: 20px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Labels */
    .stTextArea label, .stTextInput label,
    .stSelectbox label, .stRadio label,
    label[data-testid="stWidgetLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.78em !important;
        font-weight: 600 !important;
        color: #374151 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }

    /* Text areas */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.85em !important;
        color: #111827 !important;
        padding: 12px !important;
        transition: border-color 0.15s, box-shadow 0.15s !important;
        resize: vertical !important;
    }
    .stTextArea textarea:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 3px rgba(17,24,39,0.08) !important;
        outline: none !important;
    }

    /* Text input */
    .stTextInput input {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875em !important;
        color: #111827 !important;
        padding: 10px 12px !important;
        transition: border-color 0.15s !important;
    }
    .stTextInput input:focus {
        border-color: #111827 !important;
        box-shadow: 0 0 0 3px rgba(17,24,39,0.08) !important;
    }

    /* Primary action button */
    .stButton > button[kind="primary"] {
        background: #111827 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875em !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        box-shadow: none !important;
        transition: background 0.15s !important;
        width: 100% !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1f2937 !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875em !important;
        font-weight: 500 !important;
        transition: background 0.15s, border-color 0.15s !important;
        width: 100% !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #f9fafb !important;
        border-color: #9ca3af !important;
    }

    /* Result panel */
    .result-panel {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px 28px;
        margin-top: 24px;
        animation: fadein 0.25s ease;
    }
    @keyframes fadein {
        from { opacity: 0; transform: translateY(8px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* Question card */
    .q-card {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-left: 3px solid #111827;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 0.875em;
        color: #374151;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: #e5e7eb;
        border: none;
        margin: 24px 0;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 6px !important;
        border-color: #d1d5db !important;
        font-size: 0.875em !important;
    }

    /* Radio */
    .stRadio > div { gap: 8px !important; }
    .stRadio label { font-size: 0.875em !important; }

    /* Chat */
    .stChatMessage {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
    }
    .stChatInputContainer {
        border-top: 1px solid #e5e7eb !important;
        background: #ffffff !important;
    }

    /* Metrics */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px !important;
    }

    /* Placeholder text */
    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder {
        color: #9ca3af !important;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        padding: 28px 0 8px 0;
        color: #9ca3af;
        font-size: 0.8em;
        border-top: 1px solid #e5e7eb;
        margin-top: 48px;
    }

    /* Spinner */
    .stSpinner > div { border-top-color: #111827 !important; }

    /* Code blocks */
    code, pre {
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        font-size: 0.85em !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="app-header-left">
            <div class="app-header-title">Python Code Assistant</div>
            <div class="app-header-sub">Groq — LLaMA 3.3 70B · LLaMA 4 Scout · LLaMA 3.1 8B</div>
        </div>
        <div class="app-header-badge">v2.0</div>
    </div>
    """, unsafe_allow_html=True)


def render_navbar(pages: list) -> str:
    if "active_page" not in st.session_state:
        st.session_state["active_page"] = pages[0]

    cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        with cols[i]:
            is_active = st.session_state["active_page"] == page
            if st.button(page, key=f"nav_{i}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state["active_page"] = page
                for k in ["fix_result", "improve_result", "gen_result",
                          "gen_qs", "explain_result", "convert_result",
                          "conv_code_out"]:
                    st.session_state.pop(k, None)
                st.rerun()

    return st.session_state["active_page"]


def page_header(title: str, subtitle: str):
    st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>{subtitle}</div>", unsafe_allow_html=True)


def model_tag(label: str, model_id: str):
    st.markdown(
        f"<div class='model-tag'>Model: {label} &nbsp;/&nbsp; {model_id}</div>",
        unsafe_allow_html=True
    )


def divider():
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)


def download_code(result: str, filename: str = "code.py"):
    if "```python" in result:
        try:
            code = result.split("```python")[1].split("```")[0].strip()
            st.download_button("Download Code", data=code,
                               file_name=filename, mime="text/plain")
        except Exception:
            pass


def render_footer():
    st.markdown("""
    <div class="app-footer">
        Python Code Assistant &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Groq API
    </div>
    """, unsafe_allow_html=True)
