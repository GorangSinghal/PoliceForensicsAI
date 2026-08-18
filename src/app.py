import gradio as gr
import json
import os
import pandas as pd
from ocr_engine import OCREngine
import dotenv

# Initialize the global engine
engine = OCREngine()

# Startup Discovery Logic
weights_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "weights")
os.makedirs(weights_dir, exist_ok=True)
pro_mode = False
for f in os.listdir(weights_dir):
    if f.endswith(".gguf") and os.path.getsize(os.path.join(weights_dir, f)) > 3 * 1024 * 1024 * 1024:
        pro_mode = True
        break

MODE_BADGE = "⚡ PRO MODE (Llama 8B Active)" if pro_mode else "🪶 LITE MODE (TinyLlama 1B Active)"

# Ensure exports directory exists
EXPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "exports")
os.makedirs(EXPORTS_DIR, exist_ok=True)

def process_evidence(image_path, use_codeformer, llm_provider, api_key_input):
    if not image_path:
        return {"error": "No image uploaded."}, None, None, None, None
        
    try:
        # Persistent Environment Caching: Hot-swap the API key if it's new
        if api_key_input and api_key_input != os.getenv("GEMINI_API_KEY"):
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
            dotenv.set_key(env_path, "GEMINI_API_KEY", api_key_input)
            os.environ["GEMINI_API_KEY"] = api_key_input
            engine.update_api_key(api_key_input)
            
        # Run the engine
        json_data, processed_img_path = engine.extract_entities(
            image_path, 
            use_codeformer=use_codeformer, 
            return_image_path=True,
            llm_provider=llm_provider
        )
        
        # Create Export Files
        # 1. JSON
        json_path = os.path.join(EXPORTS_DIR, "forensics_report.json")
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=4)
            
        # 2. CSV / Excel
        csv_path = os.path.join(EXPORTS_DIR, "forensics_report.csv")
        excel_path = os.path.join(EXPORTS_DIR, "forensics_report.xlsx")
        
        # Convert the json dictionary to a flat dataframe
        df = pd.DataFrame([json_data])
        df.to_csv(csv_path, index=False)
        
        # NOTE: to_excel requires openpyxl, if not installed we will fallback to CSV for the button.
        try:
            df.to_excel(excel_path, index=False)
        except Exception:
            # If openpyxl is not installed, fallback the excel path to csv
            excel_path = csv_path
        
        return json_data, processed_img_path, json_path, csv_path, excel_path
        
    except Exception as e:
        return {"error": str(e)}, None, None, None, None

# ==========================================
# FUTURISTIC CYBER THEME (CSS + Gradio Theme)
# ==========================================
cyber_theme = gr.themes.Default(
    primary_hue="cyan",
    secondary_hue="emerald",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Rajdhani"), "sans-serif"]
)

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');

