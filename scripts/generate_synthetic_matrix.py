import os
import json
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import string
import datetime
import urllib.request

FONTS_DIR = os.path.join(os.path.dirname(__file__), 'fonts')
os.makedirs(FONTS_DIR, exist_ok=True)

# Font URLs
CURSIVE_URL = "https://github.com/google/fonts/raw/main/ofl/dancingscript/DancingScript%5Bwght%5D.ttf"
TECH_URL = "https://github.com/google/fonts/raw/main/ofl/sharetechmono/ShareTechMono-Regular.ttf"
ARIAL_URL = "https://github.com/google/fonts/raw/main/ofl/roboto/Roboto-Regular.ttf"

def download_font(url, filename):
    filepath = os.path.join(FONTS_DIR, filename)
    if not os.path.exists(filepath):
        print(f"Downloading font: {filename}...")
        try:
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print(f"Failed to download font (Internet issue): {e}")
            return None
    return filepath

def random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase + " ", k=length)).strip()

def random_plate():
    return f"{''.join(random.choices(string.ascii_uppercase, k=3))}-{random.randint(1000, 9999)}"

def random_date():
    start_date = datetime.date(2000, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    return (start_date + datetime.timedelta(days=random.randrange((end_date - start_date).days))).isoformat()

def apply_perspective_warp(cv_img):
    h, w = cv_img.shape[:2]
    # Source points (corners)
    pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    # Destination points (randomly warped)
    offset = random.randint(20, 100)
    pts2 = np.float32([
        [0, random.randint(0, offset)], 
        [w, random.randint(0, offset)], 
        [random.randint(0, offset), h], 
        [w - random.randint(0, offset), h - random.randint(0, offset)]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(cv_img, matrix, (w, h), borderValue=(0,0,0) if random.random() > 0.5 else (255,255,255))

def create_advanced_image(text, filename, style="standard"):
    width, height = 1000, 500
    
    # 1. Setup Background & Font based on Style
    if style == "doctor_note":
        bg_color = (245, 245, 220) # Beige paper
        text_color = (0, 0, 139)   # Dark blue ink
        font_path = download_font(CURSIVE_URL, "cursive.ttf")
        font_size = random.randint(40, 60)
    elif style == "night_cctv":
        bg_color = (15, 15, 15)    # Almost black
        text_color = (200, 255, 200) # Greenish night vision text
        font_path = download_font(TECH_URL, "tech.ttf")
        font_size = random.randint(30, 50)
    elif style == "muddy_plate":
        bg_color = (255, 215, 0)   # Yellow license plate
        text_color = (0, 0, 0)     # Black text
        font_path = download_font(ARIAL_URL, "arial.ttf")
        font_size = random.randint(50, 70)
    else:
        bg_color = (255, 255, 255)
        text_color = (0, 0, 0)
        font_path = download_font(ARIAL_URL, "arial.ttf")
        font_size = random.randint(35, 55)

    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    try:
        if font_path is None:
            raise IOError("Font not downloaded")
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # 2. Draw Text (Random Layout)
    if random.random() > 0.5:
        # Standard block
        d.text((50, 50), text, fill=text_color, font=font)
    else:
        # Scattered lines
        lines = text.split('\n')
        y_offset = 20
        for line in lines:
            x_offset = random.randint(10, 200)
            d.text((x_offset, y_offset), line, fill=text_color, font=font)
            y_offset += font_size + random.randint(10, 40)
            
    cv_img = np.array(img)
    
    # 3. Apply Style-Specific Effects
    if style == "muddy_plate":
        # Draw random brown circles to simulate mud
        for _ in range(random.randint(10, 30)):
            cv2.circle(cv_img, (random.randint(0, width), random.randint(0, height)), 
                       random.randint(10, 80), (34, 60, 92), -1) # Brown mud (BGR)
    
    if style == "doctor_note":
        # Add random paper texture lines (ruled paper)
        for y in range(0, height, 40):
            cv2.line(cv_img, (0, y), (width, y), (200, 200, 255), 1)
            
    # 4. Extreme Perspective Warping
    if random.random() > 0.3: # 70% chance of warping
        cv_img = apply_perspective_warp(cv_img)
        
    # 5. Noise & Blur
    noise_level = random.uniform(0.01, 0.3)
    noise = np.random.randn(*cv_img.shape) * 255 * noise_level
    noisy_img = np.clip(cv_img + noise, 0, 255).astype(np.uint8)
    
    blur = random.choice([1, 3, 5, 7, 9])
    if blur > 1:
        final_img = cv2.GaussianBlur(noisy_img, (blur, blur), 0)
    else:
        final_img = noisy_img
        
    cv2.imwrite(filename, cv2.cvtColor(final_img, cv2.COLOR_RGB2BGR))

def main():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'golden', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    styles = ["doctor_note", "night_cctv", "muddy_plate", "standard"]
    
    print("Generating Extreme Evaluation Matrix...")
    for i in range(1, 101): # Overwrite all 100 cases
        case_id = f"case_{i:03d}"
        
        name = random_string(random.randint(5, 15))
        plate = random_plate()
        date = random_date()
        
        text = f"POLICE RECORD\nDATE: {date}\nSUSPECT NAME: {name}\nLICENSE PLATE: {plate}"
        
        json_data = {
            "license_plate": plate,
            "date": date,
            "name": name,
            "raw_text": text
        }
        
        img_path = os.path.join(data_dir, f"{case_id}.jpg")
        json_path = os.path.join(data_dir, f"{case_id}_truth.json")
        
        style = random.choice(styles)
        create_advanced_image(text, img_path, style=style)
        
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=4)
            
    print(f"Successfully generated 100 FAANG-level synthetic test cases in {os.path.abspath(data_dir)}")

if __name__ == '__main__':
    main()
