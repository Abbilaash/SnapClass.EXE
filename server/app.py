from flask import Flask, render_template, request, redirect, url_for, jsonify
import socket
import os
from werkzeug.utils import secure_filename
from trans import process_files
import question_gen
import utils
import json
import slm_analyse
import subprocess
import signal
import sys
import threading
from datetime import datetime

app = Flask(__name__)

def get_base_dir():
    """Get the correct base directory for MSIX or dev environment."""
    if getattr(sys, 'frozen', False):  # Running as MSIX/compiled
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

# Get the correct base directory
BASE_DIR = get_base_dir()

# Use os.path.join for proper path handling
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Define file paths
PUBLISHED_TEST_FILE = os.path.join(BASE_DIR, "published_test.json")
TEST_SUBMISSIONS_FILE = os.path.join(BASE_DIR, "test_submissions.json")
GENERATED_QUESTIONS_FILE = os.path.join(BASE_DIR, "generated_questions.json")

if os.environ.get('SNAPCLASS_LAUNCHED_BY_DESKTOP') != '1':
    print('Please start the server from the SnapClass desktop app.')
    exit(1)

def handle_sigterm(*args):
    print("[SnapClass] Server is shutting down.", flush=True)
    print("Received SIGTERM, exiting Flask server.", flush=True)
    os._exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)

# Combined Admin Dashboard
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        # Handle file uploads
        if 'pdf' in request.files and 'audio' in request.files:
            pdf = request.files['pdf']
            audio = request.files['audio']  
            
            if pdf.filename != '' and audio.filename != '':
                # Save files with fixed names
                pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_content.md')
                audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'class_audio_transcription.md')
                
                pdf.save(pdf_path)
                audio.save(audio_path)
                
                # Before processing files in the /admin route
                output_dir = os.path.join(BASE_DIR, "output")
                transcript_files = [
                    os.path.join(output_dir, "sample_content.md"),
                    os.path.join(output_dir, "class_audio_transcription.md"),
                ]

                for file_path in transcript_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)

                try:
                    # Process files in parallel
                    updates = []
                    def status_callback(update):
                        updates.append(update)
                    
                    audio_output, pdf_output = process_files(
                        audio_path,
                        pdf_path,
                        status_callback=status_callback
                    )

                    # Read the output files' content
                    audio_text = ""
                    pdf_text = ""
                    try:
                        with open(audio_output, "r", encoding="utf-8") as f:
                            audio_text = f.read()
                    except Exception:
                        audio_text = "Could not read audio transcription output."

                    try:
                        with open(pdf_output, "r", encoding="utf-8") as f:
                            pdf_text = f.read()
                    except Exception:
                        pdf_text = "Could not read PDF extraction output."

                    return jsonify({
                        'success': True,
                        'message': 'Files processed successfully',
                        'updates': updates,
                        'audio_output': audio_output,
                        'pdf_output': pdf_output,
                        'audio_text': audio_text,
                        'pdf_text': pdf_text
                    })
                except Exception as e:
                    return jsonify({
                        'success': False,
                        'message': f'Error processing files: {str(e)}'
                    })
        
        # Handle question submission
        question = request.form.get("question")
        if question:
            options = [request.form.get(f"option{i}") for i in range(1, 5)]
            answer = request.form.get("answer")
            utils.save_question(question, options, answer)
            return redirect(url_for("admin"))

    # Load data for display
    questions = utils.load_questions()
    student_data = utils.load_student_analysis()
    return render_template("admin.html", questions=questions, data=student_data)

