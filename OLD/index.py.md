import cv2 as cv
from PIL import ImageGrab
from globalData import *
import os
import numpy as np
import pytesseract
from PIL import Image

TEMPLATE_DIR = "./images/handCards"

def load_card_templates(path: str) -> list:
    """Carga las plantillas de cartas y sus identificadores."""
    templates = []
    for template_name in os.listdir(path):
        template_image = cv.imread(os.path.join(path, template_name), 0)  # 0 para cargar en escala de grises
        template_id = os.path.splitext(template_name)[0]  # Eliminar la extensión .png
        templates.append((template_image, template_id))
    return templates

ALL_CARD_TEMPLATES = load_card_templates(TEMPLATE_DIR)


def preprocess_image(image_path):
    """Preprocesamiento de la imagen."""
    mat_image = cv.imread(image_path)
    gray_image = cv.cvtColor(mat_image, cv.COLOR_BGR2GRAY)
    return gray_image

def extract_my_hand_roi(gray_image):
    """Extraer zonas de interés de mi mano."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.62):int(height * 0.72), int(width * 0.428):int(width * 0.56)]


def extract_table_cards_roi(gray_image):
    """Extraer zonas de interés de las cartas en la mesa."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.35):int(height * 0.48), int(width * 0.32):int(width * 0.67)]


def extract_pot_amount_roi(gray_image):
    """Extraer zonas de interés del monto del bote."""
    height, width = gray_image.shape
    
    # Estas proporciones se basan en la observación de la imagen proporcionada.
    # Es posible que debas ajustar estas proporciones si cambia la resolución o si la interfaz de usuario es diferente.
    
    y_start = int(height * 0.30)  # Comenzamos en el 35% del alto total de la imagen.
    y_end = int(height * 0.35)    # Terminamos en el 45% del alto total de la imagen.
    
    x_start = int(width * 0.42)    # Comenzamos en el 40% del ancho total de la imagen.
    x_end = int(width * 0.58)      # Terminamos en el 60% del ancho total de la imagen.
    
    return gray_image[y_start:y_end, x_start:x_end]

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

def extract_text_from_roi(roi):
    """Extracción de texto."""
    # Convertir la matriz numpy a una imagen PIL para usar con pytesseract
    roi_image = Image.fromarray(roi)

    # Usar pytesseract para extraer texto
    text = pytesseract.image_to_string(roi_image, config='--psm 6')
    return text.strip().replace('Pot: ', '')

def main():
    # Supongo que quieres analizar una captura de pantalla, 
    # por lo que uso ImageGrab para obtenerla.
    screenshot = ImageGrab.grab(bbox=(0,0,970,692))
    screenshot.save("screenshot.png")
    gray_image = preprocess_image("screenshot.png")

    my_hand_roi = extract_my_hand_roi(gray_image)
    table_cards_roi = extract_table_cards_roi(gray_image)
    pot_amount_roi = extract_pot_amount_roi(gray_image)

    my_hand = recognize_cards(my_hand_roi, ALL_CARD_TEMPLATES)
    table_cards = recognize_cards(table_cards_roi, ALL_CARD_TEMPLATES)
    pot_amount = extract_text_from_roi(pot_amount_roi)

    print({
        "myHand": my_hand,
        "tableCards": table_cards,
        "potAmount": pot_amount
    })

    # cv.imshow('My Hand ROI', my_hand_roi)
    # cv.imshow('Table Cards ROI', table_cards_roi)
    # cv.imshow('Pot Amount ROI', pot_amount_roi)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

if __name__ == "__main__":
    main()
