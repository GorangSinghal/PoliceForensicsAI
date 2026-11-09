import os
import json
import glob
import random
import re
import cv2
import numpy as np
from tqdm import tqdm
import easyocr

# Directories
SROIE_DIR = os.path.join("data", "sroie")
INDIAN_PLATES_DIR = os.path.join("data", "indian_plates")
OUTPUT_JSONL = os.path.join("data", "dataset.jsonl")

def parse_sroie_ground_truth(box_file_path):
    extracted_text = []
    try:
        with open(box_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 9:
                    text = ','.join(parts[8:])
                    extracted_text.append(text)
    except:
        pass
    return {"license_plate": "", "date": "", "name": "", "raw_text": "\n".join(extracted_text)}

def format_record(messy_text, ground_truth_json):
    system_prompt = "You are a forensic OCR expert. Extract the following information from the provided police evidence RAW OCR TEXT. Return ONLY a valid JSON object."
    user_prompt = f"--- RAW OCR TEXT ---\n{messy_text}\n--- END RAW TEXT ---"
    assistant_response = json.dumps(ground_truth_json, ensure_ascii=False)
    
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_response}
        ]
    }

def resize_for_ocr(img_path):
    """Resizes large images to max 800px to speed up CPU OCR by 10x."""
    img = cv2.imread(img_path)
    if img is None: return None
    h, w = img.shape[:2]
    max_dim = 800
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return img

def apply_severe_augmentation(img_path):
    """Applies FAANG-level mathematical degradation to simulate weather/physics."""
    img = resize_for_ocr(img_path)
    if img is None: return None
    
    choice = random.randint(1, 5)
    if choice == 1:
        # Medium Motion Blur (Highway speed simulation)
        kernel_size = 13
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
        kernel /= kernel_size
        img = cv2.filter2D(img, -1, kernel)
    elif choice == 2:
        # Dim Light (Dusk/Dawn Simulation, not pitch black)
        img = cv2.convertScaleAbs(img, alpha=0.5, beta=30)
    elif choice == 3:
        # Mild Noise (Standard dashcam grain)
        row, col, ch = img.shape
        gauss = np.random.normal(0, 15, (row, col, ch))
        noisy = img + gauss
        img = np.clip(noisy, 0, 255).astype(np.uint8)
    elif choice == 4:
        # Light Glare (Daylight overexposure, not blinding headlight)
        img = cv2.convertScaleAbs(img, alpha=1.2, beta=30)
    else:
        # Light Drizzle (Fewer lines, less blur)
        row, col, ch = img.shape
        for _ in range(30):
            x1 = random.randint(0, col-1)
            y1 = random.randint(0, row-1)
            x2 = x1 + random.randint(-2, 2)
            y2 = y1 + random.randint(5, 12)
            cv2.line(img, (x1, y1), (x2, y2), (200, 200, 200), 1)
        
    return img

def process_sroie(reader, limit=1000):
    records = []
    img_files = glob.glob(os.path.join(SROIE_DIR, "**", "*.jpg"), recursive=True)
    random.seed(42)
    random.shuffle(img_files)
    img_files = img_files[:limit]
    
    for img_path in tqdm(img_files, desc="SROIE Receipts"):
        basename = os.path.basename(img_path)
        txt_basename = basename.replace(".jpg", ".txt")
        box_path = None
        
        same_dir_txt = img_path.replace(".jpg", ".txt")
        if os.path.exists(same_dir_txt):
            box_path = same_dir_txt
        else:
            parent_dir = os.path.dirname(img_path)
            if os.path.basename(parent_dir) == "img":
                box_dir = os.path.join(os.path.dirname(parent_dir), "box")
                possible_path = os.path.join(box_dir, txt_basename)
                if os.path.exists(possible_path):
                    box_path = possible_path
                    
        if not box_path: continue
        
        ground_truth = parse_sroie_ground_truth(box_path)
        img = resize_for_ocr(img_path)
        if img is None: continue
        try:
            results = reader.readtext(img, detail=0)
            messy_ocr = "\n".join(results)
        except:
            messy_ocr = ""
            
        records.append(format_record(messy_ocr, ground_truth))
    return records

