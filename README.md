# Police Forensics AI: Cyber Command Terminal 🚓

[![CI/CD Pipeline](https://github.com/GorangSinghal/PoliceForensicsAI/actions/workflows/ci.yml/badge.svg)](https://github.com/GorangSinghal/PoliceForensicsAI/actions/workflows/ci.yml)
[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-PoliceForensics__Llama3__8B-blue)](https://huggingface.co/GorangSinghal/PoliceForensics_Llama3_8B)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=flat&logo=PyTorch&logoColor=white)](https://pytorch.org/)
[![Frontend: React + Vite](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB.svg)](frontend/)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](src/api.py)

**PoliceForensicsAI** is an enterprise-grade forensic evidence extraction and super-resolution system engineered for law enforcement precincts and air-gapped forensic laboratories. The platform pairs deep-learning generative restoration (CodeFormer GAN) with a custom fine-tuned Small Language Model (SLM) based on **Llama 3 8B** quantized to 4-bit GGUF, enforcing strict deterministic guardrails to prevent AI hallucinations.

> **Law Enforcement Validation:** Developed and audited for operational law enforcement workflows, this platform was presented and demonstrated in an official training programme for **150+ Rajasthan Police personnel** under the guidance of Dr. Gyan Singh (HoD, CSE) and Mr. Abdul Javed at the Indian Institute of Information Technology (IIIT) Kota.

---

## ⚡ Key Capabilities

* **Dual-Tier Image Preprocessing (Licensing Isolation):**
  * **OpenCV Mathematical Filter (Default - Commercial MIT):** Dynamic contrast normalization, morphological sharpening, and edge enhancement. 100% MIT-licensed and safe for unencumbered commercial enterprise deployment.
  * **CodeFormer GAN Bridge (Opt-In - Research S-Lab):** For severe facial degradation and degraded license plate crops, users can toggle the PyTorch GAN super-resolution bridge to synthesize lost high-frequency details.
* **Pluggable Edge-to-Cloud SLM/LLM Engine:**
  * **Offline Air-Gapped Mode (Primary):** Runs a custom fine-tuned **Llama 3 8B** model quantized to `Q4_K_M` GGUF (4.92 GB) via `llama-cpp-python`. Engineered with strict 8GB laptop RAM constraints (`n_ctx=256`, `n_batch=8`, `n_threads=2`, `use_mmap=True`) for edge deployment on standard precinct laptops.
  * **Gemini Cloud Mode (Fallback):** Google Gemini Flash integration with exponential backoff (`tenacity`) for high-throughput cloud batch processing.
* **Cryptographic Chain-of-Custody (SHA-256):** Computes an immutable SHA-256 cryptographic digest upon image upload to guarantee evidentiary integrity against digital tampering in legal proceedings.
* **Deterministic Guardrails & Abstention Logic:** SpaCy/Regex pattern matching, Levenshtein distance string verification, and strict schema validation completely eliminate generative hallucinations (100% zero-hallucination rate on non-vehicle records).
* **Decoupled Modern Architecture:** Decoupled FastAPI REST backend (`src/api.py`) paired with a modern React + Vite + TailwindCSS Cyber Command Dashboard (`frontend/`) featuring Framer Motion telemetry animations. Retains legacy Gradio interface (`src/app_legacy.py`) for single-script offline deployments.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A["Officer Uploads Evidence Photo"] --> B["SHA-256 Cryptographic Hash<br/>(Courtroom Chain-of-Custody Stamp)"]
    
    B --> C{"Enhancement Selector"}
    C -->|Default / Commercial MIT| D["OpenCV Mathematical Filters<br/>(Contrast & Morphology)"]
    C -->|Opt-In / Severe Blur| E["CodeFormer GAN Super-Resolution<br/>(S-Lab PyTorch Bridge)"]
    
    D --> F["EasyOCR Deep Learning Engine<br/>(CRNN + LSTM Tokenizer)"]
    E --> F
    
    F --> G{"Pluggable LLM/SLM Router"}
    G -->|Offline Air-Gapped| H["Fine-Tuned Llama 3 8B (Q4_K_M GGUF)<br/>llama-cpp-python in 8GB RAM"]
    G -->|Cloud Speed| I["Google Gemini 1.5 Flash<br/>Cloud REST API"]
    
    H --> J["Deterministic Guardrails & Regex<br/>(Date Normalizer & Plate Syntax Checker)"]
    I --> J
    
    J --> K["Verified Forensic JSON Payload<br/>(license_plate, date, suspect_name, raw_text)"]
    K --> L["Courtroom Export<br/>(CSV, Excel, Database Dispatch)"]
```

---

## 📊 Empirical Benchmarks & Evaluation Reports

The fine-tuned SLM and multimodal vision pipeline were rigorously audited on Google Colab (NVIDIA T4 GPU) across a 100-case Golden Matrix:

| Benchmark Run | Evaluation Modality | Primary Metric | Zero-Hallucination Rate | Latency | Report Link |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Colab 1: Reasoning Layer** | Raw OCR Tokens $\rightarrow$ Llama 3 8B | **98.0%** (49/50 Plates) | **100.0%** (50/50 Receipts) | 1.42s | [`evaluation_report_colab1.md`](reports/evaluation_report_colab1.md) |
| **Colab 2: Physical Images** | Synthetic Physical JPEGs $\rightarrow$ OCR $\rightarrow$ Llama 3 | **30.0%** (Unassisted OCR) | **100.0%** (50/50 Receipts) | 1.80s | [`end_to_end_image_benchmark_colab2.md`](reports/end_to_end_image_benchmark_colab2.md) |
| **Colab 3: Curated 100-Case Matrix** | Adverse Weather / CCTV JPEGs $\rightarrow$ OCR $\rightarrow$ Llama 3 | **59.0%** (Adverse Baseline) | **100.0%** (Strict JSON Schema) | 1.97s | [`official_curated_100_case_report_colab3.md`](reports/official_curated_100_case_report_colab3.md) |

> **Key Architectural Takeaway:** While the fine-tuned Llama 3 8B achieves **98% extraction accuracy** when supplied clean character tokens, extreme real-world optical noise (mud splatter, cursive handwriting, night glare) drops unassisted optical OCR to 59%. This empirically justifies the upstream **CodeFormer GAN Super-Resolution layer** before OCR tokenization.

---

## 🚀 Quick Start Guide

### 1. Clone & Environment Setup

```bash
# Clone the repository
git clone https://github.com/GorangSinghal/PoliceForensicsAI.git
cd PoliceForensicsAI

# Create and activate Python virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\Activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download the Fine-Tuned Model Weights

Download the official 4-bit quantized GGUF model directly from Hugging Face:

```bash
python scripts/download_weights.py
```
*Model Repository:* [`huggingface.co/GorangSinghal/PoliceForensics_Llama3_8B`](https://huggingface.co/GorangSinghal/PoliceForensics_Llama3_8B) (`llama-3-8b-instruct.Q4_K_M.gguf`, 4.92 GB).

### 3. Launch the Application

#### Option A: Modern React + FastAPI Dashboard (Recommended)

Terminal 1 (Backend API):
```bash
uvicorn src.api:app --reload --port 8000
```

Terminal 2 (Frontend Dashboard):
```bash
cd frontend
npm install
npm run dev
```
Open [`http://localhost:5173`](http://localhost:5173) in your browser to access the Cyber Command Terminal.

#### Option B: Standalone Gradio Interface (Offline / Air-Gapped Fallback)

```bash
python src/app_legacy.py
```
Open [`http://localhost:7860`](http://localhost:7860) for direct single-script operation.

---

## 🧪 Testing & Continuous Integration (CI/CD)

The project includes an enterprise CI/CD pipeline running on GitHub Actions on every push and pull request:

```bash
# Run the 100-case deterministic guardrail test suite
python -m pytest tests/ -v

# Run AST security vulnerability audit
bandit -r src/ -c bandit.yaml
```

* **Automated Test Suite:** [`tests/test_evaluation.py`](tests/test_evaluation.py) validates Word Error Rate (WER) and entity extraction precision across 100 golden samples.
* **Security Scanner:** [`bandit.yaml`](bandit.yaml) audits against hardcoded credentials, shell injections, and insecure deserialization.
* **CI Workflow Definition:** [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## 📁 Repository Structure

```text
PoliceForensicsAI/
├── .github/workflows/ci.yml    # Enterprise CI/CD workflow (PyTest + Bandit)
├── frontend/                   # Modern React 19 + Vite + TailwindCSS dashboard
│   ├── src/App.jsx             # Cyber command telemetry interface
│   └── package.json            # Node.js dependencies
├── src/                        # Core Python backend micro-modules
│   ├── api.py                  # FastAPI REST endpoints (/analyze, /export, /health)
│   ├── ocr_engine.py           # Orchestrator (Facade Pattern)
│   ├── app_legacy.py           # Gradio fallback interface
│   └── modules/                # Decoupled SOLID components
│       ├── image_preprocessor.py # OpenCV contrast & morphology
│       ├── vision_module.py    # EasyOCR integration with local weight isolation
│       ├── llm_client.py       # Gemini SDK + Local Llama 3 8B GGUF runtime
│       ├── data_validator.py   # Deterministic Regex & date parsing guardrails
│       └── codeformer_bridge.py# PyTorch GAN super-resolution bridge
├── reports/                    # Empirical benchmark evaluation audits
│   ├── evaluation_report_colab1.md
│   ├── end_to_end_image_benchmark_colab2.md
│   └── official_curated_100_case_report_colab3.md
├── scripts/                    # Automation & MLOps utilities
│   ├── build_dataset.py        # 2,000-sample hybrid dataset builder
│   ├── download_weights.py     # Automated Hugging Face model pull
│   └── colab_step2_5_evaluation.py # Colab T4 evaluation script
├── golden/data/                # Curated 100-case high-resolution evaluation matrix
├── docs/                       # Architectural documentation & task checklists
│   ├── task.md                 # Project implementation roadmap
│   └── annexure.md             # Comprehensive technical knowledge base
├── bandit.yaml                 # Static AST security scanner configuration
└── requirements.txt            # Python dependencies
```

---

## 📜 License

This project is open-source under the permissive [MIT License](LICENSE).  
*Notice on Third-Party Weights:* S-Lab CodeFormer weights are subject to their respective non-commercial research licensing terms. When operating in commercial production, use the default OpenCV mathematical processing tier.
