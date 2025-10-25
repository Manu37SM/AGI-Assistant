import pytesseract, os, cv2
from PIL import Image
import yaml

cfg = yaml.safe_load(open('config.yaml','r'))
TESS_CMD = cfg.get('TESSERACT_CMD', 'tesseract')
pytesseract.pytesseract.tesseract_cmd = TESS_CMD

def extract_ocr_from_image(path):
    try:
        img = cv2.imread(path)
        if img is None:
            return ''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # optional thresholding could be applied
        text = pytesseract.image_to_string(gray)
        return text.strip()
    except Exception as e:
        print('[ocr] error', e)
        return ''
