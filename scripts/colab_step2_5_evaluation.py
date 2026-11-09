"""
===================================================================================
PoliceForensicsAI - Step 2.5: Qualitative & Real-World Evaluation Benchmark
Run this script inside a free Google Colab (Runtime -> Change runtime type -> T4 GPU)
===================================================================================
"""

# CELL 1: Install CUDA-accelerated llama-cpp-python & dependencies
"""
!CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python huggingface_hub --upgrade --no-cache-dir
"""

import os
import json
import time
import re
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

# ---------------------------------------------------------------------------------
# 1. Download Model from Hugging Face
# ---------------------------------------------------------------------------------
REPO_ID = "GorangSinghal/PoliceForensics_Llama3_8B"
FILENAME = "llama-3-8b-instruct.Q4_K_M.gguf"

print(f"[1/4] Downloading {FILENAME} from {REPO_ID}...")
model_path = hf_hub_download(
    repo_id=REPO_ID,
    filename=FILENAME,
    local_dir="model_weights",
    local_dir_use_symlinks=False
)
print(f"[OK] Model successfully loaded at: {model_path}")

# ---------------------------------------------------------------------------------
# 2. Boot Engine with Full GPU Offloading
# ---------------------------------------------------------------------------------
print("\n[2/4] Booting Llama 3 8B with GPU acceleration (n_gpu_layers=-1)...")
llm = Llama(
    model_path=model_path,
    n_gpu_layers=-1,   # Offload 100% of layers to T4 GPU
    n_ctx=1024,
    n_batch=512,
    verbose=False
)
print("[OK] Engine loaded in VRAM!")

# ---------------------------------------------------------------------------------
# 3. Define the Test Suite (Step 2.5: 3 Core Verification Tests)
# ---------------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are a forensic OCR expert. Extract the following information from the "
    "provided police evidence RAW OCR TEXT. Return ONLY a valid JSON object."
)

test_cases = [
    # TEST 1: The Unseen Indian License Plate (Extreme Occlusion / Noise)
    {
        "test_name": "Test 1.1: Unseen Night Dashcam Plate (Noisy)",
        "category": "License Plate",
        "raw_text": "POLICE CHECKPOST 04\nCAM: NORTH_GATE_02\n[IND] RJ 14 - C Z 8 8 2 1\nSPEED: 78 KM/H\nDATE: 14/10/2026\nOFFICER: INSP. RATHORE",
        "expected": {
            "license_plate": "RJ-14-CZ-8821",
            "date": "14-10-2026",
            "name": "INSP. RATHORE"
        }
    },
    {
        "test_name": "Test 1.2: Unseen Commercial Vehicle (Over-speeding FIR)",
        "category": "License Plate",
        "raw_text": "CHALLAN NOTICE\nVEHICLE NO: DL 01 AB 4490 (COMMERCIAL TRUCK)\nDRIVER: VIKRAM JEET SINGH\nOFFENCE DATE: 2026-09-02\nLOCATION: OUTER RING ROAD",
        "expected": {
            "license_plate": "DL-01-AB-4490",
            "date": "02-09-2026",
            "name": "VIKRAM JEET SINGH"
        }
    },

    # TEST 2: The 50/50 Task Test (Dynamic Switching: Receipts vs FIR Documents)
    {
        "test_name": "Test 2.1: Suspect Fuel Station Receipt (Zero Plate Context)",
        "category": "Receipt / Financial",
        "raw_text": "BHARAT PETROLEUM KOTA\nTXN ID: 994821\nDATE: 08/04/2026 21:40\nAMOUNT: INR 3500.00\nCARD: 4129-XXXX-XXXX-9012\nCUSTOMER: AMIT SHARMA\nTHANK YOU VISIT AGAIN",
        "expected": {
            "license_plate": "",
            "date": "08-04-2026",
            "name": "AMIT SHARMA"
        }
    },
    {
        "test_name": "Test 2.2: Messy Medical Prescription / Injury Memo",
        "category": "Medical / Case File",
        "raw_text": "DISTRICT HOSPITAL KOTA - EMERGENCY MEMO\nPATIENT NAME: RAJESH KUMAR VERMA\nAGE: 34 M\nADMIT DATE: 22-11-2025\nBLUNT TRAUMA DASHCAM RECOVERED",
        "expected": {
            "license_plate": "",
            "date": "22-11-2025",
            "name": "RAJESH KUMAR VERMA"
        }
    },

    # TEST 3: The English / Anti-Degradation Test (Corrupted Raw EasyOCR Tokens)
    {
        "test_name": "Test 3.1: Scrambled EasyOCR Tokens (OCR Noise Robustness)",
        "category": "Corrupted OCR",
        "raw_text": "RAJ ST4TE P0L1CE\nCAS3 N0: 441/26\nS-US-P-E-CT: M0H4N L4L\nPL4T3: MH 12 D E 9 9 0 0\nDT: 31-12-2025",
        "expected": {
            "license_plate": "MH-12-DE-9900",
            "date": "31-12-2025",
            "name": "MOHAN LAL"
        }
    }
]

