import os
try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Installing huggingface_hub...")
    os.system("pip install huggingface_hub")
    from huggingface_hub import hf_hub_download

def download_model():
    print("Initializing Enterprise Hugging Face Downloader...")
    repo_id = "GorangSinghal/PoliceForensics_Llama3_8B"
    filename = "llama-3-8b-instruct.Q4_K_M.gguf"
    
    # Get the absolute path to the weights directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    weights_dir = os.path.join(base_dir, "weights")
    os.makedirs(weights_dir, exist_ok=True)
    
    print(f"Downloading {filename} directly to: \n{weights_dir}")
    print("This connection is highly stable and will automatically resume if interrupted. Please wait...\n")
    
    # Download the file
    downloaded_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir=weights_dir,
        local_dir_use_symlinks=False # Download actual file, not a symlink
    )
    
    print(f"\n[SUCCESS] Model saved permanently at: {downloaded_path}")

if __name__ == "__main__":
    download_model()
