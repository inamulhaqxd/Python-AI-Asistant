# modules/chatbot.py
# Python Chatbot — conversational assistant with memory

import streamlit as st
from modules import ui, groq_client

SYSTEM = """You are an expert Python developer acting as a coding assistant.
Answer questions clearly and accurately at any experience level.
Always provide code examples in ```python blocks.
Be concise. Avoid padding. Redirect non-Python topics politely."""

STARTERS = [
    "How do I read a CSV file in Python?",
    "What is a decorator and how does it work?",
    "How should I handle exceptions properly?",
    "What is the difference between a list and a tuple?",
    "How do I make HTTP requests in Python?",
    "What are type hints and when should I use them?",
    "How does list comprehension work?",
    "How do I connect Python to a PostgreSQL database?",
]

STYLES = {
    "Standard":          "Answer clearly and completely.",
    "Concise":           "Be brief. Get to the point immediately.",
    "Beginner-friendly": "Use simple language. Avoid jargon. Include analogies.",
}


def render():
    label, model_id = groq_client.model_info("chat")
    ui.page_header("Chatbot", "Ask any Python question. The assistant maintains conversation context.")
    ui.model_tag(label, model_id)

    col_main, col_side = st.columns([3, 1])

    with col_side:
        st.markdown("**Common Questions**")
        for q in STARTERS:
            if st.button(q, key=f"s_{q[:12]}", use_container_width=True):
                st.session_state["chat_prefill"] = q
        ui.divider()
        style = st.selectbox("Response Style", list(STYLES.keys()),
                             key="chat_style")
        if st.button("Clear Conversation", use_container_width=True,
                     key="chat_clr"):
            st.session_state["chat_msgs"] = []
            st.rerun()

    with col_main:
        if "chat_msgs" not in st.session_state:
            st.session_state["chat_msgs"] = [{
                "role": "assistant",
                "content": (
                    "Hello. I am your Python assistant.\n\n"
                    "You can ask me about debugging, language concepts, "
                    "library recommendations, architecture, or anything else "
                    "related to Python development."
                )
            }]

        for msg in st.session_state["chat_msgs"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prefill    = st.session_state.pop("chat_prefill", "")
        user_input = st.chat_input("Ask a Python question...") or prefill

        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            st.session_state["chat_msgs"].append(
                {"role": "user", "content": user_input}
            )

            system = SYSTEM + f"\n\nStyle instruction: {STYLES[style]}"
            messages = [{"role": "system", "content": system}]
            messages += st.session_state["chat_msgs"][-12:]

            with st.chat_message("assistant"):
                with st.spinner(""):
                    reply = groq_client.call(
                        "chat", messages, temperature=0.4, max_tokens=2048
                    )
                st.markdown(reply)

            st.session_state["chat_msgs"].append(
                {"role": "assistant", "content": reply}
            )
