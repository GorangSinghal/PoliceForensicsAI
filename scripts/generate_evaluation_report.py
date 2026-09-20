import os
import sys
import json
import time
import jiwer
import re

# Add src to the python path so imports resolve correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ocr_engine import OCREngine
from dateutil import parser

# Point this to the reports directory
REPORT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'evaluation_report.md'))

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_entity_accuracy(truth, prediction):
    total_entities = 0
    correct_entities = 0
    
    entities_to_check = ['license_plate', 'date', 'name']
    for entity in entities_to_check:
        if entity in truth and entity in prediction:
            total_entities += 1
            
            val_truth = truth[entity].strip().upper() if isinstance(truth[entity], str) else str(truth[entity])
            val_pred = prediction[entity].strip().upper() if isinstance(prediction[entity], str) else str(prediction[entity])
            
            if entity == 'date' and val_truth and val_pred:
                try:
                    date_truth = parser.parse(val_truth)
                    date_pred = parser.parse(val_pred, fuzzy=True, dayfirst=True)
                    if date_truth.date() == date_pred.date():
                        correct_entities += 1
                        continue
                except Exception:
                    pass
                    
            if val_truth == val_pred:
                correct_entities += 1
                
    return (correct_entities / total_entities) if total_entities > 0 else 0.0

def generate_report():
    print("========================================")
    print("INITIATING FAANG EVALUATION SUITE")
    print("========================================")
    print("Processing 100 cases. This will take ~25 minutes to respect Google's Rate Limits.")
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'golden', 'data')
    engine = OCREngine()
    
    total_wer = 0.0
    total_entity_acc = 0.0
    valid_wer_count = 0
    valid_entity_count = 0
    
    cases = [f for f in os.listdir(data_dir) if f.endswith('_truth.json')]
    total_cases = len(cases)
    
    report_lines = [
        "# 📊 Police Forensics AI: Final Evaluation Report",
        "> This report was automatically generated against the 100-Case Synthetic Golden Matrix.",
        "",
        "| Case ID | Entity Accuracy | Word Error Rate (WER) |",
        "|---------|-----------------|-----------------------|"
    ]
    
    for i, filename in enumerate(cases):
        case_id = filename.replace('_truth.json', '')
        json_path = os.path.join(data_dir, filename)
        img_path = os.path.join(data_dir, f"{case_id}.jpg")
        
        with open(json_path, 'r') as f:
            truth = json.load(f)
            
        print(f"[{i+1}/{total_cases}] Evaluating {case_id}...")
        
        # Guardrail: If file doesn't exist, skip it
        if not os.path.exists(img_path):
            print(f"    Warning: {img_path} not found. Skipping.")
            continue
            
        try:
            # 1. Real OCR Engine call
            prediction = engine.extract_entities(img_path)
            
            # 2. Calculate Entity Accuracy
            entity_acc = calculate_entity_accuracy(truth, prediction)
            total_entity_acc += entity_acc
            valid_entity_count += 1
            
            # 3. Calculate Word Error Rate (WER)
            truth_text = truth.get('raw_text', '')
            pred_text = prediction.get('raw_text', '')
            
            truth_norm = normalize_text(truth_text)
            pred_norm = normalize_text(pred_text)
            
            if truth_norm and pred_norm:
                error_rate = jiwer.wer(truth_norm, pred_norm)
                total_wer += error_rate
                valid_wer_count += 1
            elif truth_norm and not pred_norm:
                error_rate = 1.0 # Missed completely
                total_wer += error_rate
                valid_wer_count += 1
            else:
                error_rate = 0.0
                
            report_lines.append(f"| `{case_id}` | {entity_acc*100:.1f}% | {error_rate*100:.1f}% |")
            
        except Exception as e:
            print(f"    Failed on {case_id}: {e}")
            report_lines.append(f"| `{case_id}` | FAILED | FAILED |")
            
        # Write intermediate report so user can see progress!
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
            
        # SLEEP TO PREVENT QUOTA EXHAUSTION
        if i < total_cases - 1:
            time.sleep(15)
            
    # Calculate Final Averages
    avg_wer = (total_wer / valid_wer_count) if valid_wer_count > 0 else 0.0
    avg_entity_acc = (total_entity_acc / valid_entity_count) if valid_entity_count > 0 else 0.0
    
    # Prepend the summary header to the report
    summary = [
        "# 🏆 Final Certification Scores",
        "",
        f"- **Total Cases Evaluated:** {valid_entity_count}",
        f"- **Global Entity Extraction Accuracy:** `{avg_entity_acc*100:.1f}%`",
        f"- **Global Word Error Rate (WER):** `{avg_wer*100:.2f}%`",
        "",
        "---",
        ""
    ]
    
    final_report = summary + report_lines
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(final_report))
        
    print("\nEVALUATION COMPLETE! Report saved to artifacts.")

if __name__ == '__main__':
    generate_report()
