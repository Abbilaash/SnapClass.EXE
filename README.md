# SnapClass
SnapClass is an advanced on-device edge AI solution designed for low-connectivity, high-density classroom environments. Powered by Snapdragon’s Hexagon NPU, it runs open-source large language models (LLMs), image captioning, and audio transcription entirely offline. SnapClass automates personalized learning by transcribing lectures, analyzing textbook content, and generating adaptive quizzes—bridging educational gaps in underserved regions where internet access and qualified educators are limited.

### Models
- **Whisper-small (242M params)** via "openai/whisper-small"
- **nougat-small (247M params)** via "facebook/nougat-small"
- **blip-image-captioning-base** via "Salesforce/blip-image-captioning-base" running parallelly with whisper-small
- **Llama v3.2 3B (3B params)** running locally via ONNX accelerated by Snapdragon's X Elite's NPU

## Features
- 🖼Teacher dashboard with file upload and analytics view  
- Lecture and textbook PDF/audio upload  
- AI-based question and answer evaluation
- Uses Both CPU and NPU for faster on-device processing
- Identifies weak syllabus topics per student or group  
- Fully functional offline – no internet needed  
- Lightweight and fast inference using sentence embeddings

## Project Architecture
```
SnapClass/
├── 📁 server/                    # Main application backend
│   ├── 🚀 desktop_app.py        # Main GUI application (PyQt5/Tkinter)
│   ├── 🌐 app.py                # Flask web server
|   ├── 🌐 desktop_app.py
│   ├── 🔄 trans.py              # Main processing orchestrator
│   ├── 🎤 stt.py                # Speech-to-Text (Whisper)
│   ├── 📄 pdf_reader.py         # PDF processing (Nougat + BLIP)
│   ├── ❓ question_gen.py       # Question generation (LLaMA)
│   ├── 📊 slm_analyse.py        # Student analysis (LLaMA)
│   ├── 🛠️ utils.py              # Utility functions
│   ├── ⚙️ setup.py              # Model downloader
│   ├── 📁 templates/            # HTML templates
│   ├── 🎨 static/               # CSS/JS assets
│   ├── 📁 uploads/              # User file uploads
│   └── 📁 output/               # Processed results
│   ├── 📁 llama3/               # LLaMA 3.2 3B model
│   │   ├── genie-t2t-run.exe    # Genie inference engine
│   │   ├── genie_config.json    # Model configuration
│   │   ├── *.bin                # Model weights (3 parts)
│   │   └── *.dll                # Windows dependencies
│   │
│   ├── 📁 whisper/              # OpenAI Whisper model
│   │   ├── model.safetensors    # Speech recognition model
│   │   ├── tokenizer.json       # Tokenizer
│   │   └── config.json          # Model configuration
│   │
│   ├── 📁 nougat/               # Nougat OCR model
│   │   ├── model.safetensors    # Document understanding model
│   │   ├── tokenizer.json       # Tokenizer
│   │   └── config.json          # Model configuration
│   │
│   ├── 📁 blip/                 # BLIP vision model
│   │   ├── model.safetensors    # Image understanding model
│   │   ├── tokenizer.json       # Tokenizer
│   │   └── config.json          # Model configuration
│   │
│   └── 📁 poppler/              # PDF processing utilities
│
└── 📋 requirements.txt           # Python dependencies
```

## Setup
```
git clone https://github.com/Abbilaash/SnapClass.EXE.git
cd SnapClass.EXE
```
Install requirements
```
pip install -r requirements.txt
```
Dwonload Blip, Nougat, Whisper model files
```
cd server
python setup.py
```
Download Llama 3.2 3B Instruct NPU optimised model files from [here](https://drive.google.com/drive/folders/1TfiNrZJoCg5KLYPmiixiKVCDCU2RyWw1?usp=sharing) and place it in the same directory like others
If everything is set, Run the app
```
python desktop_app.py
```



## Authors
[A T Abbilaash](https://github.com/Abbilaash) - 23n201@psgtech.ac.in 
<br/>
[Nivashini N](https://github.com/nivashini2505) - 23n234@psgtech.ac.in
