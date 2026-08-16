- `[x]` **Phase 1: Foundation & Evaluation (MLOps Setup)**
    - `[x]` Initialize `PoliceForensicsAI` master directory
    - `[x]` Create repository standards (MIT `LICENSE`, `.gitignore`, `.env`)
    - `[x]` Setup Python environment and install core dependencies (`google-generativeai`, `opencv-python`, `python-dotenv`, `pytest`)
    - `[x]` Create the Golden Matrix structure (`tests/golden_matrix/`)
    - `[x]` Curate 3-5 sample evidence images and write their ground-truth JSONs
    - `[x]` Write `test_evaluation.py` to calculate Word Error Rate (WER) and Entity Accuracy

- `[x]` **Phase 2: Core OCR Engine (Hybrid Pipeline)**
    - `[x]` Write `src/ocr_engine.py` (OpenCV pre-processing logic)
    - `[x]` Implement Gemini Few-Shot prompting for strict JSON output
    - `[x]` Implement deterministic guardrails (SpaCy/Regex) for date and license plate validation
    - `[x]` Run the evaluation suite and iterate on the prompt until target accuracy is reached

- `[x]` **Phase 3: CodeFormer Integration (Image Restoration)**
    - `[x]` Migrate the local CodeFormer module into `third_party/CodeFormer/`
    - `[x]` Write `modules/codeformer_bridge.py` to interface with the PyTorch GAN
    - `[x]` Ensure VRAM override limits (40,000px) are hardcoded into the bridge

- `[x]` **Phase 4: Unified UI (Frontend & Exporting)**
    - `[x]` Design and build `main_app.py` using Gradio Tabs
    - `[x]` Connect Tab 1 (Image Restoration) to the CodeFormer bridge
    - `[x]` Connect Tab 2 (Document OCR) to the OCR engine
    - `[x]` Connect Tab 3 (Batch Processing) for high-throughput folder scanning
    - `[x]` Implement "Export to CSV" and "Export to Excel (.xlsx)" functionality for police record keeping

- `[x]` **Phase 5: Cloud Deployment, Open Source & Production Readiness**
    - `[x]` Containerize the application (`Dockerfile`)
    - `[x]` Package as a standalone desktop application (`.exe` using PyInstaller) for easy police precinct installation
    - `[x]` Implement Pluggable LLM Architecture (Support for Gemini Cloud & Local Llama 3 fallback)
    - `[x]` Expand Golden Matrix to >= 100 diverse, OOD real-world edge cases to ensure prompt generalization
    - `[x]` Write comprehensive `README.md` and `CONTRIBUTING.md`
    - `[x]` Ensure MIT License is applied to all open-source components
    - `[x]` Deploy to Hugging Face Spaces / GitHub

- `[ ]` **Phase 5.5: Standalone Commercial Real-ESRGAN Pipeline**
    - `[ ]` Write `modules/realesrgan_bridge.py` to decouple Real-ESRGAN from CodeFormer
    - `[ ]` Update the Gradio UI to include a 3-way Radio Button (OpenCV vs Real-ESRGAN vs CodeFormer)
    - `[ ]` Test Real-ESRGAN standalone upscaling on license plates to verify commercial-safe inference

- `[ ]` **Phase 6: Offline SLM Engine Implementation (Ollama)**
    - `[ ]` Install Ollama natively on the target deployment machine
    - `[ ]` Evaluate and benchmark Small Language Models (SLMs) that fit within 8GB RAM (e.g. `moondream2` or `qwen2-vl-2b`)
    - `[ ]` Re-run the 100-Case Evaluation Suite purely offline to certify Air-Gapped accuracy
    - `[ ]` Remove the UI warning label once the physical engine is successfully detected on `localhost:11434`

- `[ ]` **Phase 7: Mobile Application Scaling (Flutter)**
    - `[ ]` Expose the existing Python OCR/GAN backend as a REST API (using FastAPI or Flask)
    - `[ ]` Initialize Flutter mobile app repository for iOS and Android officers
    - `[ ]` Build native camera interface to capture and crop evidence photos in the field
    - `[ ]` Implement secure token authentication between the mobile app and central precinct server
    - `[ ]` Build an offline caching system for mobile devices when cellular connection is lost in remote areas

- `[ ]` **Phase 8: Advanced Video & Biometric Analysis (Dynamic Routing)**
    - `[ ]` Integrate `YOLOv8` for real-time bounding box detection of vehicles, license plates, and faces in video files
    - `[ ]` **Build the Dynamic Routing Pipeline:**
        - `[ ]` Route `[Face]` bounding boxes directly to CodeFormer (S-Lab) for facial restoration
        - `[ ]` Route `[License Plate]` bounding boxes directly to Real-ESRGAN + OpenCV (MIT/BSD) for commercial-safe text extraction
    - `[ ]` Integrate `facenet-pytorch` for facial detection and biometric feature extraction
    - `[ ]` Build a Facial Matching Database to compare cropped faces against known suspects
    - `[ ]` Add a new "Video & Biometrics" tab in the Gradio UI

- `[ ]` **Phase 9: Security & QA Polish (Enterprise Hardening)**
    - `[ ]` **Fix Mocking Loophole:** Write an un-mocked Integration Test suite that hits a local LLM or sandbox API to verify true end-to-end OCR math.
    - `[ ]` **Fix PII Logging Loophole:** Audit `src/ocr_engine.py` and replace all raw `print(e)` exceptions with sanitized, generic error loggers to ensure zero PII leakage on crash.
    - `[ ]` **Fix Over-Fitting Loophole:** Siphon 100 actual, physical Out-Of-Distribution (OOD) degraded images into `golden/data/` to replace the synthetic evaluation script.
