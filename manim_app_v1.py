# -*- coding: utf-8 -*-
"""
Created on Sat May  3 08:20:59 2025

@author: vivek
"""

import streamlit as st
import tempfile
import os
import json
import subprocess
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
    return f"""# Placeholder Manim code for prompt: {prompt}

from manim import *

class MyScene(Scene):
    def construct(self):
        text = Text("This is a placeholder animation")
        self.play(Write(text))
        self.wait()
"""

def render_manim_scene(script_path: str) -> tuple:
    try:
        result = subprocess.run(
            [
                "manim",
                "-ql",
                script_path,
                "MyScene"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30
        )

        return result.returncode == 0, result.stderr.decode()
    except Exception as e:
        return False, str(e)

# --- Streamlit Interface ---
st.title("🧠 Manimind")
st.markdown("Generate Manim animations from text or textbook images. (Video now rendered and shown below!)")

input_mode = st.radio("Input Type", ["Text", "Image"])
text_input, image_input = "", None

if input_mode == "Text":
    text_input = st.text_area("Describe your animation")
else:
    image_input = st.file_uploader("Upload a textbook snippet image", type=["png", "jpg", "jpeg"])

if st.button("Generate Animation"):
    if input_mode == "Text":
        code = generate_manim_code_from_text(text_input)
    elif image_input:
        code = "# Placeholder: image-to-code not supported yet."
    else:
        st.error("Please provide input before generating.")

    # Save code to a .py file
    script_path = os.path.join(output_dir, f"MyScene_{session_time}.py")
    with open(script_path, "w") as f:
        f.write(code)

    success, error = render_manim_scene(script_path)

    attempt_history.append({
        "attempt": 1,
        "input_type": input_mode,
        "user_input": text_input if input_mode == "Text" else "<image>",
        "generated_code": code,
        "error": error if not success else None
    })
    save_attempt_history()

    if success:
        st.success("✅ Code rendered successfully!")

        # Hardcoded video path based on known Manim behavior
        video_path = f"media/videos/MyScene_{session_time}/480p15/MyScene.mp4"
        if os.path.exists(video_path):
            st.video(video_path)
        else:
            st.warning("Video file not found at expected location.")

    else:
        st.error("❌ Manim render failed.")
        st.text(error)
