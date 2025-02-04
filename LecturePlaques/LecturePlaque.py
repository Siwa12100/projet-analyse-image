import cv2
import pytesseract

def extract_text_from_image(image: "cv2.Mat", lang: str = 'fra') -> str:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    extracted_text = pytesseract.image_to_string(thresh, lang=lang)
    
    return extracted_text.strip()
