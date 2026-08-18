import os
import sys
import json
import time
import argparse
import jiwer
import re
from dateutil import parser
from difflib import SequenceMatcher

# Add src to the python path so imports resolve correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ocr_engine import OCREngine

PROGRESS_FILE = os.path.join(os.path.dirname(__file__), '..', 'exports', 'eval_offline_progress.json')
REPORT_PATH = r"C:\Users\Radhe Shyam\.gemini\antigravity-ide\brain\1772646e-7ea3-47ba-b106-faba5f86ae5d\offline_evaluation_report.md"

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_entity_accuracy(truth, prediction):
    total_entities = 0
    strict_correct = 0
    fuzzy_correct = 0
    total_similarity = 0.0
    
    entities_to_check = ['license_plate', 'date', 'name']
    for entity in entities_to_check:
        if entity in truth and entity in prediction:
            total_entities += 1
            
            val_truth = str(truth[entity]).strip().upper() if truth[entity] else ""
            val_pred = str(prediction[entity]).strip().upper() if prediction[entity] else ""
            
            # Date Handling
            if entity == 'date' and val_truth and val_pred:
                try:
                    date_truth = parser.parse(val_truth)
                    date_pred = parser.parse(val_pred, fuzzy=True, dayfirst=True)
                    
                    # Direct Match
                    if date_truth.date() == date_pred.date():
                        strict_correct += 1
                        fuzzy_correct += 1
                        total_similarity += 1.0
                        continue
                        
                    # Anagram Match (e.g. 07-02-2006 vs 2006-07-02)
                    # Compares the unordered sets of {Year, Month, Day}
                    elif {date_truth.year, date_truth.month, date_truth.day} == {date_pred.year, date_pred.month, date_pred.day}:
                        strict_correct += 1
                        fuzzy_correct += 1
                        total_similarity += 1.0
                        continue
                        
                except Exception:
                    pass
            
            # String Handling
            if val_truth == val_pred:
                strict_correct += 1
                fuzzy_correct += 1
                total_similarity += 1.0
            else:
                # Calculate Character Similarity (1.0 - CER)
                if val_truth:
                    similarity = SequenceMatcher(None, val_truth, val_pred).ratio()
                else:
                    similarity = 0.0
                    
                total_similarity += similarity
                
                # If more than 75% characters match, it's a Fuzzy Match
                if similarity >= 0.75:
                    fuzzy_correct += 1
                
    strict_acc = (strict_correct / total_entities) if total_entities > 0 else 0.0
    fuzzy_acc = (fuzzy_correct / total_entities) if total_entities > 0 else 0.0
    avg_sim = (total_similarity / total_entities) if total_entities > 0 else 0.0
    
    return strict_acc, fuzzy_acc, avg_sim

def generate_markdown_report(progress_data):
    valid_entity_count = len(progress_data)
    
    total_strict = sum(d['strict_acc'] for d in progress_data.values() if d['strict_acc'] is not None)
    total_fuzzy = sum(d['fuzzy_acc'] for d in progress_data.values() if d['fuzzy_acc'] is not None)
    total_sim = sum(d['avg_sim'] for d in progress_data.values() if d['avg_sim'] is not None)
    
    avg_strict = (total_strict / valid_entity_count) if valid_entity_count > 0 else 0.0
    avg_fuzzy = (total_fuzzy / valid_entity_count) if valid_entity_count > 0 else 0.0
    avg_sim = (total_sim / valid_entity_count) if valid_entity_count > 0 else 0.0

    report_lines = [
        "# 🏆 Final Certification Scores (Incremental)",
        "",
        f"- **Total Cases Evaluated:** {valid_entity_count} / 100",
        f"- **Strict Entity Accuracy (100% Match):** `{avg_strict*100:.1f}%`",
        f"- **Fuzzy Entity Accuracy (>= 75% Match):** `{avg_fuzzy*100:.1f}%`",
        f"- **Average Character Similarity (1 - CER):** `{avg_sim*100:.1f}%`",
        "",
        "---",
        "",
        "# 📊 Police Forensics AI: Evaluation Report",
        "> This report is being generated incrementally to respect hardware limits.",
        "",
        "| Case ID | Strict Accuracy | Fuzzy Accuracy (>75%) | Character Similarity |",
        "|---------|-----------------|-----------------------|----------------------|"
    ]
    
    for case_id, metrics in progress_data.items():
        s_acc = f"{metrics['strict_acc']*100:.1f}%" if metrics['strict_acc'] is not None else "FAILED"
        f_acc = f"{metrics['fuzzy_acc']*100:.1f}%" if metrics['fuzzy_acc'] is not None else "FAILED"
        c_sim = f"{metrics['avg_sim']*100:.1f}%" if metrics['avg_sim'] is not None else "FAILED"
        report_lines.append(f"| `{case_id}` | {s_acc} | {f_acc} | {c_sim} |")

    report_lines.extend(["", "---", "", "## 🔍 Detailed Extraction Logs (Truth vs Output JSON)", ""])

    for case_id, metrics in progress_data.items():
        report_lines.append(f"### {case_id}")
        report_lines.append("| Ground Truth | LITE Mode Prediction (Output) |")
        report_lines.append("|--------------|-------------------------------|")
        
        truth_json = json.dumps(metrics.get('truth', {}), indent=2).replace('\n', '<br>')
        pred_json = json.dumps(metrics.get('prediction', {}), indent=2).replace('\n', '<br>')
        
        report_lines.append(f"| `<pre>{truth_json}</pre>` | `<pre>{pred_json}</pre>` |")
        report_lines.append("")

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

def main():
    parser_arg = argparse.ArgumentParser(description="Incrementally evaluate images to respect API limits.")
    parser_arg.add_argument('--batch', type=int, default=5, help="Number of images to process in this run.")
    parser_arg.add_argument('--llm', type=str, default='gemini', help="LLM backend to use (gemini or offline).")
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
            prediction = engine.extract_entities(img_path, llm_provider=args.llm)
            strict_acc, fuzzy_acc, avg_sim = calculate_entity_accuracy(truth, prediction)
            
            progress_data[case_id] = {
                'strict_acc': strict_acc, 
                'fuzzy_acc': fuzzy_acc,
                'avg_sim': avg_sim,
                'truth': truth,
                'prediction': prediction
            }
            
        except Exception as e:
            print(f"    Failed on {case_id}: {e}")
            progress_data[case_id] = {'strict_acc': None, 'fuzzy_acc': None, 'avg_sim': None, 'truth': {}, 'prediction': {}}
            
        # Save progress and report immediately after each case
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f, indent=4)
        generate_markdown_report(progress_data)
            
        if i < len(cases_to_process) - 1:
            if args.llm == 'gemini':
                time.sleep(15)
            
    print(f"\nBatch complete! {len(progress_data)} / {len(all_cases)} total cases finished.")
    print("Report has been safely updated.")

if __name__ == '__main__':
    main()
