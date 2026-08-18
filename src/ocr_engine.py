import os
import re
import json
import cv2
import numpy as np
from google import genai
from modules.codeformer_bridge import CodeFormerBridge
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class OCREngine:
    def __init__(self, model_name="gemini-1.5-flash"):
        # The new SDK takes the API key directly in the Client constructor.
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = model_name
        self.codeformer = CodeFormerBridge(
            codeformer_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "third_party", "CodeFormer")
        )
        
    def update_api_key(self, new_key):
        """Hot-swaps the Gemini API key into the client memory without requiring a restart."""
        if new_key:
            self.client = genai.Client(api_key=new_key)
        
    def preprocess_image(self, image_path):
        """
        Uses OpenCV to preprocess the image and optionally extract bounding boxes.
        For now, we will perform basic grayscale and contrast enhancement to help the LLM.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Avoid brittle hardcoded adaptive thresholds which fail on flash photography.
        # Instead, use robust min-max normalization to maximize contrast globally.
        processed = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        
        # Save temporary processed image for the LLM
        temp_path = image_path.replace(".jpg", "_processed.jpg")
        cv2.imwrite(temp_path, processed)
        return temp_path

    def _validate_license_plate(self, plate):
        """Deterministic Guardrail for License Plates"""
        if not plate:
            return None
        # Allow alphanumeric, hyphens, and spaces.
        clean_plate = re.sub(r'[^A-Z0-9\-\s]', '', plate.upper()).strip()
        # Widen the length constraint to avoid rejecting foreign/special plates
        if len(clean_plate) >= 4 and len(clean_plate) <= 12:
            return clean_plate
        return "INVALID_FORMAT"

    def _validate_date(self, date_str):
        """Deterministic Guardrail for Dates (Robust parsing, India default DD-MM-YYYY)"""
        if not date_str:
            return None
        
        try:
            from dateutil import parser
            # dayfirst=True ensures ambiguous dates (like 10/11/2023) are treated as DD/MM/YYYY (India Standard)
            parsed_date = parser.parse(date_str, fuzzy=True, dayfirst=True)
            # Standardize output format
            return parsed_date.strftime("%d-%m-%Y")
        except Exception:
            return "INVALID_FORMAT"

    def extract_entities(self, image_path, use_codeformer=False, return_image_path=False, llm_provider="gemini"):
        """
        Main extraction pipeline (Kraken + SLM).
        1. Preprocess Image (CodeFormer GAN)
        2. Kraken OCR Extraction (Vision)
        3. Local SLM Extraction (NLP Parsing)
        4. Deterministic Guardrails
        """
        if use_codeformer:
            processed_img_path = self.codeformer.enhance_image(image_path)
        else:
            processed_img_path = self.preprocess_image(image_path)
        
        # 2. LLM Extraction
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
        
        import tenacity
        
        @tenacity.retry(
            stop=tenacity.stop_after_attempt(3),
            wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
            retry=tenacity.retry_if_exception_type(Exception),
            reraise=True
        )
        def call_gemini():
            # Upload to Gemini API using the new SDK
            sample_file = self.client.files.upload(file=processed_img_path)
            
            # Generate content using the new SDK
            # Set temperature=0.0 for deterministic, non-hallucinated extractions
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=[sample_file, prompt],
                config=genai.types.GenerateContentConfig(
                    temperature=0.0
                )
            )
            return response.text.strip()
        
        def run_easyocr(img_path):
            import easyocr
            print("\n[EASYOCR] Reading pixels...")
            # We initialize EasyOCR in English mode
            reader = easyocr.Reader(['en'], verbose=False)
            # Detail=0 returns just a list of text strings
            results = reader.readtext(img_path, detail=0)
            return "\n".join(results)

        def call_local_slm(raw_text):
            import requests
            print(f"\n[SLM PARSING] Feeding Kraken text to local Language Model...")
            url = "http://localhost:11434/api/generate"
            
            # Check for PRO vs LITE weights in the folder
            weights_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weights")
            pro_mode = any(f.endswith('.gguf') and os.path.getsize(os.path.join(weights_dir, f)) > 3 * 1024 * 1024 * 1024 for f in os.listdir(weights_dir)) if os.path.exists(weights_dir) else False
            
            slm_model = "llama3" if pro_mode else "llama3.2:1b"
            
            # Use XML Structured Tags for smaller edge models to prevent JSON corruption
            xml_prompt = """
            You are a forensic OCR expert. Extract the following information from the provided police evidence RAW OCR TEXT.
            Do not write any conversational text. ONLY return the requested XML tags populated with the extracted data.
            Format your output exactly like this:
            <license_plate></license_plate>
            <date></date>
            <name></name>
            <raw_text></raw_text> <!-- YOU MUST COPY THE ENTIRE RAW OCR TEXT HERE VERBATIM. DO NOT SUMMARIZE. DO NOT TRUNCATE. -->
            """
            
            slm_prompt = xml_prompt + f"\n\n--- RAW OCR TEXT ---\n{raw_text}\n--- END RAW TEXT ---"
            
            payload = {
                "model": slm_model,
                "prompt": slm_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "num_predict": 500,
                    "repeat_penalty": 1.1
                }
            }
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code != 200:
                raise Exception(f"SLM Server returned {response.status_code}: {response.text}")
            return response.json().get("response", "").strip()
            
        try:
            if llm_provider == "gemini":
                response_text = call_gemini()
                
                # Cloud Mode Parse: Clean up JSON if necessary
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    response_text = json_match.group(0)
                extracted_data = json.loads(response_text.strip())
                
            else:
                # Offline Edge Mode
                # Step 1: EasyOCR extracts text
                ocr_text = run_easyocr(processed_img_path)
                
                # Step 2: SLM parses into XML Tags
                response_text = call_local_slm(ocr_text)
                
                # Edge Mode Parse: Extract XML Tags via Regex
                import re
                extracted_data = {}
                plate_match = re.search(r'<license_plate>(.*?)</license_plate>', response_text, re.IGNORECASE | re.DOTALL)
                date_match = re.search(r'<date>(.*?)</date>', response_text, re.IGNORECASE | re.DOTALL)
                name_match = re.search(r'<name>(.*?)</name>', response_text, re.IGNORECASE | re.DOTALL)
                raw_match = re.search(r'<raw_text>(.*?)</raw_text>', response_text, re.IGNORECASE | re.DOTALL)
                
                extracted_data['license_plate'] = plate_match.group(1).strip() if plate_match else ""
                extracted_data['date'] = date_match.group(1).strip() if date_match else ""
                extracted_data['name'] = name_match.group(1).strip() if name_match else ""
                extracted_data['raw_text'] = raw_match.group(1).strip() if raw_match else ""

            
        except Exception as e:
            print(f"Extraction failed: {e}")
            extracted_data = {}
            
        # Clean up temporary processed image ONLY if we aren't returning it to the UI
        if not return_image_path and os.path.exists(processed_img_path):
            os.remove(processed_img_path)
            
        # 3. Deterministic Guardrails
        if 'license_plate' in extracted_data:
            extracted_data['license_plate'] = self._validate_license_plate(extracted_data['license_plate'])
            
        if 'date' in extracted_data:
            extracted_data['date'] = self._validate_date(extracted_data['date'])
            
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
