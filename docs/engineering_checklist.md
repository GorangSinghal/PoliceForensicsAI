# PoliceForensicsAI Engineering Checklist

This checklist must be followed before merging any Pull Request to ensure we are building a robust, production-ready forensic tool, rather than a brittle prototype that only passes test cases.

## 1. MLOps & Computer Vision Integrity
- [ ] **No Hardcoded Magic Numbers:** Ensure parameters like OpenCV block sizes, thresholds, or C-constants are either dynamically calculated or omitted if they introduce catastrophic failure points on varying edge cases (e.g. night vs day).
- [ ] **Deterministic LLM Output:** Ensure all Gemini/LLM API calls set `temperature=0.0` and `top_p` constraints when extracting strict facts to prevent hallucination.
- [ ] **Graceful Degradation:** If an intermediate processing step (like GAN de-blurring or CV thresholding) destroys the image completely, the system must have a fallback mechanism to try the raw image.

## 2. Robust Guardrails
- [ ] **Flexible Input, Strict Output:** Guardrails (Regex, Date Parsers) must be designed to accept diverse inputs. (e.g. Do not force the LLM to output one format, instead let it extract the raw entity and use code like `dateutil.parser` to normalize it).
- [ ] **Global Standards:** Always default to localized standards (e.g., India Date Standard: `DD-MM-YYYY`) in the final UI output.
- [ ] **No Destructive Regex:** Ensure Regex filters (like stripping characters from License Plates) do not unintentionally destroy foreign or non-standard inputs.

## 3. Data Privacy & Legal Compliance (Forensics)
- [ ] **Zero Logging of PII:** Ensure the application never saves raw JSON output to persistent local log files (unless specifically exported by the user).
- [ ] **Immutable Golden Truths:** The Golden Matrix test cases must NEVER be modified just to make a new test pass. If a test fails, the algorithm is flawed, not the test data.

## 4. System Architecture & QA Loophole Checks
- [ ] **The "Mocking" False Security Check:** `unittest.mock` is great for CI/CD speed, but it bypasses core logic. Ensure you run at least one un-mocked Integration Test (using a local SLM or real API key) before every major release to verify the actual OCR math is intact.
- [ ] **PII Crash-Logging Protection:** Ensure all `try/except` blocks gracefully catch errors. Python must never dump raw variables or payloads into a stack trace if the program crashes, as this violates "Zero PII Logging" compliance.
- [ ] **Golden Matrix Over-Fitting Prevention:** Ensure the Golden Matrix is continuously injected with chaotic, heavily degraded, Out-of-Distribution (OOD) images (e.g., night-time, blurry, obscured plates) to prevent the AI from falsely scoring 100% on "perfect" inputs.
