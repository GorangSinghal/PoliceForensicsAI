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

- `[❌]` **Phase 5.5: Standalone Commercial Real-ESRGAN Pipeline**
    - `[❌]` Integrate Real-ESRGAN to test commercial viability.
    - `[❌]` Evaluate results: Commercial GANs introduce Generative Smoothing and destroy text.
    - `[❌]` Rollback architecture and document failure to justify S-Lab CodeFormer Licensing.

- `[x]` **Phase 6: Offline SLM Engine Implementation (Dynamic .gguf Architecture)**
    - `[x]` Pivot from native Ollama dependency to a fully bundled `.gguf` weight detection system.
    - `[x]` Evaluate and benchmark Small Language Models (SLMs) (e.g. `TinyLlama 1B` for LITE mode).
    - `[x]` Re-run the 100-Case Evaluation Suite purely offline to certify Air-Gapped accuracy.
    - `[x]` Build a dynamic Hardware Badge in the UI that auto-unlocks PRO Mode when 8B `.gguf` weights are detected.

- `[ ]` **Phase 6.5: ECLIPSE-Tier UI Upgrade (React + FastAPI)**
    - `[ ]` Migrate backend to a decoupled FastAPI REST architecture (`src/api.py`).
    - `[ ]` Initialize a Vite + React + TailwindCSS frontend (`frontend/`).
    - `[ ]` Build a premium, cinematic Cyber Command Dashboard with Framer Motion animations.
    - `[ ]` Retain existing Gradio interface as `src/app_legacy.py` for fallback offline deployments.

- `[ ]` **Phase 6.6: Forensic Explainable AI (XAI) / AEGIS**
    - `[ ]` **Cryptographic Hashing (SHA-256):** Generate an unbreakable mathematical hash of the raw image upon upload to guarantee chain-of-custody and prevent digital tampering.
    - `[ ]` Implement "Difference Heatmaps" to visually highlight exact pixels altered by the CodeFormer GAN.
    - `[ ]` **Counter-Factual Visualizations:** Visually demonstrate why the AI rejected alternative extractions (e.g., showing the pixel distance between an '8' and a 'B') to preempt defense attorney arguments.
    - `[ ]` Expose Multi-Metric Confidence Scoring:
        - **LLM Token Probabilities:** To indicate pure neural certainty.
        - **Fuzzy Accuracy / Levenshtein Distance:** To measure string distance when cross-referencing names or plates against known police databases.
        - **Character Structural Similarity:** Highlighting ambiguous characters (e.g., '8' vs 'B' or 'O' vs '0') based on visual feature matching.
    - `[ ]` Display AEGIS transparency reports directly in the React dashboard for courtroom readiness.
    - `[ ]` **Automated Courtroom-Ready PDF Reporting:** Generate verifiable, stylized PDF documents containing original/restored images, cryptographic hashes, extracted JSON, and AEGIS confidence metrics for handoffs.

- `[ ]` **Phase 7: Mobile Application Scaling (Flutter)**
    - `[ ]` Expose the existing Python OCR/GAN backend as a REST API (using FastAPI or Flask)
    - `[ ]` Initialize Flutter mobile app repository for iOS and Android officers
    - `[ ]` Build native camera interface to capture and crop evidence photos in the field
    - `[ ]` Implement secure token authentication between the mobile app and central precinct server
    - `[ ]` Build an offline caching system for mobile devices when cellular connection is lost in remote areas

- `[ ]` **Phase 8: Advanced Video & Biometric Analysis (Dynamic Routing)**
    - `[ ]` Integrate `YOLOv8` for real-time bounding box detection of vehicles, license plates, and faces in video files
    - `[ ]` Train a custom YOLOv8 / OpenCV license plate detection filter purely on heavily degraded, low-light footage
    - `[ ]` **Build the Dynamic Routing Pipeline:**
        - `[ ]` Route `[Face]` bounding boxes directly to CodeFormer (S-Lab) for facial restoration
        - `[ ]` Route `[License Plate]` bounding boxes directly to Real-ESRGAN + OpenCV (MIT/BSD) for commercial-safe text extraction
    - `[ ]` Integrate `facenet-pytorch` for facial detection and biometric feature extraction
    - `[ ]` Build a Facial Matching Database to compare cropped faces against known suspects
    - `[ ]` Add a new "Video & Biometrics" tab in the Gradio UI