# Student Test Page
@app.route("/")
def test():
    questions = []
    test_available = False
    
    # Check if questions are published (only show if published)
    if os.path.exists(GENERATED_QUESTIONS_FILE):
        try:
            with open(GENERATED_QUESTIONS_FILE, "r", encoding="utf-8") as f:
                generated_data = json.load(f)
            if generated_data.get("status") == "published" and os.path.exists(PUBLISHED_TEST_FILE):
                with open(PUBLISHED_TEST_FILE, "r", encoding="utf-8") as f:
                    questions = json.load(f)
                test_available = True
        except Exception as e:
            print(f"Error reading generated questions: {e}")
    
    # Print connection info
    try:
        ip = request.remote_addr
        print(f"[SnapClass] New device connected from {ip}", flush=True)
        # Print number of devices
        if os.path.exists(TEST_SUBMISSIONS_FILE):
            with open(TEST_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                submissions = json.load(f)
            print(f"[SnapClass] Current number of devices (submissions): {len(submissions)}", flush=True)
        else:
            print(f"[SnapClass] Current number of devices (submissions): 0", flush=True)
    except Exception as e:
        print(f"[SnapClass] Error printing connection info: {e}", flush=True)
    
    return render_template("test.html", questions=questions, test_available=test_available)

# Submit Test
@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    answers = data.get("answers")
    name = data.get("name")
    # Get questions from published test
    questions = []
    if os.path.exists(PUBLISHED_TEST_FILE):
        with open(PUBLISHED_TEST_FILE, "r", encoding="utf-8") as f:
            questions = json.load(f)
    # Save the submission
    utils.save_test_submission(name, questions, answers)
    # Print number of devices after submission
    try:
        if os.path.exists(TEST_SUBMISSIONS_FILE):
            with open(TEST_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                submissions = json.load(f)
            print(f"[SnapClass] Submission received from {name}. Total devices: {len(submissions)}", flush=True)
        else:
            print(f"[SnapClass] Submission received from {name}. Total devices: 1", flush=True)
    except Exception as e:
        print(f"[SnapClass] Error printing submission info: {e}", flush=True)
    # Calculate and save result
    result = utils.evaluate(answers)
    if name:
        utils.save_student_result(name, result["score"], result["total"])
    return jsonify(result)

@app.route("/generate_ques", methods=["POST"])
def generate_ques():
    try:
        print("Generating questions...")
        para1, para2 = question_gen.read_paragraphs()
        questions = question_gen.generate_questions(para1, para2)
        questions = questions.split("\n")
        q = []
        for i in questions:
            if i!="":
                q.append(i)
        q = q[1:]
        questions = q 

        # Save generated questions with timestamp
        generated_data = {
            "questions": questions,
            "generated_date": datetime.now().isoformat(),
            "status": "generated"  # not yet published
        }
        
        with open(GENERATED_QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(generated_data, f, indent=2)
        
        print("[SnapClass] Test questions generated successfully!",flush=True)
        return jsonify({"success": True, "questions": questions, "message": "Questions generated and saved"})
    except Exception as e:
        print(f"Error generating questions: {e}")
        return jsonify({"success": False, "message": str(e)})

@app.route("/publish_test", methods=["POST"])
def publish_test():
    try:
        # Check if generated questions exist
        if not os.path.exists(GENERATED_QUESTIONS_FILE):
            return jsonify({"success": False, "message": "No generated questions found. Please generate questions first."})
        
        # Read the generated questions
        with open(GENERATED_QUESTIONS_FILE, "r", encoding="utf-8") as f:
            generated_data = json.load(f)
        
        # Update status to published
        generated_data["status"] = "published"
        generated_data["published_date"] = datetime.now().isoformat()
        
        # Save updated generated questions
        with open(GENERATED_QUESTIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(generated_data, f, indent=2)
        
        # Publish the questions to the test file (accessible by students)
        with open(PUBLISHED_TEST_FILE, "w", encoding="utf-8") as f:
            json.dump(generated_data["questions"], f)
        
        print("[SnapClass] Test published successfully!",flush=True)
        return jsonify({"success": True, "message": "Test published successfully"})
    except Exception as e:
        print(f"Error publishing test: {e}",flush=True)
        return jsonify({"success": False, "message": str(e)})


@app.route("/get_generated_questions_status", methods=["GET"])
def get_generated_questions_status():
    try:
        if os.path.exists(GENERATED_QUESTIONS_FILE):
            with open(GENERATED_QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return jsonify({
                "success": True,
                "exists": True,
                "status": data.get("status", "unknown"),
                "generated_date": data.get("generated_date"),
                "published_date": data.get("published_date")
            })
        else:
            return jsonify({
                "success": True,
                "exists": False,
                "status": "not_generated"
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/clear_all_data", methods=["POST"])
def clear_all_data():
    """Clear all previous data: test questions, output files, analysis, and submissions"""
    try:
        files_to_delete = []
        
        # Add generated questions file
        if os.path.exists(GENERATED_QUESTIONS_FILE):
            files_to_delete.append(GENERATED_QUESTIONS_FILE)
        
        # Add published test file
        if os.path.exists(PUBLISHED_TEST_FILE):
            files_to_delete.append(PUBLISHED_TEST_FILE)
        
        # Add test submissions file
        if os.path.exists(TEST_SUBMISSIONS_FILE):
            files_to_delete.append(TEST_SUBMISSIONS_FILE)
        
        # Add student results file (if exists)
        student_results_file = os.path.join(BASE_DIR, "student_analysis.json")
        if os.path.exists(student_results_file):
            files_to_delete.append(student_results_file)
        
        # Clear output folder files
        output_dir = os.path.join(BASE_DIR, "output")
        if os.path.exists(output_dir):
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                if os.path.isfile(file_path):
                    files_to_delete.append(file_path)
        
        # Clear uploads folder files
        uploads_dir = os.path.join(BASE_DIR, "uploads")
        if os.path.exists(uploads_dir):
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                if os.path.isfile(file_path):
                    files_to_delete.append(file_path)
        
        # Delete all files
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        
        print("[SnapClass] Previous records cleared successfully!",flush=True)
        
        return jsonify({
            "success": True,
            "message": f"Successfully cleared {deleted_count} files",
            "deleted_count": deleted_count
        })
        
    except Exception as e:
        print(f"Error clearing data: {e}")
        return jsonify({
            "success": False,
            "message": f"Error clearing data: {str(e)}"
        })

@app.route("/analyse", methods=["GET"])
def analyse():
    try:
        analysis_result = slm_analyse.get_analysis()
        
        if not analysis_result["success"]:
            return render_template("analysis.html", error=analysis_result["error"], data=analysis_result)
        
        # Read the test submissions for display
        submissions = []
        if os.path.exists(utils.TEST_SUBMISSIONS_FILE):
            with open(utils.TEST_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                submissions = json.load(f)
        
        # Format the data for display
        analysis_data = {
            "total_submissions": len(submissions),
            "submissions": submissions,
            "ai_analysis": analysis_result["analysis"]
        }
        
        return render_template("analysis.html", data=analysis_data)
    except Exception as e:
        return render_template("analysis.html", error=str(e))




def stop(self):
    if self.process and self.process.poll() is None:
        self.process.terminate()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.kill()
        self.running = False

def run_server():
    ip = socket.gethostbyname(socket.gethostname())
    print(f"[SnapClass] Server running at http://{ip}:5000", flush=True)
    print(f"[SnapClass] Public test URL: http://{ip}:5000", flush=True)
    print("[SnapClass] Server started!", flush=True)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()