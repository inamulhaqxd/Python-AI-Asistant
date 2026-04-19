# modules/convert.py
# Convert Code — language translation and style modernisation

import streamlit as st
from modules import ui, groq_client

SYSTEM = """You are an expert in multiple programming languages.
Convert the submitted code exactly, preserving all logic and behaviour.
Use idiomatic patterns of the target language.

Format:

## Converted Code
```[language]
[complete converted code]
```

## Conversion Notes
- **[Change]:** [reason it differs in the target language]

## Key Differences
[behavioural or syntactic differences the developer should be aware of]

Produce complete, runnable output only."""

CONVERSIONS = {
    "Python 2 to Python 3":           ("Python 2",     "Python 3",     "py"),
    "Python to JavaScript":            ("Python",       "JavaScript",   "js"),
    "JavaScript to Python":            ("JavaScript",   "Python",       "py"),
    "Python to Java":                  ("Python",       "Java",         "java"),
    "Python to TypeScript":            ("Python",       "TypeScript",   "ts"),
    "Python to Rust":                  ("Python",       "Rust",         "rs"),
    "Script to OOP classes":           ("Script",       "OOP Classes",  "py"),
    "Synchronous to async/await":      ("Sync Python",  "Async Python", "py"),
    "Functions to FastAPI endpoints":  ("Functions",    "FastAPI",      "py"),
}


def render():
    label, model_id = groq_client.model_info("convert")
    ui.page_header("Convert Code",
                   "Translate between languages or modernise your Python code.")
    ui.model_tag(label, model_id)

    conv_name = st.selectbox("Conversion", list(CONVERSIONS.keys()),
                              key="conv_type")
    src, tgt, ext = CONVERSIONS[conv_name]
    st.caption(f"Source: {src}   →   Target: {tgt}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{src} — Input**")
        code = st.text_area("Source code", height=300, key="conv_code",
                             label_visibility="collapsed",
                             placeholder=f"Paste your {src} code here.")
    with c2:
        st.markdown(f"**{tgt} — Output**")
        if "conv_code_out" in st.session_state:
            st.code(st.session_state["conv_code_out"],
                    language=tgt.lower().split()[0])
        else:
            st.markdown(
                "<div style='height:280px; background:#f9fafb; "
                "border:1px solid #e5e7eb; border-radius:6px; "
                "display:flex; align-items:center; justify-content:center; "
                "color:#9ca3af; font-size:0.85em;'>"
                "Output appears here after conversion."
                "</div>",
                unsafe_allow_html=True
            )

    col_a, col_b = st.columns(2)
    with col_a:
        comments = st.checkbox("Add inline comments explaining changes", value=True,
                               key="conv_cmts")
    with col_b:
        structure = st.checkbox("Preserve original structure", value=True,
                                key="conv_str")

    if st.button("Convert", type="primary", use_container_width=True,
                 key="conv_btn"):
        if not code.strip():
            st.warning(f"Paste your {src} code first.")
            return
        msg = (f"Convert this {src} code to {tgt}.\n"
               f"Inline comments: {'Yes' if comments else 'No'}\n"
               f"Preserve structure: {'Yes' if structure else 'No'}\n\n"
               f"```\n{code}\n```\n\nReturn complete, runnable {tgt} code.")
        with st.spinner(f"Converting to {tgt}..."):
            result = groq_client.call("convert", [
                {"role": "system", "content": SYSTEM},
                {"role": "user",   "content": msg}
            ], temperature=0.2)
            st.session_state["convert_result"] = result
            if "```" in result:
                try:
                    block = result.split("```")[1]
                    lines = block.split("\n")
                    if lines[0].strip().isalpha():
                        block = "\n".join(lines[1:])
                    st.session_state["conv_code_out"] = block.strip()
                except Exception:
                    st.session_state["conv_code_out"] = result
            st.rerun()

    if "convert_result" in st.session_state:
        ui.divider()
        st.markdown("### Conversion Report")
        st.markdown(st.session_state["convert_result"])
        c1, c2 = st.columns([1, 5])
        with c1:
            if "conv_code_out" in st.session_state:
                st.download_button(
                    f"Download .{ext}",
                    data=st.session_state["conv_code_out"],
                    file_name=f"converted.{ext}",
                    mime="text/plain"
                )
        with c2:
            if st.button("Clear", key="conv_clr"):
                for k in ["convert_result", "conv_code_out"]:
                    st.session_state.pop(k, None)
                st.rerun()
