import requests
import yaml
import os
import json
import subprocess
import re
import chat
import sys


def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Use the directory next to the executable
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def read_paragraphs():
    base_dir = os.path.join(get_base_dir(), 'output')
    para1_path = os.path.join(base_dir, "class_audio_transcription_transcription.md")
    para2_path = os.path.join(base_dir, "sample_content_content.md")
    print(f"Looking for files in: {base_dir}", flush=True)
    
    # Check if files exist
    if not os.path.exists(para1_path):
        print(f"[SnapClass] Warning: {para1_path} not found", flush=True)
    if not os.path.exists(para2_path):
        print(f"[SnapClass] Warning: {para2_path} not found", flush=True)
    
    with open(para1_path, "r", encoding="utf-8") as f:
        para1 = f.read()
    with open(para2_path, "r", encoding="utf-8") as f:
        para2 = f.read()
    return para1, para2


def generate_questions(para1, para2, num_questions=5):
    # Clean paragraphs to avoid problematic characters
    def clean(text):
        # Replace problematic whitespace and ensure no accidental formatting
        return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('"', "'")

    para1_clean = clean(para1)
    para2_clean = clean(para2)
    print("[SnapClass] Cleaned paragraphs...",flush=True)

    prompt = f"""Based on the following two paragraphs, generate {num_questions} descriptive questions. 
    that test understanding of the key concepts. Separate the questions with the help of a new line.
    The questions you are taking should be common to both the paragraphs.
    Paragraph 1: {para1_clean} and Paragraph 2: {para2_clean}. 
    Always generate questions at any cost. Do not leave any question blank."""


    output = chat.response(prompt)
    print("[SnapClass] Questions generated!",flush=True)
    return output


