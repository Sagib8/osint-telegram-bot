import pytesseract
from PIL import Image, ImageFilter, ImageOps
from utils.Validators import is_valid_ip, is_valid_domain
import re


def clean_word(word: str) -> str:
    # Keep only letters, digits, dots, dashes
    return re.sub(r"[^\w\.-]", "", word)


def extract_ip_or_domain_from_image(image_path: str) -> list[str]:
    matches = []
    try:
        print(f"[OCR] Opening image: {image_path}")
        image = Image.open(image_path).convert("L")  # Convert to grayscale

        # Enhance contrast and sharpness
        image = ImageOps.autocontrast(image)
        image = image.filter(ImageFilter.SHARPEN)

        print("[OCR] Running Tesseract OCR...")
        text = pytesseract.image_to_string(image, config="--psm 6")
        print(f"[OCR] Extracted text:\n{text}")

        # Go through each word and try to clean and validate
        for word in text.split():
            cleaned = clean_word(word.strip().lower())
            if is_valid_ip(cleaned) or is_valid_domain(cleaned):
                if cleaned not in matches:
                    print(f"[OCR] Found valid match: {cleaned}")
                    matches.append(cleaned)

    except Exception as e:
        print(f"[OCR] Error: {e}")

    return matches