def process_indian_plates(reader, clean_limit=500, augmented_limit=500):
    records = []
    
    labels_file = os.path.join(INDIAN_PLATES_DIR, "train_labels.txt")
    img_folder = os.path.join(INDIAN_PLATES_DIR, "images", "train")
    
    if not os.path.exists(labels_file):
        print("Could not find train_labels.txt!")
        return records
        
    with open(labels_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    random.seed(42)
    random.shuffle(lines)
    
    total_needed = clean_limit + augmented_limit
    selected_lines = lines[:total_needed]
    
    # 1. Process 500 Clean Plates (Strict Syntax Training)
    for line in tqdm(selected_lines[:clean_limit], desc="Indian Plates (Clean)"):
        parts = line.strip().split("\t")
        if len(parts) != 2: continue
        
        filename, true_text = parts[0], parts[1]
        img_path = os.path.join(img_folder, filename)
        if not os.path.exists(img_path): continue
        
        clean_true_text = re.sub(r'[^A-Za-z0-9]', '', true_text)
        if not clean_true_text: continue
        
        ground_truth = {"license_plate": clean_true_text, "date": "", "name": "", "raw_text": clean_true_text}
        
        img = resize_for_ocr(img_path)
        if img is None: continue
        try:
            results = reader.readtext(img, detail=0)
            messy_ocr = "\n".join(results)
            messy_ocr = re.sub(r'[^A-Za-z0-9\s]', '', messy_ocr).strip()
        except:
            messy_ocr = ""
        records.append(format_record(messy_ocr, ground_truth))
        
    # 2. Process 500 Augmented Plates (Extreme Weather Resilience)
    for line in tqdm(selected_lines[clean_limit:], desc="Indian Plates (Extreme Weather)"):
        parts = line.strip().split("\t")
        if len(parts) != 2: continue
        
        filename, true_text = parts[0], parts[1]
        img_path = os.path.join(img_folder, filename)
        if not os.path.exists(img_path): continue
        
        clean_true_text = re.sub(r'[^A-Za-z0-9]', '', true_text)
        if not clean_true_text: continue
        
        ground_truth = {"license_plate": clean_true_text, "date": "", "name": "", "raw_text": clean_true_text}
        
        degraded_img = apply_severe_augmentation(img_path)
        if degraded_img is None: continue
            
        try:
            results = reader.readtext(degraded_img, detail=0)
            messy_ocr = "\n".join(results)
            messy_ocr = re.sub(r'[^A-Za-z0-9\s]', '', messy_ocr).strip()
        except:
            messy_ocr = ""
            
        records.append(format_record(messy_ocr, ground_truth))
        
    return records

def build_dataset():
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    
    print("[1/3] Initializing EasyOCR Reader (English)...")
    # Dropped ch_sim since we are no longer using CCPD
    reader = easyocr.Reader(['en'], verbose=False, quantize=True)
    
    all_records = []
    
    print("\n[2/3] Extracting Dataset Text...")
    if os.path.exists(SROIE_DIR):
        all_records.extend(process_sroie(reader, 1000))
    else:
        print(f"Skipping SROIE: Not found at {SROIE_DIR}")
        
    if os.path.exists(INDIAN_PLATES_DIR):
        all_records.extend(process_indian_plates(reader, 500, 500))
    else:
        print(f"Skipping Indian Plates: Not found at {INDIAN_PLATES_DIR}")
        
    print(f"\n[3/3] Writing {len(all_records)} records to {OUTPUT_JSONL}...")
    with open(OUTPUT_JSONL, 'w', encoding='utf-8') as f:
        for r in all_records:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            
    print(f"Dataset generation complete! File saved at {OUTPUT_JSONL}")

if __name__ == "__main__":
    build_dataset()