- `[/]` **Phase 9: Security & QA Polish (Enterprise Hardening)**
    - `[x]` **Fix Mocking Loophole:** Write an un-mocked Integration Test suite that hits a local LLM or sandbox API to verify true end-to-end OCR math.
    - `[x]` Implement robust Error Handling for malformed JSON returns and Edge Cases
    - `[x]` **Sanitize the GitHub Repo:** Remove hardcoded paths (Completed) and add `.env.example` (Completed).
    - `[x]` **Fix PII Logging Loophole:** Audit `src/ocr_engine.py` and replace all raw `print(e)` exceptions with sanitized, generic error loggers to ensure zero PII leakage on crash.
    - `[ ]` **Documentation (Post-Phase 11):** Write a FAANG-level `README.md` and `DEPLOYMENT.md` detailing the new LoRA architecture.
    - `[ ]` **Fix Over-Fitting Loophole:** Siphon 100 actual, physical Out-Of-Distribution (OOD) degraded images into `golden/data/` to replace the synthetic evaluation script.
    - `[x]` **Refactor God Class (Weekend Task):** Refactor `src/ocr_engine.py` using the Single Responsibility Principle to decouple it into 5 distinct modules: `vision_module.py`, `llm_client.py`, `data_validator.py`, `image_preprocessor.py`, and the main `ocr_controller.py`.

- `[ ]` **Phase 10: FAANG / GSoC Mock Interview**
    - `[ ]` Type `/grill-me` in the chat to initiate a brutal Mock Interview covering the architectural decisions of PoliceForensicsAI.

- `[ ]` **Phase 11: Custom Model Fine-Tuning (LoRA) & Enterprise Deployment**
    - `[ ]` **Step 1 - Dataset Engineering (The 2,000 Hybrid):** Write a Python script to automatically construct a `dataset.jsonl` file by merging:
        - `[ ]` 1,000 JSON documents from Kaggle's SROIE (Teaches JSON structural discipline)
        - `[ ]` 500 global plates from Hugging Face `sonnetechnology` (Teaches extreme rain/night/blur resilience)
        - `[ ]` 500 regional plates from Hugging Face `Dataclusterlabspvtltd` (Teaches Indian state codes and syntax)
    - `[ ]` **Step 2 - LoRA Fine-Tuning:** Use Google Colab to train a LoRA/QLoRA adapter on a `Llama 3 8B` model using your `dataset.jsonl` file, exporting it as a Q4_K_M `.gguf` file.
    - `[ ]` **Step 3 - Optimized Runtime:** Refactor `src/ocr_engine.py` to completely replace Ollama with `llama-cpp-python`, strictly limiting RAM usage so the 8B model fits safely inside 8GB laptops.
    - `[ ]` **Step 4 - Plug & Play Auto-Downloader:** Write an `__init__.py` script that automatically downloads the 4.5GB `.gguf` file into the `weights/` folder upon first boot.
    - `[ ]` **Step 5 - Setup CI/CD Pipeline:** Create a GitHub Actions `.yml` file to automatically run the PyTest Integration Suite against the new LoRA model on every commit.

- `[ ]` **Phase 11.11: RAG-Based Digital Case Files (Difficulty: Low/Medium)**
    - `[ ]` Implement a "Chat with the Evidence" feature using LangChain and a Vector Database (like ChromaDB).
    - `[ ]` Allow officers to query restored evidence naturally (e.g., "Show me every blurry blue sedan caught on dashcam near 5th Street last week").

- `[ ]` **Phase 11.22: Adversarial Deepfake Detection (Difficulty: Medium)**
    - `[ ]` Integrate an open-source Deepfake detection model as an Anti-Tamper routing layer.
    - `[ ]` Analyze images at the noise/pixel level before CodeFormer processing to detect GAN-artifacts or Photoshop manipulation.
    - `[ ]` Flag and lock tampered files to preserve the legal integrity of the precinct.

- `[ ]` **Phase 11.33: Continuous Active Learning (Difficulty: Hard)**
    - `[ ]` Log officer UI corrections when the XAI module flags low-confidence extractions.
    - `[ ]` Trigger automated micro-fine-tuning scripts (LoRA) nightly using the officer's corrections.
    - `[ ]` Implement safeguards against Catastrophic Forgetting to ensure the AI gets smarter without losing baseline accuracy.

- `[ ]` **Phase 11.44: Distributed Edge Computing / Swarm (Difficulty: Extreme)**
    - `[ ]` Build a decentralized cluster to process heavy workloads (like 2-hour YOLOv8 dashcam videos).
    - `[ ]` Chunk videos and distribute inference tasks to idle laptops on the local precinct Wi-Fi network.
    - `[ ]` Handle network failures and asynchronous polling to create an on-premise supercomputer out of cheap hardware.

