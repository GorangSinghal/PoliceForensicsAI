# Police Forensics AI: Cyber Command Terminal 🚓

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![UI: Gradio](https://img.shields.io/badge/UI-Gradio-orange)](https://gradio.app/)

Welcome to the **Police Forensics AI** project, an advanced secure evidence extraction system designed for law enforcement precincts. This tool leverages cutting-edge Deep Learning GANs (CodeFormer/RealESRGAN) to computationaly restore blurry dashboard camera and surveillance evidence, and state-of-the-art Vision-Language Models (Google Gemini & Llama 3) to strictly extract deterministic data.

## Features
- **Dual-Tier Image Preprocessing (Licensing Strategy):** 
  - **OpenCV Pipeline (Default - Commercial MIT):** Utilizes dynamic contrast normalization and mathematical edge-detection to prepare evidence for OCR. This path is 100% MIT-licensed and safe for commercial enterprise deployment.
  - **CodeFormer GAN (Opt-In - Research S-Lab):** For heavily degraded images, users can toggle the Deep Learning PyTorch bridge. This runs CodeFormer + Real-ESRGAN to computationally restore human faces and background text. *Note: This path invokes an S-Lab Non-Commercial license and requires strict legal compliance.*
- **Pluggable LLM Architecture:** 
  - **Gemini Cloud (Default):** Lightning-fast structured extraction using Google's Gemini Flash.
  - **Llama 3 Local (Fallback):** 100% offline edge-computing extraction using Ollama for maximum evidence security.
- **Deterministic Guardrails:** Implements strict regex, fuzzy date parsing, and Word Error Rate (WER) evaluations to completely eliminate AI hallucinations.
- **Exporting Capabilities:** Seamlessly exports extracted JSON data into flat CSV and Excel reports for precinct archives.

## Installation & Setup

### 1. Developer Setup (Python Environment)
1. Clone the repository: `git clone https://github.com/your-username/PoliceForensicsAI.git`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `.\venv\Scripts\Activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and insert your Gemini API Key.
6. Run the application: `python src/app.py`

### 2. Standalone Windows Desktop App
For non-technical officers, you can download the standalone `.exe` folder.
1. Run `.\scripts\build_executable.ps1` to compile the application using PyInstaller.
2. Distribute the generated `dist/CyberTerminal/` folder to precinct laptops. No Python installation required!

### 3. Docker Deployment
For IT infrastructure deployment:
1. Build the image: `docker build -t police-forensics-ai .`
2. Run the container: `docker run -p 7860:7860 police-forensics-ai`

## Project Architecture
- `src/app.py`: The Gradio User Interface.
- `src/ocr_engine.py`: The orchestration layer managing LLMs and Guardrails.
- `src/modules/codeformer_bridge.py`: The PyTorch bridge interfacing with the GAN.
- `tests/test_evaluation.py`: The rigorous unit testing suite evaluating WER and Entity Accuracy against the 100-case Golden Matrix.

## License
This project is released under the permissive [MIT License](LICENSE).
