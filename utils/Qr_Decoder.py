from qreader import QReader
from PIL import Image
import numpy as np
from urllib.parse import urlparse
from utils.Validators import is_valid_ip, is_valid_domain

def extract_from_qr(image_path: str) -> str | None:
    try:
        pil_image = Image.open(image_path).convert("RGB")
        image_np = np.array(pil_image)

        qreader = QReader()
        results = qreader.detect_and_decode(image_np)

        if not results:
            print("[QReader] No QR code found.")

        for result in results:
            result = result.strip()
            print(f"[QReader] Decoded: {result}")

            # Try to extract hostname if it's a URL
            parsed = urlparse(result)
            hostname = parsed.hostname
            if hostname and (is_valid_ip(hostname) or is_valid_domain(hostname)):
                return hostname

            # Otherwise, check raw string
            if is_valid_ip(result) or is_valid_domain(result):
                return result

    except Exception as e:
        print(f"[QReader] Error: {e}")
    return None