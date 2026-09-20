import os
import sys
import shutil
import json
import pandas as pd
from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import dotenv

# Fix path to import from same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ocr_engine import OCREngine

app = FastAPI(title="PoliceForensicsAI - AEGIS Protocol API")

# Setup CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(EXPORTS_DIR, exist_ok=True)

app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")
app.mount("/exports", StaticFiles(directory=EXPORTS_DIR), name="exports")

# Initialize Engine globally as None to prevent laptop hanging on boot
engine = None

def get_engine():
    global engine
    if engine is None:
        # Load heavy PyTorch models only when a user actually requests an extraction
        engine = OCREngine()
    return engine

# Load env variables for API key detection
dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

class StatusResponse(BaseModel):
    mode: str
    message: str
    has_api_key: bool

@app.get("/api/status", response_model=StatusResponse)
def get_status():
    weights_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    pro_mode = False
    for f in os.listdir(weights_dir):
        if f.endswith(".gguf") and os.path.getsize(os.path.join(weights_dir, f)) > 3 * 1024 * 1024 * 1024:
            pro_mode = True
            break
            
    has_key = bool(os.getenv("GEMINI_API_KEY"))
            
    if pro_mode:
        return StatusResponse(mode="PRO", message="PRO MODE (Llama 8B Active)", has_api_key=has_key)
    return StatusResponse(mode="LITE", message="LITE MODE (TinyLlama 1B Active)", has_api_key=has_key)

@app.post("/api/extract")
async def extract_evidence(
    file: UploadFile = File(...),
    use_codeformer: str = Form("false"),
    llm_provider: str = Form("gemini"),
    api_key: Optional[str] = Form(None)
):
    try:
        # Save uploaded file to assets
        file_path = os.path.join(ASSETS_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        import hashlib
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
            
        use_cf = use_codeformer.lower() == "true"
        
        # Instantiate the engine lazily
        current_engine = get_engine()
        
        # Handle API Key
        if api_key and api_key != os.getenv("GEMINI_API_KEY"):
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
            dotenv.set_key(env_path, "GEMINI_API_KEY", api_key)
            os.environ["GEMINI_API_KEY"] = api_key
            current_engine.update_api_key(api_key)
            
        # Process image
        json_data, processed_img_path = current_engine.extract_entities(
            file_path,
            use_codeformer=use_cf,
            return_image_path=True,
            llm_provider=llm_provider
        )
        
        # Generate Exports
        json_path = os.path.join(EXPORTS_DIR, "forensics_report.json")
        csv_path = os.path.join(EXPORTS_DIR, "forensics_report.csv")
        excel_path = os.path.join(EXPORTS_DIR, "forensics_report.xlsx")
        
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=4)
            
        df = pd.DataFrame([json_data])
        df.to_csv(csv_path, index=False)
        try:
            df.to_excel(excel_path, index=False)
        except Exception:
            # Fallback if openpyxl is missing
            pass
            
        # Convert absolute path to relative URL
        img_filename = os.path.basename(processed_img_path)
        img_url = f"/assets/{img_filename}"
        
        return {
            "status": "success",
            "extracted_data": json_data,
            "processed_image_url": img_url,
            "file_hash": file_hash,
            "exports": {
                "json": "/exports/forensics_report.json",
                "csv": "/exports/forensics_report.csv",
                "excel": "/exports/forensics_report.xlsx"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images/{filename}")
async def get_image(filename: str):
    # This serves the image directly to the React frontend
    # Depending on whether CodeFormer was used, it might be in different folders, 
    # but the engine returns absolute paths, so we should map it securely.
    
    # For now, let's assume images are in the UPLOADS_DIR or CodeFormer results dir.
    # To keep it simple and secure, we'll search a few known paths.
    
    possible_paths = [
        os.path.join(UPLOADS_DIR, filename),
        os.path.join(BASE_DIR, "..", "third_party", "CodeFormer", "results", "test_img_1.0", "final_results", filename),
        os.path.join(BASE_DIR, "..", "golden", "data", filename.replace("_processed", "")) # Fallback
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)
            
    # If we still can't find it, we'll try a generic fallback for processed images
    processed_temp_path = os.path.join(UPLOADS_DIR, filename)
    if os.path.exists(processed_temp_path):
        return FileResponse(processed_temp_path)
        
    raise HTTPException(status_code=404, detail="Image not found")
