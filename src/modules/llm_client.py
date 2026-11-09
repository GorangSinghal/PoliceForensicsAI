import os
import json
import re
import tenacity
from google import genai

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

class LLMClient:
    def __init__(self, model_name="gemini-3.6-flash"):
        self.model_name = model_name
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception:
                self.client = None
        else:
            self.client = None
        self.local_llm = None

    def update_api_key(self, new_key):
        """Hot-swaps the Gemini API key into the client memory without requiring a restart."""
        if new_key:
            try:
                self.client = genai.Client(api_key=new_key)
            except Exception:
                self.client = None

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(3),
        wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
        retry=tenacity.retry_if_exception_type(Exception),
        reraise=True
    )
    def call_gemini(self, processed_img_path, prompt):
        if not self.client:
            raise ValueError("GEMINI_API_KEY is not configured. Please set the environment variable or use offline mode.")
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

    def _load_local_llm(self, weights_dir):
        """Loads the .gguf model locally using llama-cpp-python, caching it in memory."""
        if self.local_llm is not None:
            return # Already loaded
            
        if Llama is None:
            raise ImportError("llama-cpp-python is not installed. Run 'pip install llama-cpp-python' to use local offline mode.")
            
        print("[LLM INIT] Searching for .gguf models in:", weights_dir)
        gguf_files = [f for f in os.listdir(weights_dir) if f.endswith('.gguf')]
        
        if not gguf_files:
            raise FileNotFoundError(f"No .gguf model found in {weights_dir}. Please download PoliceForensics_Llama3_8B.")
            
        # Prioritize the specific model if present, otherwise just grab the first one
        target_model = "llama-3-8b-instruct.Q4_K_M.gguf"
        if target_model in gguf_files:
            model_path = os.path.join(weights_dir, target_model)
        else:
            model_path = os.path.join(weights_dir, gguf_files[0])
            
        print(f"[LLM INIT] Booting local AI Engine: {model_path}...")
        print("[LLM INIT] Using 8GB RAM Safety Constraints (n_ctx=512, use_mmap=True)")
        
        self.local_llm = Llama(
            model_path=model_path,
            n_ctx=256,        # Extreme context reduction
            n_batch=8,        # Process tiny chunks to prevent RAM spikes
            n_threads=2,      # Limit thread context switching on older laptops
            use_mmap=True,    # Force SSD Virtual Memory
            verbose=True      # TURN ON LOGGING so we can see tokens/second!
        )
        print("[LLM INIT] Engine booted successfully!")

    def call_local_slm(self, raw_text, weights_dir):
        """Passes raw OCR text to the fine-tuned offline Llama 3 model."""
        self._load_local_llm(weights_dir)
        print(f"\n[SLM PARSING] Feeding Kraken text to local Offline GGUF Model...")
        
        # The exact prompt used during the LoRA fine-tuning process
        system_prompt = "You are a forensic OCR expert. Extract the following information from the provided police evidence RAW OCR TEXT. Return ONLY a valid JSON object."
        user_prompt = f"--- RAW OCR TEXT ---\n{raw_text}\n--- END RAW TEXT ---"
        
        # Llama 3 Chat Template formatting
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        print("[SLM PARSING] Waiting for inference generation...")
        
        # Generate JSON via Local Llama 3
        response = self.local_llm.create_chat_completion(
            messages=messages,
            max_tokens=300,
            temperature=0.0 # Strict deterministic output
        )
        
        response_text = response['choices'][0]['message']['content'].strip()
        
        # Parse the JSON explicitly
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(0)
            
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("[ERROR] Local SLM failed to return valid JSON.")
            print("Raw Output:", response_text)
            return {"license_plate": "", "date": "", "name": "", "raw_text": raw_text}
