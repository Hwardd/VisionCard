from PIL import Image
import cv2 as cv
import numpy as np
import pytesseract
from config.constants import ALL_CARD_TEMPLATES, AC_TEMPLATE, AS_TEMPLATE

def recognize_cards(roi):
    """Dado una zona roi detecta todas las cartas que se encuentran en el roi."""
    detected_cards = initial_card_detection(roi)
    detected_cards = reevaluate_ace_detection(roi, detected_cards)
    return detected_cards


def initial_card_detection(roi):
    """Realiza la detección inicial de cartas con el umbral predeterminado."""
    detected_cards = []
    for template, template_id in ALL_CARD_TEMPLATES:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(roi, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.94
        loc = np.where(res >= threshold) 

        for pt in zip(*loc[::-1]):
            if template_id not in detected_cards:
                detected_cards.append(template_id)
    
    return detected_cards


def reevaluate_ace_detection(roi, detected_cards):
    """Reevalúa la detección de As y Ac con un umbral más alto."""
    if "Ac" in detected_cards or "As" in detected_cards:
        for specific_template, specific_id in [(AC_TEMPLATE, "Ac"), (AS_TEMPLATE, "As")]:
            res = cv.matchTemplate(roi, specific_template, cv.TM_CCOEFF_NORMED)
            threshold_specific = 0.96
            if np.max(res) >= threshold_specific:
                if specific_id == "Ac" and "As" in detected_cards:
                    detected_cards.remove("As")
                elif specific_id == "As" and "Ac" in detected_cards:
                    detected_cards.remove("Ac")
                # Solo añadir el as correcto si no está ya en la lista
                if specific_id not in detected_cards:
                    detected_cards.append(specific_id)
    
    return detected_cards

def recognize_text(roi):
    """Dado una zona roi se usa OCR para extraer el texto (acota el roi para que contenga unicamente texto)"""
    # Convertir la matriz numpy a una imagen PIL para usar con pytesseract
    roi_image = Image.fromarray(roi)

    # Usar pytesseract para extraer texto
    text = pytesseract.image_to_string(roi_image, config='--psm 6')
    return text.strip().replace('Pot: ', '')





