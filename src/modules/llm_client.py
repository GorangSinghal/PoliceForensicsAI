import os
import json
import re
import requests
import tenacity
from google import genai

class LLMClient:
    def __init__(self, model_name="gemini-3.6-flash"):
        self.model_name = model_name
        # The new SDK takes the API key directly in the Client constructor.
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def update_api_key(self, new_key):
        """Hot-swaps the Gemini API key into the client memory without requiring a restart."""
        if new_key:
            self.client = genai.Client(api_key=new_key)

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception_type(Exception),
        reraise=True
    )
    def call_gemini(self, processed_img_path, prompt):
        # Upload to Gemini API using the new SDK
        sample_file = self.client.files.upload(file=processed_img_path)
        
        # Generate content using the new SDK
        # Set temperature=0.0 for deterministic, non-hallucinated extractions
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[sample_file, prompt],
            config=genai.types.GenerateContentConfig(
                temperature=0.0
            )
        )
        response_text = response.text.strip()
        
        # Cloud Mode Parse: Clean up JSON if necessary
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
        return json.loads(response_text.strip())

    def call_local_slm(self, raw_text, weights_dir):
        print(f"\n[SLM PARSING] Feeding Kraken text to local Language Model...")
        url = "http://localhost:11434/api/generate"
        
        # Check for PRO vs LITE weights in the folder
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
            
        response_text = response.json().get("response", "").strip()
        
        # Edge Mode Parse: Extract XML Tags via Regex
        extracted_data = {}
        plate_match = re.search(r'<license_plate>(.*?)</license_plate>', response_text, re.IGNORECASE | re.DOTALL)
        date_match = re.search(r'<date>(.*?)</date>', response_text, re.IGNORECASE | re.DOTALL)
        name_match = re.search(r'<name>(.*?)</name>', response_text, re.IGNORECASE | re.DOTALL)
        raw_match = re.search(r'<raw_text>(.*?)</raw_text>', response_text, re.IGNORECASE | re.DOTALL)
        
        extracted_data['license_plate'] = plate_match.group(1).strip() if plate_match else ""
        extracted_data['date'] = date_match.group(1).strip() if date_match else ""
        extracted_data['name'] = name_match.group(1).strip() if name_match else ""
        extracted_data['raw_text'] = raw_match.group(1).strip() if raw_match else ""
        
        return extracted_data
