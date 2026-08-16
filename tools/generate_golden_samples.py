import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_noisy_image(text, filename, blur=3, noise_level=0.1, font_name="arial.ttf"):
    # Create a blank white image
    img = Image.new('RGB', (600, 200), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype(font_name, 30)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except IOError:
            font = ImageFont.load_default()
        
    d.text((20, 20), text, fill='black', font=font)
    
    # Convert to OpenCV format (numpy array)
    cv_img = np.array(img)
    
    # Add noise
    noise = np.random.randn(*cv_img.shape) * 255 * noise_level
    noisy_img = np.clip(cv_img + noise, 0, 255).astype(np.uint8)
    
    # Add blur
    blurred_img = cv2.GaussianBlur(noisy_img, (blur, blur), 0)
    
    # Save the image
    cv2.imwrite(filename, cv2.cvtColor(blurred_img, cv2.COLOR_RGB2BGR))

def main():
    data_dir = '../golden/data'
    os.makedirs(data_dir, exist_ok=True)
    
    samples = [
        {
            "id": "case_001",
            "text": "SUSPECT VEHICLE REPORT\nDATE: 2023-10-27\nNAME: JOHN DOE\nPLATE: ABC-1234",
            "json": {
                "license_plate": "ABC-1234",
                "date": "2023-10-27",
                "name": "JOHN DOE",
                "raw_text": "SUSPECT VEHICLE REPORT\nDATE: 2023-10-27\nNAME: JOHN DOE\nPLATE: ABC-1234"
            },
            "blur": 3,
            "noise": 0.1
        },
        {
            "id": "case_002",
            "text": "INCIDENT LOG\nDATE: 2023-11-05\nNAME: JANE SMITH\nPLATE: XYZ-9876",
            "json": {
                "license_plate": "XYZ-9876",
                "date": "2023-11-05",
                "name": "JANE SMITH",
                "raw_text": "INCIDENT LOG\nDATE: 2023-11-05\nNAME: JANE SMITH\nPLATE: XYZ-9876"
            },
            "blur": 5,
            "noise": 0.2
        },
        {
            "id": "case_003",
            "text": "TRAFFIC STOP\nDATE: 2023-12-12\nNAME: MICHAEL JOHNSON\nPLATE: DEF-5678",
            "json": {
                "license_plate": "DEF-5678",
                "date": "2023-12-12",
                "name": "MICHAEL JOHNSON",
                "raw_text": "TRAFFIC STOP\nDATE: 2023-12-12\nNAME: MICHAEL JOHNSON\nPLATE: DEF-5678"
            },
            "blur": 7,
            "noise": 0.3
        },
        {
            "id": "case_004",
            "text": "HIT AND RUN\nDATE: 2024-01-01\nNAME: ALICE WONDER\nPLATE: GHI-9012",
            "json": {
                "license_plate": "GHI-9012",
                "date": "2024-01-01",
                "name": "ALICE WONDER",
                "raw_text": "HIT AND RUN\nDATE: 2024-01-01\nNAME: ALICE WONDER\nPLATE: GHI-9012"
            },
            "blur": 15,
            "noise": 0.6
        },
        {
            "id": "case_005",
            "text": "SUSPECT MEDICAL FILE\nDATE: 2024-02-15\nNAME: DR K SMITH\nPLATE: MED-1111",
            "json": {
                "license_plate": "MED-1111",
                "date": "2024-02-15",
                "name": "DR K SMITH",
                "raw_text": "SUSPECT MEDICAL FILE\nDATE: 2024-02-15\nNAME: DR K SMITH\nPLATE: MED-1111"
            },
            "blur": 5,
            "noise": 0.2,
            "font": "pristina.ttf" # Messy cursive font on Windows
        }
    ]
    
    for sample in samples:
        img_path = os.path.join(data_dir, f"{sample['id']}.jpg")
        json_path = os.path.join(data_dir, f"{sample['id']}_truth.json")
        
        # Ensure blur is odd
        blur = sample['blur'] if sample['blur'] % 2 != 0 else sample['blur'] + 1
        font_name = sample.get('font', 'arial.ttf')
        
        create_noisy_image(sample['text'], img_path, blur, sample['noise'], font_name)
        
        with open(json_path, 'w') as f:
            json.dump(sample['json'], f, indent=4)
            
        print(f"Generated {img_path} and {json_path}")

if __name__ == '__main__':
    main()
