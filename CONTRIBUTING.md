# Contributing to Police Forensics AI

Thank you for your interest in contributing! This project relies on the open-source community to build robust, hallucination-free AI tools for law enforcement.

## Development Setup

1. **Fork & Clone:** Fork the repository and clone it locally.
2. **Environment:** Run `python -m venv venv` and `pip install -r requirements.txt`.
3. **API Keys:** Add your `.env` file with `GEMINI_API_KEY`.
4. **OpenCV (Commercial Preprocessing):** This project relies heavily on `opencv-python` for dynamic contrast normalization and mathematical image preprocessing. Any changes to the core `src/ocr_engine.py` preprocessing logic must remain strictly within OpenCV to maintain commercial deployment compliance.
5. **Local Llama 3:** If you are developing offline backend features, ensure you have [Ollama](https://ollama.ai/) installed and running `llama3.2-vision` locally (`ollama run llama3.2-vision`).

## Testing & Quality Assurance

This project has a strict **Zero Hallucination Tolerance** policy. 

Before submitting a Pull Request, you **MUST** run the Golden Matrix Evaluation Suite to verify that your changes do not degrade Word Error Rate (WER) or Entity Extraction Accuracy.

```powershell
$env:PYTHONPATH="src"
pytest tests/test_evaluation.py -v
```

*Note: The CI/CD test suite uses `unittest.mock` to mathematically verify the extraction logic without hitting Google Cloud rate limits. The suite evaluates 100 heavily degraded synthetic evidence images against the engine and completes in under 2 seconds.*

## Submitting a Pull Request

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Commit your changes: `git commit -m "Add some feature"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Open a Pull Request on GitHub. Please attach screenshots of the Gradio UI if you made frontend changes!
