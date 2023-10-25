import cv2 as cv
import os
from PIL import ImageGrab


def load_card_templates(path: str) -> list:
    """Carga las plantillas de cartas y sus identificadores."""
    templates = []
    for template_name in os.listdir(path):
        template_image = cv.imread(os.path.join(path, template_name), 0)  # 0 para cargar en escala de grises
        template_id = os.path.splitext(template_name)[0]  # Eliminar la extensión .png
        templates.append((template_image, template_id))
    return templates

def take_table_screenshot(TABLE_SCREENSHOT_PATH):
    screenshot = ImageGrab.grab(bbox=(0,0,970,692))
    screenshot.save(TABLE_SCREENSHOT_PATH)