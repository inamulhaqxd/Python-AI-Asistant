# modules/explain.py
# Explain Code — three levels of explanation depth

import streamlit as st
from modules import ui, groq_client

SYSTEMS = {
    "Beginner": """Explain Python code to someone with no programming background.
Use plain English, real-world analogies, and avoid jargon entirely.

Format:
## What This Does
[1-2 plain English sentences]

## Line by Line
[explain each significant line in simple terms]

## Real-World Analogy
[relate the code's behaviour to an everyday situation]

## Key Concepts
- [concept]: [plain explanation]""",

    "Intermediate": """Explain Python code to a junior developer.
Be technically accurate but clear. Explain design choices.

Format:
## Overview
[technical summary of purpose and approach]

## Section by Section
[break down each function, class, or block]

## Design Decisions
[why certain approaches were chosen over alternatives]

## Potential Issues
[edge cases, risks, or areas to improve]""",

    "Advanced": """Perform a deep technical analysis of Python code.

Format:
## Technical Summary
[architecture, purpose, and high-level approach]

## Deep Analysis
[algorithms, data structures, and patterns used]

## Complexity
- Time: [Big-O]
- Space: [Big-O]

## Pythonic Assessment
[how idiomatic is the code, what violates or follows Python conventions]

## Optimization Opportunities
[concrete improvements with brief code examples where relevant]""",
}


def render():
    label, model_id = groq_client.model_info("explain")
    ui.page_header("Explain Code", "Submit any Python code and receive a structured explanation.")
    ui.model_tag(label, model_id)

    level = st.radio("Explanation Depth", list(SYSTEMS.keys()),
                     horizontal=True, key="exp_level")

    code = st.text_area("Python Code", height=260,
                         placeholder="Paste the code you want explained.",
                         key="exp_code")

    question = st.text_input(
        "Specific Question (optional)",
        placeholder="e.g. Why is a generator used here instead of a list?",
        key="exp_q"
    )

    view = st.radio("Layout", ["Single column", "Side by side"],
                    horizontal=True, key="exp_view")

    if st.button("Explain", type="primary", key="exp_btn"):
        if not code.strip():
            st.warning("Paste your code first.")
            return
        msg = f"Explain this Python code:\n\n```python\n{code}\n```"
        if question.strip():
            msg += f"\n\nSpecific question: {question}"
        with st.spinner("Analyzing..."):
            result = groq_client.call("explain", [
                {"role": "system", "content": SYSTEMS[level]},
                {"role": "user",   "content": msg}
            ], temperature=0.3)
            st.session_state["explain_result"] = result
            st.session_state["explain_code"]   = code

    if "explain_result" in st.session_state:
        ui.divider()
        if view == "Side by side":
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Code")
                st.code(st.session_state.get("explain_code", ""),
                        language="python")
            with c2:
                st.markdown("#### Explanation")
                st.markdown(st.session_state["explain_result"])
        else:
            st.markdown("### Explanation")
            st.markdown(st.session_state["explain_result"])

        if st.button("Clear", key="exp_clr"):
            del st.session_state["explain_result"]
            st.rerun()
