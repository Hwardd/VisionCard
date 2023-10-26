from PIL import Image
import cv2 as cv
import numpy as np
import pytesseract
from config.constants import BET_DOLLAR_SIGN_TEMPLATE

def recognize_cards(roi, templates):
    """Reconocimiento de cartas."""
    detected_cards = []
    for template, template_id in templates:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(roi, template, cv.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            # Evita la duplicación y agrega el identificador de la carta
            if template_id not in detected_cards:
                detected_cards.append(template_id)
    return detected_cards

def recognize_text_from_mat(roi):
    """Extracción de texto."""
    # Convertir la matriz numpy a una imagen PIL para usar con pytesseract
    roi_image = Image.fromarray(roi)

    # Usar pytesseract para extraer texto
    text = pytesseract.image_to_string(roi_image, config='--psm 6')
    return text.strip().replace('Pot: ', '')

def detect_dealer_position(gray_image, dealer_template):
    positions = {
        'D': (.58, .68, .35, .45), # me
        'D+1': (.40, .50, .15, .20), # one
        'D+2': (.30, .40, .19, .27), # two
        'D+3': (.22, .32, .50, .60), # three
        'D+4': (.30, .40, .72, .82), # four
        'D-1': (.52, .62, .68, .78) # five
    }

    h, w = gray_image.shape
    w_t, h_t = dealer_template.shape[::-1]

    max_correlation = 0
    dealer_position = None

    for position, (top, bottom, left, right) in positions.items():
        roi = gray_image[int(top*h):int(bottom*h), int(left*w):int(right*w)]
        
        if roi.shape[0] < h_t or roi.shape[1] < w_t:
            continue  # Skip this ROI if it's smaller than the template

        result = cv.matchTemplate(roi, dealer_template, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(result)

        if max_val > max_correlation:
            max_correlation = max_val
            dealer_position = position

    return dealer_position


def get_bet_zone_roi(original_image):

    # Usar template matching para encontrar el signo $
    res = cv.matchTemplate(original_image, BET_DOLLAR_SIGN_TEMPLATE, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(res)

    # Introducir un umbral de coincidencia
    THRESHOLD = 0.8
    if max_val < THRESHOLD:
        return None

    top_left = max_loc
    bottom_right = (top_left[0] + BET_DOLLAR_SIGN_TEMPLATE.shape[1], top_left[1] + BET_DOLLAR_SIGN_TEMPLATE.shape[0])


    # Corrección en la asignación de x y y
    x, y = max_loc

    # Definir la ROI a la derecha del signo $
    roi_width = 30
    roi_height = BET_DOLLAR_SIGN_TEMPLATE.shape[0]

    # Ajustar el ancho de la ROI si se sale de la imagen
    if x + BET_DOLLAR_SIGN_TEMPLATE.shape[1] + roi_width > original_image.shape[1]:
        roi_width = original_image.shape[1] - (x + BET_DOLLAR_SIGN_TEMPLATE.shape[1])

    # Verificar si la ROI tiene un tamaño válido
    if roi_width <= 0 or roi_height <= 0:
        return None

    roi = original_image[y:y+roi_height, x+BET_DOLLAR_SIGN_TEMPLATE.shape[1]:x+BET_DOLLAR_SIGN_TEMPLATE.shape[1]+roi_width]

    return roi


def extract_bets_from_positions(gray_image):
    positions = {
        'V1': (.49, .59, .23, .42),
        'V2': (.315, .355, .25, .45),
        'V3': (.22, .32, .47, .67),
        'V4': (.28, .33, .55, .73),
        'V-1': (.52, .57, .62, .81)
    }
    bets = {}

    
    for villano, (top, bottom, left, right) in positions.items():
        h, w = gray_image.shape
        roi = gray_image[int(top*h):int(bottom*h), int(left*w):int(right*w)]
        
        bet_zone=get_bet_zone_roi(roi)
        if bet_zone is None:
            bet_value = None
        else:
            # cv.imshow('Match', bet_zone)
            # cv.waitKey(0)
            bet_value = recognize_text_from_mat(bet_zone)
        
        if bet_value:
            # Convertir a formato numérico si es necesario (ejemplo: "$0.02" -> 0.02)
            try:
                bet_value = float(bet_value.replace('$', ''))
            except ValueError:
                pass
            
            bets[villano] = bet_value
    
    return bets