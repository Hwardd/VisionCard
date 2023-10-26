from PIL import Image
import cv2 as cv
import numpy as np
import pytesseract
from config.constants import ALL_CARD_TEMPLATES

def recognize_cards(roi):
    """Dado una zona roi detecta todas las cartas que se encuentran en el roi"""
    detected_cards = []
    for template, template_id in ALL_CARD_TEMPLATES:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(roi, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            # Evita la duplicación y agrega el identificador de la carta
            if template_id not in detected_cards:
                detected_cards.append(template_id)
    return detected_cards

def recognize_text(roi):
    """Dado una zona roi se usa OCR para extraer el texto (acota el roi para que contenga unicamente texto)"""
    # Convertir la matriz numpy a una imagen PIL para usar con pytesseract
    roi_image = Image.fromarray(roi)

    # Usar pytesseract para extraer texto
    text = pytesseract.image_to_string(roi_image, config='--psm 6')
    return text.strip().replace('Pot: ', '')





