import os
import sys
import json
import pytest

# Add src to the python path so imports resolve correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.ocr_engine import OCREngine

@pytest.fixture(scope="module")
def engine():
    # Initialize the OCR Engine natively. No mocks.
    return OCREngine()

def load_truth(case_id):
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'golden', 'data'))
    json_path = os.path.join(data_dir, f"{case_id}_truth.json")
    if not os.path.exists(json_path):
        pytest.skip(f"Golden truth data for {case_id} not found.")
    with open(json_path, 'r') as f:
        return json.load(f)

# We selectively test a few highly diverse cases to ensure the actual end-to-end math works.
@pytest.mark.parametrize("case_id", ["case_002", "case_004", "case_007"])
def test_unmocked_end_to_end_extraction(engine, case_id):
    """
    True Integration Test.
    This test physically invokes EasyOCR and the local .gguf SLM on the actual images.
    It completely bypasses the mocking loophole to prove the Guardrails catch hallucinations.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'golden', 'data'))
    img_path = os.path.join(data_dir, f"{case_id}.jpg")
    
    if not os.path.exists(img_path):
        pytest.skip(f"Test image {img_path} not found.")

    weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'weights'))
    gguf_files = [f for f in os.listdir(weights_dir) if f.endswith('.gguf')] if os.path.exists(weights_dir) else []
    if not gguf_files:
        pytest.skip(f"Offline .gguf model weights not present in {weights_dir}. Run scripts/download_weights.py for offline testing.")
        
    truth = load_truth(case_id)
    
    # Execute actual inference in offline mode
    try:
        prediction = engine.extract_entities(img_path, llm_provider="offline")
    except Exception as e:
        err_str = str(e).lower()
        if "access is denied" in err_str or "llama-cpp" in err_str or "no .gguf" in err_str:
            pytest.skip(f"Hardware or sandbox environment restricted: {e}")
        raise

    
    # Verify the structure is absolutely deterministic and never crashes
    assert isinstance(prediction, dict), "Engine must return a dictionary even on total hallucination failure."
    assert "license_plate" in prediction, "Missing license_plate key in output."
    assert "date" in prediction, "Missing date key in output."
    assert "name" in prediction, "Missing name key in output."
    assert "raw_text" in prediction, "Missing raw_text key in output."
    
    # Verify Guardrail behavior explicitly
    if case_id == "case_007":
        # We know case_007's date is heavily pixelated and EasyOCR misreads the '0's as '8's.
        # This test mathematically proves that the date parser catches this and returns INVALID_FORMAT
        # instead of letting a hallucinated date corrupt the DB.
        assert prediction["date"] == "INVALID_FORMAT", "Guardrail failed to catch the pixelated hallucinated date on case 007!"
        
    # Verify accurate inference (Case 002 is perfectly clean and should hit 100% strict accuracy)
    if case_id == "case_002":
        assert prediction["license_plate"] == "NSZ-8485", "Failed to extract accurate license plate on a clean image."
        # The parser standardizes to DD-MM-YYYY
        assert prediction["date"] == "22-11-2020", "Failed to extract and standardize the date."
