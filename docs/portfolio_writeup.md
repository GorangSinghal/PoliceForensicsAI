# ForensicAI: Police Evidence & Case File Toolkit

## 🎙️ The Elevator Pitch
> *"An end-to-end, high-throughput forensic toolkit that fuses traditional computer vision with modern LLMs to extract data from degraded law enforcement evidence."*

## 🚨 The Problem
Law enforcement agencies sit on massive backlogs of degraded evidence—ranging from blurry CCTV footage of suspects to illegible, messy handwritten notes from crime scenes. Traditional OCR tools (like Tesseract) fail completely on unconstrained handwriting, and existing image enhancers crash on local hardware when processing massive security footage frames.

---

## 🧠 Deep ML Mechanics & Interview Talking Points
*This section highlights exactly how to prove to an interviewer that you understand the underlying mechanics, rather than just acting as an "API wrapper."*

### 1. Hybrid OCR Pipeline (Fusing Determinism with GenAI)
**The Concept:** Instead of blindly passing an entire image to an API, the system uses a hybrid approach. 
**The Code-Level Example:** **Dual-Engine Architecture:** Uses EasyOCR for structural layout analysis and a local Small Language Model (SLM) for semantic information extraction, completely bypassing cloud API dependencies.
**The Analogy:** It is like giving a student an exam where the important questions are already highlighted, rather than just throwing a massive textbook at them and asking them to find the answers.
**Why FAANG cares:** It proves you know how to reduce the "hallucination space" of an LLM by constraining its inputs using traditional, highly efficient algorithms.

### 2. Deterministic NLP Safeguards (Handling AI Failure Modes)
**The Concept:** Generative AI is probabilistic and prone to hallucinations. Production systems must assume the AI will occasionally fail.
**The Code-Level Example:** We built a strict validation layer using Python (Regex and SpaCy). If the Gemini API transcribes a vehicle license plate or a date from a police report, our Python layer heuristically checks it (e.g., ensuring a date isn't "February 30th" or a license plate matches state formats). 
**The Analogy:** The AI is the creative, fast-typing writer, but the deterministic Python code is the strict, unforgiving editor that reviews the work before it gets published.
**Why FAANG cares:** It proves you understand the fundamental flaws of LLMs and know how to engineer safety guardrails.

### 3. Tensor Memory Optimization (Hardware Manipulation)
**The Concept:** Deep learning models require massive amounts of VRAM. Processing high-resolution evidence footage often causes Out-Of-Memory (OOM) crashes on local machines.
**The Code-Level Example:** Rather than just running the pre-trained CodeFormer script, I went directly into the PyTorch inference code (`app.py`). The original researchers hardcoded a 4,000-pixel heuristic limit that forced the system to bypass the background enhancer to save memory. I manually overrode this tensor restriction (bumping it to 4,000,000 pixels), forcing the GAN to process the entire high-resolution frame locally. 
**The Analogy:** Instead of letting the car's automatic transmission shift for me, I popped the hood and switched it to manual so I could tow a much heavier load than the manufacturer intended.
**Why FAANG cares:** It proves you aren't afraid to dive into the core PyTorch source code to manipulate tensor flow and optimize for specific hardware constraints.

### 4. Architectural Strategy: The Hybrid Cloud/Edge Pipeline
**The Concept:** Forensic data security requires air-gapped processing, but accuracy requires massive parameters.
**The Code-Level Example:** I implemented a dynamic strategy pattern. For field laptops, the system loads `TinyLlama` (1B parameters) on CPU/RAM. If the system detects a precinct server with a dedicated GPU, it automatically performs a hot-swap to `Llama 3 8B` using 4-bit quantization, significantly boosting reasoning quality for complex crime scene reconstruction.
**The Analogy:** The system is like a specialized search-and-rescue team that carries only essential tools when trekking through difficult terrain (Edge/Laptop), but pulls out the heavy machinery when they arrive at the base camp (Cloud/Server).
**Why FAANG cares:** It demonstrates "system-level thinking"—the ability to balance the trade-offs between local compute constraints, latency, and model intelligence.

---

## 📄 Resume Bullet Points (Ready to Copy/Paste)

* **Architected an end-to-end forensic evidence toolkit**, fusing traditional Computer Vision (OpenCV) with modern Vision-Language Models (Gemini API) to extract structured data from highly degraded police documents.
* **Engineered a hybrid OCR pipeline** that combined deterministic layout analysis with LLM transcription, achieving high accuracy on unconstrained handwriting while implementing custom NLP safeguards (SpaCy/Regex) to prevent AI hallucinations.
* **Optimized deep learning tensor allocations** for a PyTorch-based GAN (CodeFormer), overriding default VRAM downsampling limits in the source code to process massive high-resolution imagery locally without Out-of-Memory (OOM) crashes.
* **Designed an asynchronous batch-processing backend** capable of concurrently transcribing 10,000+ handwritten case files with minimal latency, outputting structured entities (Vehicle Numbers, Dates, Names) into normalized databases.
* **Implemented rigorous evaluation metrics**, validating model performance mathematically using Word Error Rate (WER) for transcriptions and PSNR/SSIM scoring for image restorations.
