# modules/fix.py
# Fix Error — analyzes and repairs broken Python code

import streamlit as st
from modules import ui, groq_client

SYSTEM = """You are a senior Python engineer specializing in debugging.

Given broken Python code and an error message:
1. Identify what is wrong and why, in clear plain language.
2. Provide the complete fixed code.
3. List every change made as bullet points.
4. Add one practical tip to prevent this class of error.

Response format:

## Error Analysis
[clear explanation of what went wrong and why]

## Fixed Code
```python
[complete corrected code]
```

## Changes Made
- [change — reason]

## Tip
[one concrete preventive tip]"""


def render():
    label, model_id = groq_client.model_info("fix")
    ui.page_header("Fix Error", "Paste broken code and the error message. Get a full debug report.")
    ui.model_tag(label, model_id)

    col1, col2 = st.columns([1, 1])
    with col1:
        code = st.text_area("Python Code", height=240,
                            placeholder="Paste your code here.",
                            key="fix_code")
    with col2:
        error = st.text_area("Error / Traceback", height=140,
                             placeholder="Paste the full error or traceback.",
                             key="fix_err")
        context = st.text_area("Context (optional)", height=80,
                               placeholder="Describe what this code is supposed to do.",
                               key="fix_ctx")

    if st.button("Analyze and Fix", type="primary", key="fix_btn"):
        if not code.strip():
            st.warning("Paste your code first.")
            return
        prompt = f"Fix this Python code:\n\n```python\n{code}\n```"
        if error.strip():
            prompt += f"\n\nError:\n```\n{error}\n```"
        if context.strip():
            prompt += f"\n\nContext: {context}"

        with st.spinner("Analyzing..."):
            result = groq_client.call("fix", [
                {"role": "system", "content": SYSTEM},
                {"role": "user",   "content": prompt}
            ], temperature=0.2)
            st.session_state["fix_result"] = result

    if "fix_result" in st.session_state:
        ui.divider()
        st.markdown("### Debug Report")
        st.markdown(st.session_state["fix_result"])
        c1, c2 = st.columns([1, 5])
        with c1:
            ui.download_code(st.session_state["fix_result"], "fixed.py")
        with c2:
            if st.button("Clear", key="fix_clr"):
                del st.session_state["fix_result"]
                st.rerun()
