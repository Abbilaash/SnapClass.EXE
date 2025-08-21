import requests
import yaml
import os
import sys
import json
import subprocess
from argparse import Namespace
import chat
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_base_dir():
    if getattr(sys, 'frozen', False):
        # Use the directory next to the executable
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def read_paragraphs():
    base_dir = os.path.join(get_base_dir(), "output")
    para1_path = os.path.join(base_dir, "class_audio_transcription_transcription.md")
    para2_path = os.path.join(base_dir, "sample_content_content.md")
    with open(para1_path, "r", encoding="utf-8") as f:
        para1 = f.read()
    with open(para2_path, "r", encoding="utf-8") as f:
        para2 = f.read()
    return para1, para2


def read_submissions():
    """Read and organize questions and answers from test_submissions.json"""
    try:
        submissions_file = os.path.join(get_base_dir(), "test_submissions.json")
        with open(submissions_file, "r", encoding="utf-8") as f:
            submissions = json.load(f)
        
        # Get unique questions from the first submission
        questions = []
        if submissions:
            questions = [qa["question"] for qa in submissions[0]["questions_and_answers"]]
        
        # Organize answers by student
        student_answers = {}
        for submission in submissions:
            student_name = submission["student_name"]
            answers = [qa["answer"] for qa in submission["questions_and_answers"]]
            student_answers[student_name] = answers
        
        return {
            "questions": questions,
            "student_answers": student_answers
        }
    except FileNotFoundError:
        print("test_submissions.json not found")
        return {"questions": [], "student_answers": {}}
    except Exception as e:
        print(f"Error reading submissions: {str(e)}")
        return {"questions": [], "student_answers": {}}


def build_student_qa_pairs():
    """Build per-student list of (question, answer) pairs.

    Returns a list of tuples: [(student_name, [(q1, a1), (q2, a2), ...])]
    """
    submissions_path = os.path.join(get_base_dir(), "test_submissions.json")
    if not os.path.exists(submissions_path):
        return []
    try:
        with open(submissions_path, "r", encoding="utf-8") as f:
            submissions = json.load(f)
    except Exception:
        return []

    student_to_pairs = []
    for submission in submissions:
        student_name = submission.get("student_name", "Unknown")
        qa_list = submission.get("questions_and_answers", [])
        pairs = []
        for qa in qa_list:
            q = (qa.get("question") or "").strip()
            a = (qa.get("answer") or "").strip()
            pairs.append((q, a))
        student_to_pairs.append((student_name, pairs))
    return student_to_pairs


def format_student_qa_text(student_to_pairs):
    """Format per-student Q/A pairs as a readable plain-text block (not JSON)."""
    if not student_to_pairs:
        return ""
    lines = []
    for student_name, pairs in student_to_pairs:
        lines.append(f"Student: {student_name}")
        for idx, (q, a) in enumerate(pairs, start=1):
            lines.append(f"Q{idx} - {q}")
            lines.append(f"A{idx} - {a}")
        lines.append("")
    return "\n".join(lines).strip()


def sanitize_text_for_llm(text: str) -> str:
    """Remove special characters like #, *, [, ], <, > and keep clean ASCII with basic punctuation."""
    if not text:
        return ""
    # Replace disallowed characters with space
    cleaned = re.sub(r"[^A-Za-z0-9\s\.,:;!\?\-\(\)|]", " ", text)
    # Collapse multiple whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def get_analysis():
    try:
        # Build non-JSON representations of student answers
        student_to_pairs = build_student_qa_pairs()
        para1, para2 = read_paragraphs()

        if not student_to_pairs:
            print("[SnapClass] No submissions found!")
            return {
                "success": False,
                "error": "No submissions found. Analysis cannot be performed yet."
            }

        # Prepare sanitized text blocks
        student_qa_text = format_student_qa_text(student_to_pairs)
        safe_para1 = sanitize_text_for_llm(para1)
        safe_para2 = sanitize_text_for_llm(para2)
        safe_student_qa = sanitize_text_for_llm(student_qa_text)

        prompt = f"""
        You are a strict and consistent grader. Grade student answers based only on PARA2 unless information is missing.
        Return per-question grades in the format: Q number - points out of 5 - short reasoning.

        PARA1
        {safe_para1}

        PARA2
        {safe_para2}

        STUDENT QA
        {safe_student_qa}
        """

        response = chat.response(prompt)
        print(response)

        if not response:
            # Return a clear error so the UI shows the message instead of an empty analysis
            return {
                "success": False,
                "error": (
                    "AI analysis failed: Genie returned no output. "
                    f"Checked paths -> genie: {getattr(chat, 'GENIE_PATH', 'N/A')}, "
                    f"config: {getattr(chat, 'CONFIG_FILE', 'N/A')}. "
                    "Ensure the 'llama3' folder (with genie-t2t-run.exe and genie_config.json) "
                    "is next to the executable."
                ),
                "analysis": "",
                "student_qa_text": student_qa_text,
                "student_qa_array": student_to_pairs
            }

        return {
            "success": True,
            "analysis": response,
            "student_qa_text": student_qa_text,
            "student_qa_array": student_to_pairs
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


