# modules/generate.py
# Generate Code — clarifying questions then complete generation

import streamlit as st
from modules import ui, groq_client

Q_SYSTEM = """You are a Python developer scoping a project.
Ask exactly 3 short, specific clarifying questions based on what the user wants to build.
Return only the 3 questions, numbered 1. 2. 3. — no other text."""

GEN_SYSTEM = """You are a senior Python developer.
Generate complete, production-ready code based on the requirements provided.

Response format:

## Generated Code
```python
[complete working code with inline comments]
```

## How It Works
[step-by-step explanation, clear and concise]

## How to Run
```bash
[installation and execution commands]
```

## Customization
- [how to extend or modify the code]

Requirements: include all imports, docstrings, type hints, and error handling."""


def render():
    label, model_id = groq_client.model_info("generate")
    ui.page_header("Generate Code",
                   "Describe what you need. Answer three clarifying questions. Receive complete code.")
    ui.model_tag(label, model_id)

    prompt = st.text_area(
        "What do you want to build?",
        height=110,
        placeholder=(
            "Examples:\n"
            "  A REST API for a task management system using FastAPI\n"
            "  A script that scrapes product prices and exports to CSV\n"
            "  A command-line tool to batch-resize images"
        ),
        key="gen_prompt"
    )

    c1, c2 = st.columns(2)
    with c1:
        complexity = st.select_slider(
            "Complexity",
            ["Simple", "Intermediate", "Advanced"],
            value="Intermediate",
            key="gen_cx"
        )
    with c2:
        tests = st.checkbox("Include unit tests", key="gen_tests")

    if st.button("Get Clarifying Questions", type="secondary",
                 use_container_width=True, key="gen_q"):
        if not prompt.strip():
            st.warning("Describe what you want to build first.")
            return
        with st.spinner("Generating questions..."):
            raw = groq_client.call("generate", [
                {"role": "system", "content": Q_SYSTEM},
                {"role": "user",   "content": f"User wants to build: {prompt}"}
            ], temperature=0.4, max_tokens=200)
            lines = [l.strip() for l in raw.split("\n")
                     if l.strip() and l.strip()[0].isdigit()]
            qs = [l.split(". ", 1)[-1] for l in lines[:3]]
            if not qs:
                qs = ["What is the primary use case?",
                      "Are there specific libraries or frameworks required?",
                      "Should error handling and logging be included?"]
            st.session_state["gen_qs"]     = qs
            st.session_state["gen_saved"]  = prompt
            st.session_state.pop("gen_result", None)

    if "gen_qs" in st.session_state:
        ui.divider()
        st.markdown("### Clarifying Questions")
        answers = []
        for i, q in enumerate(st.session_state["gen_qs"]):
            st.markdown(
                f'<div class="q-card"><strong>Q{i+1}:</strong> {q}</div>',
                unsafe_allow_html=True
            )
            a = st.text_input(f"Answer {i+1}", key=f"gen_a{i}",
                              placeholder="Your answer...")
            answers.append(a)

        if st.button("Generate Code", type="primary",
                     use_container_width=True, key="gen_go"):
            qa = "\n".join([
                f"Q: {st.session_state['gen_qs'][i]}\nA: {answers[i]}"
                for i in range(len(answers))
            ])
            msg = (f"Build: {st.session_state['gen_saved']}\n"
                   f"Complexity: {complexity}\n"
                   f"Include tests: {'Yes' if tests else 'No'}\n\n"
                   f"Answers to clarifying questions:\n{qa}\n\n"
                   f"Generate complete, working Python code.")
            with st.spinner("Generating..."):
                result = groq_client.call("generate", [
                    {"role": "system", "content": GEN_SYSTEM},
                    {"role": "user",   "content": msg}
                ], temperature=0.4)
                st.session_state["gen_result"] = result

    ui.divider()
    if st.button("Generate Directly", type="secondary",
                 use_container_width=True, key="gen_direct"):
        if not prompt.strip():
            st.warning("Describe what you want to build first.")
            return
        msg = (f"Build: {prompt}\n"
               f"Complexity: {complexity}\n"
               f"Include tests: {'Yes' if tests else 'No'}\n"
               f"Generate complete Python code.")
        with st.spinner("Generating..."):
            result = groq_client.call("generate", [
                {"role": "system", "content": GEN_SYSTEM},
                {"role": "user",   "content": msg}
            ], temperature=0.4)
            st.session_state["gen_result"] = result

    if "gen_result" in st.session_state:
        ui.divider()
        st.markdown("### Generated Code")
        st.markdown(st.session_state["gen_result"])
        c1, c2, c3 = st.columns([1, 1, 4])
        with c1:
            ui.download_code(st.session_state["gen_result"], "generated.py")
        with c2:
            if st.button("Regenerate", key="gen_regen"):
                del st.session_state["gen_result"]
                st.rerun()
        with c3:
            if st.button("Clear", key="gen_clr"):
                for k in ["gen_result", "gen_qs", "gen_saved"]:
                    st.session_state.pop(k, None)
                st.rerun()
