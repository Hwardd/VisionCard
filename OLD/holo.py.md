import cv2 as cv
import numpy as np
from PIL import ImageGrab
from globalData import *
from time import sleep

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

def recognize_cards_in_image(img_gray, templates, allCards, img_bgr=None, threshold=0.95):
    """
    Recognize cards in an image.

    Args:
    - img_gray (numpy array): Grayscale image.
    - templates (list): List of card image templates.
    - allCards (list of str): Paths to all card images.
    - img_bgr (numpy array): BGR image for drawing. Default is None.
    - threshold (float): Matching threshold.

    Returns:
    - set: Set of recognized card paths.
    """
    recognized = set()

    for template, card_path in zip(templates, allCards):
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
        
        if np.any(res >= threshold):
            recognized.add(card_path)
            print(card_path)

        if img_bgr is not None:  # If an image for drawing is provided
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_bgr, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)

    return recognized

def main():
    templates = load_templates(allCards)
    recognized_cards = set()

    while True:
        print('\n\n')
        sleep(0.5)  # Pausa de 500 ms
        img_gray, img_bgr = capture_screen()

        newly_recognized = recognize_cards_in_image(img_gray, templates, allCards, img_bgr=img_bgr)
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

if __name__ == "__main__":
    main()
