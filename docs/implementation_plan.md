# PoliceForensicsAI: Evidence Processing Toolkit (MLOps & Implementation Plan)

We will be migrating the entire project into a new, master folder to represent the complete software suite. This project will follow strict MLOps (Machine Learning Operations) and FAANG-level testing practices.

**Proposed Project Name:** `PoliceForensicsAI` 

## 📍 Project Roadmap
We will build this in strict, test-driven phases to ensure production-level reliability.

* **Phase 1: Foundation & Evaluation (Current)** - Setup the `NexusForensics` folder, initialize the environment, and establish the **Golden Matrix**.
* **Phase 2: The Core OCR Engine** - Build `ocr_engine.py` (OpenCV + Gemini) and run it against the Golden Matrix to establish baseline accuracy.
* **Phase 3: Image Restoration Integration** - Migrate the local CodeFormer repo into our master architecture.
* **Phase 4: The Unified UI** - Build the 3-Tab Gradio Interface (Restoration, OCR, Batch Processing).
* **Phase 5: Cloud Deployment** - Containerize the app and deploy it to Hugging Face Spaces.

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

## 📁 Master Folder Structure & Repo Standards (sipllm-inspired)

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

---

## User Review Required
> [!IMPORTANT]
> The plan now officially incorporates strict **MLOps Testing**, a **Roadmap**, and a **Golden Matrix** for mathematical evaluation. Does this level of engineering rigor look good to you? If so, we will kick off **Phase 1** and start creating this structure!
