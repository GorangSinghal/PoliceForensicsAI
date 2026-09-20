import os
import json
from dotenv import load_dotenv

from modules.codeformer_bridge import CodeFormerBridge
from modules.image_preprocessor import ImagePreprocessor
from modules.vision_module import VisionModule
from modules.llm_client import LLMClient
from modules.data_validator import DataValidator

# Load environment variables
load_dotenv()

class OCREngine:
    def __init__(self, model_name="gemini-3.6-flash"):
        self.llm_client = LLMClient(model_name=model_name)
        self.codeformer = CodeFormerBridge(
            codeformer_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "third_party", "CodeFormer")
        )
        
    def update_api_key(self, new_key):
        """Hot-swaps the Gemini API key into the client memory without requiring a restart."""
        self.llm_client.update_api_key(new_key)
        
    def extract_entities(self, image_path, use_codeformer=False, return_image_path=False, llm_provider="gemini"):
        """
        Main extraction pipeline orchestrator (Kraken + SLM).
        1. Preprocess Image
        2. LLM / SLM Extraction
        3. Deterministic Guardrails
        """
        # 1. Preprocess Image
        if use_codeformer:
            processed_img_path = self.codeformer.enhance_image(image_path)
        else:
            processed_img_path = ImagePreprocessor.preprocess_image(image_path)
            
        prompt = """
        You are a forensic OCR expert. Extract the following information from the provided police evidence image:
        - license_plate (string)
        - date (string in DD-MM-YYYY format)
        - name (string)
        - raw_text (the complete transcribed text exactly as it appears)
        
        Return ONLY a valid JSON object. Do not include markdown formatting or backticks.
        Example output:
        {
            "license_plate": "ABC-1234",
            "date": "27-10-2023",
            "name": "JOHN DOE",
            "raw_text": "SUSPECT VEHICLE REPORT..."
        }
        """
        
        # 2. Extract Data
        extracted_data = {}
        try:
            if llm_provider == "gemini":
                extracted_data = self.llm_client.call_gemini(processed_img_path, prompt)
            else:
                ocr_text = VisionModule.run_easyocr(processed_img_path)
                weights_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weights")
                extracted_data = self.llm_client.call_local_slm(ocr_text, weights_dir)
                
        except Exception as e:
            # PII Security: We log the generic failure, but we MUST raise the actual exception 
            # so the FastAPI backend knows the API call failed (e.g., Invalid API Key) 
            # instead of silently returning empty data and hanging the UI with retries.
            print(f"Extraction failed: {str(e)}")
            if os.path.exists(processed_img_path) and not return_image_path:
                os.remove(processed_img_path)
            raise RuntimeError(f"OCR Engine Failure: {str(e)}")
            
        # Clean up temporary processed image ONLY if we aren't returning it to the UI
        if not return_image_path and os.path.exists(processed_img_path):
            os.remove(processed_img_path)
            
        # 3. Deterministic Guardrails
        if 'license_plate' in extracted_data:
            extracted_data['license_plate'] = DataValidator.validate_license_plate(extracted_data['license_plate'])
            
        if 'date' in extracted_data:
            extracted_data['date'] = DataValidator.validate_date(extracted_data['date'])
            
        # Ensure base structure is present
        final_dict = {
            "license_plate": extracted_data.get("license_plate", ""),
            "date": extracted_data.get("date", ""),
            "name": extracted_data.get("name", ""),
            "raw_text": extracted_data.get("raw_text", "")
        }
        
        if return_image_path:
            return final_dict, processed_img_path
        return final_dict

if __name__ == "__main__":
    # Test block
    engine = OCREngine()
    # Resolve absolute path based on this file's location
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_image = os.path.join(base_dir, "golden", "data", "case_005_real.jpg")
    
    if os.path.exists(test_image):
        print(f"Testing OCR on {test_image}...")
        result = engine.extract_entities(test_image)
        print(json.dumps(result, indent=4))
    else:
        print(f"Test image not found: {test_image}")
