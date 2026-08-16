import os
import sys
import json
import time
import argparse
import jiwer
import re
from dateutil import parser

# Add src to the python path so imports resolve correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ocr_engine import OCREngine

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'exports', 'eval_progress.json')
REPORT_PATH = r"C:\Users\Radhe Shyam\.gemini\antigravity-ide\brain\1772646e-7ea3-47ba-b106-faba5f86ae5d\evaluation_report.md"

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

def generate_markdown_report(progress_data):
    valid_entity_count = len(progress_data)
    total_entity_acc = sum(d['entity_acc'] for d in progress_data.values() if d['entity_acc'] is not None)
    total_wer = sum(d['wer'] for d in progress_data.values() if d['wer'] is not None)
    
    valid_wer_count = sum(1 for d in progress_data.values() if d['wer'] is not None)
    
    avg_wer = (total_wer / valid_wer_count) if valid_wer_count > 0 else 0.0
    avg_entity_acc = (total_entity_acc / valid_entity_count) if valid_entity_count > 0 else 0.0

    report_lines = [
        "# 🏆 Final Certification Scores (Incremental)",
        "",
        f"- **Total Cases Evaluated:** {valid_entity_count} / 100",
        f"- **Global Entity Extraction Accuracy:** `{avg_entity_acc*100:.1f}%`",
        f"- **Global Word Error Rate (WER):** `{avg_wer*100:.2f}%`",
        "",
        "---",
        "",
        "# 📊 Police Forensics AI: Evaluation Report",
        "> This report is being generated incrementally to respect API quotas.",
        "",
        "| Case ID | Entity Accuracy | Word Error Rate (WER) |",
        "|---------|-----------------|-----------------------|"
    ]
    
    for case_id, metrics in progress_data.items():
        e_acc = f"{metrics['entity_acc']*100:.1f}%" if metrics['entity_acc'] is not None else "FAILED"
        w_err = f"{metrics['wer']*100:.1f}%" if metrics['wer'] is not None else "FAILED"
        report_lines.append(f"| `{case_id}` | {e_acc} | {w_err} |")

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

def main():
    parser_arg = argparse.ArgumentParser(description="Incrementally evaluate images to respect API limits.")
    parser_arg.add_argument('--batch', type=int, default=5, help="Number of images to process in this run.")
    args = parser_arg.parse_args()

    print("========================================")
    print(f"INITIATING INCREMENTAL EVALUATION ({args.batch} images)")
    print("========================================")
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'golden', 'data')
    engine = OCREngine()
    
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            progress_data = json.load(f)
    else:
        progress_data = {}
        
    all_cases = sorted([f.replace('_truth.json', '') for f in os.listdir(data_dir) if f.endswith('_truth.json')])
    remaining_cases = [c for c in all_cases if c not in progress_data]
    
    if not remaining_cases:
        print("All cases have already been evaluated! Report is fully generated.")
        generate_markdown_report(progress_data)
        return

    cases_to_process = remaining_cases[:args.batch]
    print(f"Found {len(remaining_cases)} remaining cases. Processing {len(cases_to_process)} now.")
    
    for i, case_id in enumerate(cases_to_process):
        json_path = os.path.join(data_dir, f"{case_id}_truth.json")
        img_path = os.path.join(data_dir, f"{case_id}.jpg")
        
        with open(json_path, 'r') as f:
            truth = json.load(f)
            
        print(f"[{i+1}/{len(cases_to_process)}] Evaluating {case_id}...")
        
        if not os.path.exists(img_path):
            print(f"    Warning: {img_path} not found. Skipping.")
            progress_data[case_id] = {'entity_acc': None, 'wer': None}
            continue
            
        try:
            prediction = engine.extract_entities(img_path)
            entity_acc = calculate_entity_accuracy(truth, prediction)
            
            truth_text = truth.get('raw_text', '')
            pred_text = prediction.get('raw_text', '')
            
            truth_norm = normalize_text(truth_text)
            pred_norm = normalize_text(pred_text)
            
            if truth_norm and pred_norm:
                error_rate = jiwer.wer(truth_norm, pred_norm)
            elif truth_norm and not pred_norm:
                error_rate = 1.0 # Missed completely
            else:
                error_rate = 0.0 # Both empty or truth is empty
                
            progress_data[case_id] = {'entity_acc': entity_acc, 'wer': error_rate}
            
        except Exception as e:
            print(f"    Failed on {case_id}: {e}")
            progress_data[case_id] = {'entity_acc': None, 'wer': None}
            
        # Save progress and report immediately after each case
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f, indent=4)
        generate_markdown_report(progress_data)
            
        if i < len(cases_to_process) - 1:
            time.sleep(15)
            
    print(f"\nBatch complete! {len(progress_data)} / {len(all_cases)} total cases finished.")
    print("Report has been safely updated.")

if __name__ == '__main__':
    main()
