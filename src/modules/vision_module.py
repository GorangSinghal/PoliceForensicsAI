class VisionModule:
    @staticmethod
    def run_easyocr(img_path):
        import easyocr
        print("\n[EASYOCR] Reading pixels...")
        # We initialize EasyOCR in English mode
        reader = easyocr.Reader(['en'], verbose=False)
        # Detail=0 returns just a list of text strings
        results = reader.readtext(img_path, detail=0)
        return "\n".join(results)
