import os
import sys
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, AutoModelForVision2Seq
from transformers import AutoTokenizer, AutoModelForVision2Seq

def get_base_dir():
    if getattr(sys, 'frozen', False):  # Running as MSIX/compiled
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

WHISPER_MODEL_NAME = "openai/whisper-small"
WHISPER_FOLDER_NAME = "whisper"

NOUGAT_MODEL_NAME = "facebook/nougat-small"
NOUGAT_FOLDER_NAME = "nougat"

BLIP_MODEL_NAME = "Salesforce/blip-image-captioning-base"
BLIP_FOLDER_NAME = "blip"

def whisper_setup_model():
    base_dir = get_base_dir()
    model_dir = os.path.join(base_dir, WHISPER_FOLDER_NAME)
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        print(f"[SNAPCLASS SETUP] Model already exists in: {model_dir}")
        return
    print(f"[SNAPCLASS SETUP] Downloading whisper model '{WHISPER_MODEL_NAME}' to '{model_dir}' ...")
    os.makedirs(model_dir, exist_ok=True)
    # Download and save model + processor
    processor = AutoProcessor.from_pretrained(WHISPER_MODEL_NAME)
    processor.save_pretrained(model_dir)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(WHISPER_MODEL_NAME)
    model.save_pretrained(model_dir)
    print(f"[SNAPCLASS SETUP] Whisper model downloaded and saved to: {model_dir}")

def setup_nougat_model():
    base_dir = get_base_dir()
    model_dir = os.path.join(base_dir, NOUGAT_FOLDER_NAME)
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        print(f"[SNAPCLASS SETUP] Model already exists in: {model_dir}")
        return
    print(f"[SNAPCLASS SETUP] Downloading nougat model '{NOUGAT_MODEL_NAME}' to '{model_dir}' ...")
    os.makedirs(model_dir, exist_ok=True)
    # Download and save model + processor
    processor = AutoProcessor.from_pretrained(NOUGAT_MODEL_NAME)
    processor.save_pretrained(model_dir)
    model = AutoModelForVision2Seq.from_pretrained(NOUGAT_MODEL_NAME)
    model.save_pretrained(model_dir)
    print(f"[SNAPCLASS SETUP] Nougat model downloaded and saved to: {model_dir}")

def setup_blip_model():
    base_dir = get_base_dir()
    model_dir = os.path.join(base_dir, BLIP_FOLDER_NAME)
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        print(f"[SNAPCLASS SETUP] Model already exists in: {model_dir}")
        return
    print(f"[SNAPCLASS SETUP] Downloading blip image captioning model '{BLIP_MODEL_NAME}' to '{model_dir}' ...")
    os.makedirs(model_dir, exist_ok=True)
    # Download and save model + processor
    processor = AutoProcessor.from_pretrained(BLIP_MODEL_NAME)
    processor.save_pretrained(model_dir)
    model = AutoModelForVision2Seq.from_pretrained(BLIP_MODEL_NAME)
    model.save_pretrained(model_dir)
    print(f"[SNAPCLASS SETUP] Blip image captioning model downloaded and saved to: {model_dir}")


if __name__ == "__main__":
    whisper_setup_model()
    setup_nougat_model()
    setup_blip_model()
