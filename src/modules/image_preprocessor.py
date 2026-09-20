import cv2

class ImagePreprocessor:
    @staticmethod
    def preprocess_image(image_path):
        """
        Uses OpenCV to preprocess the image and optionally extract bounding boxes.
        For now, we perform basic grayscale and contrast enhancement to help the LLM.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image at {image_path}")
            
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Avoid brittle hardcoded adaptive thresholds which fail on flash photography.
        # Instead, use robust min-max normalization to maximize contrast globally.
        processed = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        
        # Save temporary processed image for the LLM
        temp_path = image_path.replace(".jpg", "_processed.jpg")
        cv2.imwrite(temp_path, processed)
        return temp_path
