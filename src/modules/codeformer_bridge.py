import os
import sys
import cv2
import subprocess
import shutil

class CodeFormerBridge:
    def __init__(self, codeformer_dir, vram_override_limit=4000000):
        self.codeformer_dir = codeformer_dir
        self.vram_override_limit = vram_override_limit
        self.inference_script = os.path.join(codeformer_dir, "inference_codeformer.py")

    def _check_vram_safety(self, image_path):
        """
        Safety guardrail: Check if image exceeds VRAM pixel limits.
        If it's too large, resize it down to prevent CUDA Out-Of-Memory crashes.
        """
        img = cv2.imread(image_path)
        if img is None:
            return image_path
            
        height, width = img.shape[:2]
        total_pixels = height * width
        
        if total_pixels > self.vram_override_limit:
            scale_factor = (self.vram_override_limit / total_pixels) ** 0.5
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            resized = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            safe_path = image_path.replace(".jpg", "_safe.jpg").replace(".png", "_safe.png")
            cv2.imwrite(safe_path, resized)
            return safe_path
            
        return image_path

    def enhance_image(self, input_path):
        """
        Routes the image through the PyTorch CodeFormer GAN.
        Returns the path to the enhanced image.
        """
        if not os.path.exists(self.inference_script):
            print("CodeFormer not found. Returning original image.")
            return input_path
            
        # Ensure VRAM safety
        safe_input_path = self._check_vram_safety(input_path)
        
        # Prepare output directory
        output_dir = os.path.join(os.path.dirname(safe_input_path), "enhanced_output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Build the command for CodeFormer
        # -w 0.7 is the standard fidelity balance for faces
        # --bg_upsampler realesrgan ensures we also enhance non-face text (like license plates!)
        cmd = [
            sys.executable, self.inference_script,
            "-w", "0.7",
            "--bg_upsampler", "realesrgan",
            "-i", os.path.abspath(safe_input_path),
            "-o", os.path.abspath(output_dir)
        ]
        
        print(f"Enhancing image with CodeFormer: {safe_input_path}...")
        try:
            # We run this in a subprocess to isolate the PyTorch VRAM context
            # from the rest of our application.
            subprocess.run(cmd, check=True, cwd=self.codeformer_dir)
            
            # CodeFormer outputs to specific subfolders. 
            # We want the full image from 'final_results', NOT the unrestored 'cropped_faces'.
            final_results_dir = os.path.join(output_dir, "final_results")
            if os.path.exists(final_results_dir):
                for file in os.listdir(final_results_dir):
                    if file.endswith((".png", ".jpg", ".jpeg")):
                        return os.path.join(final_results_dir, file)
                        
        except subprocess.CalledProcessError as e:
            print(f"CodeFormer enhancement failed: {e}")
            
        # Fallback to original if enhancement failed or output not found
        return safe_input_path
