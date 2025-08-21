# 🎓 SnapClass - AI-Powered Educational Assistant

SnapClass is an intelligent educational platform that combines multiple AI models to process, analyze, and generate educational content from various input sources including audio, PDFs, and text.

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
│
├── 🤖 AI Models/                # AI model directories
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
├── 🌐 snapclass webpage/         # Frontend React application
│   ├── 📁 src/
│   │   ├── components/          # React components
│   │   ├── App.jsx              # Main application
│   │   └── main.jsx             # Entry point
│   └── package.json             # Node.js dependencies
│
└── 📋 requirements.txt           # Python dependencies
```

## 🚀 Key Features

### 🎯 **Multi-Modal AI Processing**
- **Audio Processing**: Speech-to-text conversion using Whisper
- **Document Processing**: PDF text extraction using Nougat
- **Image Understanding**: Visual content analysis using BLIP
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
- **AI/ML**: PyTorch, Transformers, Whisper, Nougat, BLIP
- **Audio**: librosa, soundfile
- **PDF**: pdf2image, pytesseract
- **Data**: numpy, PIL, PyYAML

### **Frontend (React)**
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Components**: Modern, responsive UI

### **AI Models**
- **LLaMA 3.2 3B**: Text generation and analysis
- **Whisper**: Speech-to-text transcription
- **Nougat**: Document understanding and OCR
- **BLIP**: Visual language understanding

## 📋 Prerequisites

### **System Requirements**
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: 10GB+ free space for models
- **GPU**: Optional but recommended for faster inference

### **Software Requirements**
- **Python**: 3.8 - 3.11
- **Node.js**: 18+ (for frontend development)
- **Git**: For version control
- **Git LFS**: For large model files

## 🚀 Installation & Setup

### **1. Clone Repository**
```bash
# Clone with Git LFS
git lfs install
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

**Note**: This will download ~8GB of AI models. Ensure stable internet connection.

### **4. Frontend Setup (Optional)**
```bash
# Navigate to frontend directory
cd ../snapclass webpage

# Install Node.js dependencies
npm install

# Build frontend
npm run build
```

## 🎯 Usage

### **Desktop Application**
```bash
cd server
python desktop_app.py
```

### **Web Server Only**
```bash
cd server
python app.py
```

### **Frontend Development**
```bash
cd snapclass webpage
npm run dev
```

## 🔧 Configuration

### **Model Configuration**
- **LLaMA**: Edit `server/llama3/genie_config.json`
- **Whisper**: Configure in `server/whisper/config.json`
- **Nougat**: Settings in `server/nougat/config.json`
- **BLIP**: Options in `server/blip/config.json`

### **Server Settings**
- **Port**: Default 5000 (configurable in `app.py`)
- **Upload Limits**: Adjust in Flask configuration
- **Output Paths**: Modify in `trans.py`

## 📦 Building Executable

### **Using PyInstaller**
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name SnapClass desktop_app.py

# Copy model folders to dist/
xcopy "llama3" "dist\llama3\" /E /I /Y
xcopy "whisper" "dist\whisper\" /E /I /Y
xcopy "nougat" "dist\nougat\" /E /I /Y
xcopy "blip" "dist\blip\" /E /I /Y
xcopy "poppler" "dist\poppler\" /E /I /Y
```

## 🐛 Troubleshooting

### **Common Issues**

#### **Model Loading Errors**
```bash
# Verify model files exist
ls -la server/llama3/
ls -la server/whisper/
ls -la server/nougat/
ls -la server/blip/
```

#### **Memory Issues**
- Reduce batch sizes in model configurations
- Use CPU-only inference for lower memory usage
- Close other applications to free RAM

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
- **JavaScript**: Use ESLint configuration
- **Documentation**: Update README for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI**: LLaMA 3.2 model
- **OpenAI**: Whisper speech recognition
- **Microsoft**: Nougat document understanding
- **Salesforce**: BLIP vision-language model
- **Open Source Community**: Various libraries and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/SnapClass/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/SnapClass/discussions)
- **Wiki**: [Project Wiki](https://github.com/YOUR_USERNAME/SnapClass/wiki)

## 🔄 Version History

- **v1.0.0**: Initial release with core AI models
- **v1.1.0**: Added desktop GUI application
- **v1.2.0**: Web interface and React frontend
- **v1.3.0**: Enhanced question generation and analysis

---

**Made with ❤️ for the educational community**
