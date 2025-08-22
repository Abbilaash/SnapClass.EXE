# 🎓 SnapClass.AI - AI-Powered Educational Assistant

SnapClass.AI is a fully Offline intelligent educational platform that combines multiple AI models to process, analyze, and generate educational content from various input sources including audio, PDFs, and text.

## 🏗️ Project Architecture

```
SnapClass/
├── 📁 server/                    # Main application backend
│   ├── 🚀 desktop_app.py        # Main GUI application (PyQt5/Tkinter)
│   ├── 🌐 app.py                # Flask web server
|   ├── 🌐 desktop_app.py
|   ├── 🌐 chat.py
│   ├── 🔄 trans.py              # Main processing orchestrator
│   ├── 🎤 stt.py                # Speech-to-Text (Whisper)
│   ├── 📄 pdf_reader.py         # PDF processing (Nougat + BLIP)
│   ├── ❓ question_gen.py        # Question generation (LLaMA)
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
│   └── 📁 poppler/              # PDF processing utilities
│
└── 📋 requirements.txt           # Python dependencies
```

## 🚀 Key Features

### 🎯 **Multi-Modal AI Processing**
- **Audio Processing**: Speech-to-text conversion using Whisper
- **Document Processing**: PDF text extraction module
- **Text Generation**: Question generation and analysis using LLaMA 3.2

### 🖥️ **Dual Interface**
- **Desktop Application**: Native GUI built with customtkinter
- **Web Interface**: Flask-based web server with React frontend

### 🔄 **Workflow Pipeline**
1. **Input Processing**: Audio files, PDFs, or text input
2. **AI Analysis**: Multi-model AI processing pipeline
3. **Content Generation**: Questions, summaries, and insights
4. **Output Delivery**: Structured results via GUI or web interface

## 🛠️ Technology Stack

### **Backend (Python)**
- **Framework**: Flask (web server)
- **GUI**: customtkinter (desktop app)
- **AI/ML**: PyTorch, Transformers, Whisper, Llama3.2
- **Audio**: librosa, soundfile
- **PDF**: pytesseract, pypdf
- **Data**: numpy, PIL, PyYAML


### **AI Models**
- **LLaMA 3.2 3B**: Text generation and analysis
- **Whisper**: Speech-to-text transcription

## 📋 Prerequisites

### **System Requirements**
- **OS**: Windows 10/11, macOS, or Linux
- **Processor**: Snapdragon X Elite
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: 10GB+ free space for models
- **GPU**: Optional but recommended for faster inference

### **Software Requirements**
- **Python**: 3.8 - 3.11
- **Git**: For version control

## 🚀 Installation & Setup

### **1. Clone Repository**
```bash
git clone https://github.com/YOUR_USERNAME/SnapClass.git
cd SnapClass
```

### **2. Python Environment Setup**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Model Setup**
```bash
# Navigate to server directory
cd server

# Download and setup AI models
python setup.py
```
Dwonload NPU optimised Llama3.2 model [Click here](https://drive.google.com/drive/folders/1TfiNrZJoCg5KLYPmiixiKVCDCU2RyWw1?usp=drive_link)
Download poppler from [here](https://drive.google.com/drive/folders/1Uiy7IQCcPGxjNv6xnyAoFE6zhR81HFH5?usp=sharing)
**Note**: This will download ~5GB of AI models. Ensure stable internet connection.

## 🎯 Usage

### **Desktop Application**
```bash
cd server
python desktop_app.py
```

## 🔧 Configuration

### **Model Configuration**
- **LLaMA**: Edit `server/llama3/genie_config.json`
- **Whisper**: Configure in `server/whisper/config.json`
- **Nougat**: Settings in `server/nougat/config.json`
- **BLIP**: Options in `server/blip/config.json`

## 📦 Building Executable and Msix

### **Using PyInstaller**
```bash
# Use MSIX build script
.\build.ps1 -Version "1.0.0.0" -Publisher "CN=SnapClass.A"
```

## 🐛 Troubleshooting

#### **Model Loading Errors**
```bash
# Verify model files exist
ls -la server/llama3/
ls -la server/whisper/
```

#### **Memory Issues**
- Reduce batch sizes in model configurations
- Use CPU-only inference for lower memory usage
- Close other applications to free RAM
- Check the availability of Snapdragon NPU

#### **Import Errors**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

### **Performance Optimization**
- **GPU Acceleration**: Install CUDA-enabled PyTorch
- **Model Quantization**: Use quantized models for faster inference
- **Batch Processing**: Process multiple files simultaneously

## 🤝 Contributing

### **Development Setup**
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature-name`
6. Create Pull Request

### **Code Style**
- **Python**: Follow PEP 8 guidelines
- **Documentation**: Update README for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI**: LLaMA 3.2 model
- **OpenAI**: Whisper speech recognition
- **Open Source Community**: Various libraries and tools

## 📞 Support
- A T Abbilaash (abbilaashat@gmail.com)

**Made with ❤️ for the educational community**
