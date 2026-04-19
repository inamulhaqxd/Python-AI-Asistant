# main.py
# Python Code Assistant
# Entry point and router

import streamlit as st
from modules import ui, groq_client, fix, improve, generate, explain, convert, chatbot

st.set_page_config(
    page_title="Python Code Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ui.load_css()
ui.render_header()

PAGES = {
    "Generate":  "generate",
    "Improve":   "improve",
    "Fix Error": "fix",
    "Explain":   "explain",
    "Convert":   "convert",
    "Chatbot":   "chatbot",
}

selected = ui.render_navbar(list(PAGES.keys()))
page_key = PAGES[selected]

st.markdown("<div class='page-body'>", unsafe_allow_html=True)

if   page_key == "generate": generate.render()
elif page_key == "improve":  improve.render()
elif page_key == "fix":      fix.render()
elif page_key == "explain":  explain.render()
elif page_key == "convert":  convert.render()
elif page_key == "chatbot":  chatbot.render()

st.markdown("</div>", unsafe_allow_html=True)
ui.render_footer()
