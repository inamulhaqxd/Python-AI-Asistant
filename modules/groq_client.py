# modules/groq_client.py
# Groq API client — confirmed working models, April 2026
#
# Dead models — do not use:
#   gemma2-9b-it           (decommissioned)
#   mixtral-8x7b-32768     (decommissioned)

import streamlit as st
from groq import Groq

MODELS = {
    "fix":      "llama-3.3-70b-versatile",
    "improve":  "llama-3.3-70b-versatile",
    "generate": "meta-llama/llama-4-scout-17b-16e-instruct",
    "explain":  "llama-3.1-8b-instant",
    "convert":  "llama-3.1-8b-instant",
    "chat":     "llama-3.3-70b-versatile",
}

LABELS = {
    "llama-3.3-70b-versatile":                   "LLaMA 3.3 70B",
    "meta-llama/llama-4-scout-17b-16e-instruct":  "LLaMA 4 Scout 17B",
    "llama-3.1-8b-instant":                       "LLaMA 3.1 8B Instant",
}


@st.cache_resource
def get_client():
    try:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        st.error(
            "GROQ_API_KEY not found. "
            "Add it to .streamlit/secrets.toml:\n\n"
            "GROQ_API_KEY = 'gsk_your_key_here'"
        )
        st.stop()


def call(task: str, messages: list,
         temperature: float = 0.3, max_tokens: int = 4096) -> str:
    client = get_client()
    model  = MODELS.get(task, "llama-3.3-70b-versatile")
    try:
        res = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        err = str(e)
        if "401"            in err: return "Invalid API key."
        if "429"            in err: return "Rate limit reached. Wait a moment."
        if "decommissioned" in err: return "Model decommissioned. Update groq_client.py."
        return f"Groq error: {err}"


def model_info(task: str) -> tuple:
    m = MODELS.get(task, "llama-3.3-70b-versatile")
    return LABELS.get(m, m), m