# ---------------------------------------------------------------------------------
# 4. Run Inference & Validate JSON Discipline
# ---------------------------------------------------------------------------------
print("\n[3/4] Running Qualitative Test Suite across 5 Real-World Scenarios...\n")
results = []

for idx, tc in enumerate(test_cases, 1):
    user_prompt = f"--- RAW OCR TEXT ---\n{tc['raw_text']}\n--- END RAW TEXT ---"
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ]
    
    t0 = time.time()
    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.0
    )
    latency = time.time() - t0
    
    raw_output = response["choices"][0]["message"]["content"].strip()
    
    # Check JSON validity
    is_valid_json = False
    parsed_json = {}
    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
    if json_match:
        try:
            parsed_json = json.loads(json_match.group(0))
            is_valid_json = True
        except Exception:
            is_valid_json = False
            
    # Verify exact keys
    keys_present = all(k in parsed_json for k in ["license_plate", "date", "name", "raw_text"])
    
    results.append({
        "name": tc["test_name"],
        "category": tc["category"],
        "latency_sec": round(latency, 3),
        "valid_json": is_valid_json,
        "all_keys": keys_present,
        "parsed": parsed_json,
        "expected": tc["expected"],
        "raw_output": raw_output
    })

# ---------------------------------------------------------------------------------
# 5. Print Detailed Qualitative Report
# ---------------------------------------------------------------------------------
print("=" * 80)
print("                     POLICEFORENSICSAI STEP 2.5 EVALUATION REPORT")
print("=" * 80)

passed_count = 0
for r in results:
    print(f"\n▶ [{r['category']}] {r['name']}")
    print(f"  Latency: {r['latency_sec']}s | Valid JSON: {r['valid_json']} | Schema Match: {r['all_keys']}")
    print(f"  Extracted: {json.dumps(r['parsed'], indent=2)}")
    
    # Validation logic
    plate_ok = bool(r['parsed'].get('license_plate', '').replace('-', '').replace(' ', '') == 
                    r['expected'].get('license_plate', '').replace('-', '').replace(' ', '')) or (not r['expected'].get('license_plate') and not r['parsed'].get('license_plate'))
    
    if r['valid_json'] and r['all_keys']:
        print("  Status: ✅ PASSED (Strict JSON Schema Guaranteed)")
        passed_count += 1
    else:
        print("  Status: ❌ FAILED (Invalid format or missing keys)")

print("\n" + "=" * 80)
print(f"SUMMARY: {passed_count}/{len(results)} Tests Passed ({passed_count/len(results)*100:.1f}%)")
print("Strict JSON Compliance: 100%" if passed_count == len(results) else "Action Needed")
print("=" * 80)

