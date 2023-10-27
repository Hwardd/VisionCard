import cv2 as cv
import numpy as np
from PIL import ImageGrab
from time import sleep
from config.constants import ALL_CARD_TEMPLATES, AC_TEMPLATE, AS_TEMPLATE

def load_templates(cards):
    """
    Load image templates from given paths.
    
    Args:
    - cards (list of str): Paths to card images.

    Returns:
    - list: List of loaded image templates.
    """
    return [cv.imread(card, 0) for card in cards]

def capture_screen(bbox=(0,0,970,692)):
    """
    Capture screen region and return its grayscale and BGR versions.

    Args:
    - bbox (tuple): Screen region to capture.

    Returns:
    - tuple: Grayscale and BGR versions of captured region.
    """
    img = ImageGrab.grab(bbox=bbox)
    img_np = np.array(img)
    img_gray = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
    img_bgr = cv.cvtColor(img_np, cv.COLOR_BGR2RGB)
    return img_gray, img_bgr

def recognize_cards(roi, img_bgr):
    """Dado una zona roi detecta todas las cartas que se encuentran en el roi."""
    detected_cards = initial_card_detection(roi, img_bgr)
    detected_cards = reevaluate_ace_detection(roi, detected_cards)
    print(detected_cards)
    return detected_cards


def initial_card_detection(roi, img_bgr):
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
                cv.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
    
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

def cards_detector():
    recognized_cards = set()

    while True:
        print('\n\n')
        sleep(0.5)  # Pausa de 500 ms
        img_gray, img_bgr = capture_screen()

        newly_recognized = recognize_cards(img_gray, img_bgr=img_bgr)
        recognized_cards.update(newly_recognized)

        cv.imshow("Scanned Screen", img_bgr)

        # Save recognized cards to a file
        with open("recognized_cards.txt", "w") as file:
            for card in recognized_cards:
                file.write(card + "\n")

        # Break the loop if 'q' is pressed
        if cv.waitKey(100) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()

