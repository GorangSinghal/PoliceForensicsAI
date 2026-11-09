import os

class VisionModule:
    @staticmethod
    def run_easyocr(img_path):
        import easyocr
        print("\n[EASYOCR] Reading pixels...")
        # Store weights in workspace weights directory
        weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "weights", "easyocr"))
        os.makedirs(weights_dir, exist_ok=True)
        # We initialize EasyOCR in English mode
        reader = easyocr.Reader(['en'], verbose=False, model_storage_directory=weights_dir)
        # Detail=0 returns just a list of text strings
        results = reader.readtext(img_path, detail=0)
        return "\n".join(results)

