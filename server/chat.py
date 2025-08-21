
import os
import sys
import subprocess
import re


def _get_candidate_base_dirs():
    base_dirs = []
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            base_dirs.append(sys._MEIPASS)
        base_dirs.append(os.path.dirname(sys.executable))
    base_dirs.append(os.path.dirname(os.path.abspath(__file__)))
    return base_dirs


def _get_llama3_dir():
    for base in _get_candidate_base_dirs():
        candidate = os.path.join(base, 'llama3')
        if os.path.isdir(candidate):
            return candidate
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'llama3')


LLAMA3_DIR = _get_llama3_dir()
GENIE_PATH = os.path.join(LLAMA3_DIR, 'genie-t2t-run.exe')
CONFIG_FILE = os.path.join(LLAMA3_DIR, 'genie_config.json')


def _run_genie(prompt: str):
    if not os.path.isfile(GENIE_PATH):
        print(f"[SnapClass] Genie executable not found at: {GENIE_PATH}", flush=True)
        return None
    if not os.path.isfile(CONFIG_FILE):
        print(f"[SnapClass] Genie config not found at: {CONFIG_FILE}", flush=True)
        return None

    result = subprocess.run(
        [GENIE_PATH, '-c', CONFIG_FILE, '-p', prompt],
        cwd=LLAMA3_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print("[SnapClass] Error running Genie:", flush=True)
        print(result.stderr, flush=True)
        return None

    output_text = result.stdout.strip()
    match = re.search(r'\[BEGIN\s*\]:([\s\S]*?)\[END\]', output_text)
    if match:
        return match.group(1).strip()
    # Fallback: return entire stdout if markers not found
    if output_text:
        print("[SnapClass] Genie output did not include [BEGIN]/[END] markers; returning full stdout.", flush=True)
        return output_text
    return None


def response(prompt):
    wrapped = (
        f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt} <|eot_id|><|start_header_id|>assistant<|end_header_id|>"
    )
    return _run_genie(wrapped)


