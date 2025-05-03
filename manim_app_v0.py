# -*- coding: utf-8 -*-
"""
Created on Sat May  3 08:12:43 2025

@author: vivek
"""

import streamlit as st
import tempfile
import os
import json
from datetime import datetime

# Initialize session
session_time = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
context_file = f"session_{session_time}_context.json"
attempt_history = []
output_dir = "manimind_outputs"
os.makedirs(output_dir, exist_ok=True)

def save_attempt_history():
    with open(context_file, "w") as f:
        json.dump(attempt_history, f, indent=2)

def generate_manim_code_from_text(prompt: str) -> str:
    return f"# Placeholder Manim code for prompt:\n# {prompt}\n\nfrom manim import *\n\nclass MyScene(Scene):\n    def construct(self):\n        text = Text('This is a placeholder')\n        self.play(Write(text))\n        self.wait()"

# --- Streamlit Interface ---
st.title("🧠 Manimind")
st.markdown("Generate Manim animations from text or textbook images. (Rendering disabled for now)")

input_mode = st.radio("Input Type", ["Text", "Image"])
text_input, image_input = "", None

if input_mode == "Text":
    text_input = st.text_area("Describe your animation")
else:
    image_input = st.file_uploader("Upload a textbook snippet image", type=["png", "jpg", "jpeg"])

if st.button("Generate Animation"):
    for attempt in range(10):
        if input_mode == "Text":
            code = generate_manim_code_from_text(text_input)
        elif image_input:
            code = "# Placeholder: image-to-code not supported yet."
        else:
            st.error("Please provide input before generating.")
            break

        attempt_history.append({
            "attempt": attempt + 1,
            "input_type": input_mode,
            "user_input": text_input if input_mode == "Text" else "<image>",
            "generated_code": code,
            "error": None  # placeholder; no rendering yet
        })
        save_attempt_history()

        st.success(f"✅ Code generated (attempt {attempt + 1}, no rendering)")
        st.code(code, language="python")
        break
    else:
        st.error("❌ All 10 attempts failed.")
