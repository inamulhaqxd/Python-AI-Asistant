# modules/improve.py
# Improve Code — rewrites code to a higher standard

import streamlit as st
from modules import ui, groq_client

SYSTEM = """You are a senior Python engineer conducting a code review.

Rewrite the submitted code with all improvements applied.

Response format:

## Assessment
[3-4 sentences: what the code does well, what needs improvement]

## Improved Code
```python
[complete rewritten code]
```

## Improvements Made
- **[Area]:** [what changed and why]
(list every change)

## Before vs After
| Aspect       | Before | After |
|--------------|--------|-------|
| Readability  | [x/10] | [x/10] |
| Performance  | [assessment] | [assessment] |
| Best Practice| [assessment] | [assessment] |"""

FOCUS = [
    "Full review",
    "Performance",
    "Readability and PEP 8",
    "Error handling",
    "Documentation",
    "Object-oriented structure",
]


def render():
    label, model_id = groq_client.model_info("improve")
    ui.page_header("Improve Code", "Submit working code and receive a professionally rewritten version.")
    ui.model_tag(label, model_id)

    code = st.text_area("Python Code", height=260,
                         placeholder="Paste the code you want improved.",
                         key="imp_code")

    c1, c2 = st.columns(2)
    with c1:
        focus = st.selectbox("Focus", FOCUS, key="imp_focus")
    with c2:
        level = st.selectbox("Your Level",
                             ["Beginner", "Intermediate", "Advanced"],
                             index=1, key="imp_level")

    if st.button("Improve Code", type="primary", key="imp_btn"):
        if not code.strip():
            st.warning("Paste your code first.")
            return
        prompt = (f"Improve this Python code.\n"
                  f"Focus: {focus}\n"
                  f"Audience level: {level}\n\n"
                  f"```python\n{code}\n```\n\n"
                  f"Return the fully rewritten version with all changes explained.")
        with st.spinner("Rewriting..."):
            result = groq_client.call("improve", [
                {"role": "system", "content": SYSTEM},
                {"role": "user",   "content": prompt}
            ], temperature=0.3)
            st.session_state["improve_result"] = result

    if "improve_result" in st.session_state:
        ui.divider()
        st.markdown("### Improvement Report")
        st.markdown(st.session_state["improve_result"])
        c1, c2 = st.columns([1, 5])
        with c1:
            ui.download_code(st.session_state["improve_result"], "improved.py")
        with c2:
            if st.button("Clear", key="imp_clr"):
                del st.session_state["improve_result"]
                st.rerun()
