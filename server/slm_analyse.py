import requests
import yaml
import os
import sys
import json
import subprocess
from argparse import Namespace
from llama3 import chat
import re


def get_base_dir():
    """Get the correct base directory for MSIX or dev environment."""
    if getattr(sys, 'frozen', False):  # Running as MSIX/compiled
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


def get_analysis():
    try:
        submissions_data = read_submissions()
        para1, para2 = read_paragraphs()

        if not submissions_data["questions"] or not submissions_data["student_answers"]:
            print("[SnapClass] No submissions found!")
            return {
                "success": False,
                "error": "No submissions found. Analysis cannot be performed yet."
            }

        payload = f"""
            You are a strict and consistent grader. Your ONLY task is to grade student answers based on the materials provided below. 
            You must not solve the questions yourself, give new answers, or rely on outside knowledge.  
            Your evaluation must be grounded ONLY in PARA2 unless PARA2 does not contain the needed information (see rule 2).  
            Do not output anything other than the grading results.

            [MATERIAL_START]
            <PARA1>
            {para1}
            <END_P1>

            <PARA2>
            {para2}
            <END_P2>
            [MATERIAL_END]

            GRADING RULES (follow exactly):
            1) Base your grading strictly on the facts that appear in PARA2.  
            - PARA1 exists only for background/context and must not override PARA2.  
            2) If PARA2 lacks enough information to evaluate part of an answer, state "Insufficient evidence from PARA2" for that part.  
            3) Use this rubric for each question (max 5 points):
            - Factual correctness vs. PARA2 (0-3)
            - Coverage of key ideas from PARA2 (0-1)
            - Clarity/conciseness (0-1)
            4) Partial credit is allowed only if the correct parts are explicitly supported by PARA2.  
            5) Do not copy long text from PARA2. Refer abstractly (e.g., "matches PARA2 on event details").  
            6) If the answer is in another language, evaluate by meaning, not grammar.  
            7) Never make up facts not in PARA2. If unsure, deduct points accordingly.  
            8) Grade all student answers consistently across questions.

            [QUESTIONS]
            {submissions_data["questions"]}

            [STUDENT_ANSWERS]
            {submissions_data["student_answers"]}

            Return your evaluation clearly labeled per question:
            Q#: <points>/5 - <short reasoning>
        """

        response = chat.response(payload)

        return {
            "success": True,
            "analysis": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

