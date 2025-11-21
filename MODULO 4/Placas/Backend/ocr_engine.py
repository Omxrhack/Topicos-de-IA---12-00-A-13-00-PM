import easyocr
import cv2
from plate_detector import detect_plate_region

reader = easyocr.Reader(['en'])

def extract_plate_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, 0.0

    plate_region = detect_plate_region(image)
    results = reader.readtext(plate_region)

    if not results:
        return None, 0.0

    best_text = None
    best_conf = 0.0

    for (_, text, conf) in results:
        if conf > best_conf:
            best_conf = conf
            best_text = text

    if best_text:
        best_text = best_text.replace(" ", "").upper()

    return best_text, float(best_conf)