body {
    background-color: #0d1117 !important;
}
.gradio-container {
    border: 1px solid #00f2fe;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
    border-radius: 10px;
    padding: 20px;
}
h1 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00f2fe !important;
    text-shadow: 0 0 10px rgba(0, 242, 254, 0.5);
    text-transform: uppercase;
    letter-spacing: 2px;
}
.primary {
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
    border: none !important;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.6) !important;
    color: white !important;
    font-weight: bold;
    text-transform: uppercase;
}
.primary:hover {
    box-shadow: 0 0 25px rgba(0, 242, 254, 0.9) !important;
}
#api_key_box textarea:disabled, #api_key_box input:disabled {
    cursor: not-allowed !important;
}
"""

with gr.Blocks(title="PoliceForensicsAI Cyber Terminal") as app:
    gr.Markdown("# 🚓 FORENSICS AI : CYBER COMMAND TERMINAL")
    gr.Markdown("*Secure Evidence Extraction System. Powered by Google Gemini & PyTorch.*")
            
    with gr.Accordion("🛡️ Anti-Hallucination Guardrails Active | 📊 Continuously Evaluated WER | 🔒 Offline Air-Gapped Ready (Click for Proof)", open=False):
        gr.Markdown('''
        **🛡️ Anti-Hallucination Guardrails:** Utilizes strict SpaCy Named Entity Recognition (NER) and deterministic Regex validation pipelines. If the LLM attempts to hallucinate non-standard formats, the guardrail intercepts and sanitizes the payload before database entry.
        
        **📊 Continuously Evaluated WER:** System is rigorously benchmarked against the `100-Case Synthetic Golden Matrix`. Tests evaluate Word Error Rate (WER) against heavy Gaussian blur, out-of-distribution (OOD) rotations, and severe signal noise to guarantee evolving reliability across milestones.
        
        **🔒 Offline Air-Gapped Ready:** The architecture supports a Strategy Pattern allowing dynamic switching from Cloud APIs (`gemini-1.5-flash`) to a local 11B parameter edge-compute model (`llama3.2-vision`) for zero-trust, classified intranet environments.
        ''')
    
    with gr.Row():
        # Left Column: Inputs & Controls
        with gr.Column(scale=1):
            input_image = gr.Image(type="filepath", label="Upload Evidence (Image / Dashcam)", height=350, elem_id="black-drop-box")
            use_dl_toggle = gr.Checkbox(
                label="Enable Deep Learning Restoration (CodeFormer GAN)",
                info="⚠️ COMPLIANCE WARNING: Invokes CodeFormer GAN. Governed by strict S-Lab Non-Commercial/Research License. By checking this box, the agency assumes all legal compliance liability.",
                value=False
            )
            llm_provider = gr.Radio(
                choices=[("☁️ Gemini Cloud API", "gemini"), ("Offline Edge Mode (EasyOCR + Llama 3)", "offline")],
                label="Extraction Engine",
                info="Choose between cloud-scale accuracy or air-gapped security.",
                value="gemini"
            )
            with gr.Accordion("⚙️ API Key Settings", open=False, elem_id="api_key_accordion") as api_key_accordion:
                gr.Markdown("**🔑 Gemini API Key**<br><small>Your key is securely cached locally. Update it here at any time.</small>")
                with gr.Group():
                    with gr.Row(equal_height=True):
                        api_key_input = gr.Textbox(
                            show_label=False, 
                            type="password", 
                            value=os.getenv("GEMINI_API_KEY", ""),
                            interactive=False,
                            scale=10,
                            elem_id="api_key_box",
                            container=False
                        )
                        edit_key_btn = gr.Button("🔄 Edit", size="sm", scale=0, min_width=80)
            
            hardware_badge = gr.Markdown(f"### Current Hardware Configuration:\n<div style='padding: 10px; border: 1px solid #00f2fe; border-radius: 5px; background-color: #0d1117; color: #00f2fe; font-weight: bold; text-align: center; font-size: 1.2em;'>{MODE_BADGE}</div>\n<small>*Drop a 5GB Llama .gguf file into the `weights/` folder to automatically unlock PRO mode.*</small>", visible=False)
            
            submit_btn = gr.Button("⚡ INITIATE FORENSICS EXTRACTION", variant="primary")
            
        # Right Column: Outputs & Verification
        with gr.Column(scale=1):
            output_json = gr.JSON(label="Structured Evidence Data")
            output_image = gr.Image(type="filepath", label="AI Restored Verification Image", height=350, elem_id="black-drop-box-2")
            
            gr.Markdown("### 📥 Export Reports")
            with gr.Row():
                dl_json = gr.DownloadButton("Download JSON", variant="secondary")
                dl_csv = gr.DownloadButton("Download CSV", variant="secondary")
                dl_excel = gr.DownloadButton("Download Excel", variant="secondary")
            
    # Add Warning Pop-Up for CodeFormer License
    def dl_warning_popup(is_checked):
        if is_checked:
            gr.Warning("⚠️ COMPLIANCE WARNING: You are invoking the CodeFormer GAN (S-Lab Non-Commercial License). Ensure you have legal clearance.")
            
    use_dl_toggle.change(
        fn=dl_warning_popup,
        inputs=[use_dl_toggle],
        outputs=None
    )
    
    # Dynamic Visibility for API Key and Hardware Badge
    def toggle_backend(llm_choice):
        show_api = (llm_choice == "gemini")
        show_hw = (llm_choice == "offline")
        return gr.update(visible=show_api), gr.update(visible=show_hw)
        
    llm_provider.change(
        fn=toggle_backend,
        inputs=[llm_provider],
        outputs=[api_key_accordion, hardware_badge]
    )
    
    # Unlock API Key for editing
    def unlock_key():
        return gr.update(interactive=True, value="")
        
    edit_key_btn.click(
        fn=unlock_key,
        inputs=None,
        outputs=[api_key_input]
    )
            
    # Bind the button to the function
    # Note: image download button is not needed separately since gr.Image already has a built-in download button in the top right corner!
    submit_btn.click(
        fn=process_evidence,
        inputs=[input_image, use_dl_toggle, llm_provider, api_key_input],
        outputs=[output_json, output_image, dl_json, dl_csv, dl_excel]
    )

def main():
    print("Booting Cyber Terminal...")
    asset_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    app.launch(server_name="0.0.0.0", server_port=7860, allowed_paths=[asset_dir], theme=cyber_theme, css=custom_css)

if __name__ == "__main__":
    main()
