# PoliceForensicsAI: Evidence Processing Toolkit (MLOps & Implementation Plan)

**Project Name:** `PoliceForensicsAI` 

## 📍 Strategic Roadmap & Architecture Phases
This system is architected in strict, test-driven phases to ensure mission-critical reliability for law enforcement deployment.

### ✅ Completed Milestones
* **Phase 1: Foundation & Evaluation** - Established the `PoliceForensicsAI` repository, Python environments, and the synthetic 100-case **Golden Matrix** for MLOps tracking.
* **Phase 2: The Core Extraction Engine** - Engineered `ocr_engine.py` using OpenCV contrast maximization and Gemini/Llama routing with deterministic regex guardrails.
* **Phase 3: Deep Learning GAN Integration** - Successfully bridged the S-Lab CodeFormer PyTorch repository for physical evidence restoration.
* **Phase 4: Cyber Command Terminal (UI)** - Built a highly responsive, tabbed Gradio interface (`app.py`) featuring dark mode, data export (JSON/CSV/Excel), and compliance toggles.
* **Phase 5: Enterprise Deployment** - Containerized the application (`Dockerfile`), compiled a Windows standalone executable (`.exe`), and published the PyPI `setup.py` package.

### 🚧 Active & Future Milestones
* **Phase 5.5: Commercial Up-Scaling** - Decouple Real-ESRGAN from CodeFormer to provide an MIT-licensed, commercial-safe upscaling alternative.
* **Phase 6: Air-Gapped SLM Engine** - Integrate `moondream2` or `qwen2-vl-2b` natively via Ollama for strictly offline, intranet deployment.
* **Phase 7: Mobile Field Application** - Build a Flutter iOS/Android client that interfaces with the Python REST API for field officers.
* **Phase 8: Biometric Video Routing** - Implement YOLOv8 and `facenet-pytorch` for dynamic facial routing against suspect databases.
* **Phase 9: Security Hardening** - Resolve the Mocking, PII Logging, and Over-Fitting loopholes prior to official production launch.

---

## 🧪 Testing & The "Golden Matrix"
Before we write the core OCR code, we must establish how we measure success. We will implement an evaluation strategy identical to enterprise LLM pipelines (like Sipllm).

### 1. The Golden Matrix (Ground Truth Dataset)
We will create a specific folder (`tests/golden_matrix/`) containing carefully curated test cases. For each case, we will have:
* **The Input:** A highly degraded or messy police document (e.g., `case_001.jpg`).
* **The Golden Output:** A perfectly verified, manually typed JSON file representing the absolute correct extraction (e.g., `case_001_truth.json`).

### 2. Automated Evaluation Suite (PyTest)
We will write a testing script (`test_evaluation.py`) that feeds the Golden Matrix inputs into our Gemini OCR Engine and automatically compares the AI's output against the Golden Output. It will calculate:
* **Entity Accuracy:** Did it correctly find the license plate and date?
* **Word Error Rate (WER):** What percentage of the messy handwriting did it get wrong?

### 3. Prompt Versioning & Iteration
Instead of guessing if a prompt is good, we will use the Golden Matrix to mathematically prove it. If we tweak the Gemini prompt to be more strict about police jargon, we will run the Automated Evaluation Suite to ensure our overall accuracy score goes up, preventing regressions.

---

## 📁 Master Folder Structure & Repo Standards

```text
PoliceForensicsAI/
│
├── LICENSE                    # MIT License (Open Source)
├── .gitignore                 # Ignore .env, __pycache__, and large models
├── .env                       # Secure API Keys (DO NOT COMMIT)
├── Dockerfile                 # For FAANG-level cloud containerization
├── requirements.txt           # Master dependencies
├── main_app.py                # Entry Point: The Unified 3-Tab Gradio Web App
│
├── src/                       # Core Source Code (formerly 'modules/')
│   ├── __init__.py
│   ├── ocr_engine.py          # The Gemini + OpenCV Hybrid script
│   └── codeformer_bridge.py   # Code that connects to the CodeFormer model
│
├── tests/                     # Unit Tests & PyTest Suite
│   ├── test_ocr.py
│   └── test_bridge.py
│
├── golden/                    # The Golden Matrix (Ground Truth Evaluation)
│   ├── validate_matrix.py     # Python script to calculate WER & Accuracy
│   └── data/                  # Ground-truth evidence images and JSONs
│
├── scripts/                   # CI/CD & Benchmarking Scripts
│   ├── run_benchmarks.py      # Latency & throughput benchmarking
│   └── setup_env.sh           # Environment bootstrapping
│
├── docs/                      # Architecture & API Documentation
│   └── pipeline_architecture.md
│
└── tools/                     # Standalone utilities
    └── generate_pdf_report.py # E.g., The PDF exporter we wrote
```

---

## 🔍 Deep Dive: OCR Code Flow
1. **Pre-Processing:** OpenCV isolates bounding boxes of text.
2. **LLM Prompting:** Gemini API extracts the text using strict Few-Shot prompts.
3. **Deterministic Guardrails:** Python Regex and SpaCy cross-validate the dates and license plates, marking hallucinations in RED.

