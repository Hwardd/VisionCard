import numpy as np
import cv2 as cv
from config.constants import BET_DOLLAR_SIGN_TEMPLATE

def get_my_hand_roi(gray_image: np.ndarray):
    """Extraer zonas de interés de mi mano."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.62):int(height * 0.72), int(width * 0.428):int(width * 0.56)]

def get_table_cards_roi(gray_image: np.ndarray):
    """Extraer zonas de interés de las cartas en la mesa."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.35):int(height * 0.48), int(width * 0.32):int(width * 0.67)]

def get_pot_amount_roi(gray_image: np.ndarray):
    """Extraer zonas de interés del monto del bote."""
    height, width = gray_image.shape
    
    # Estas proporciones se basan en la observación de la imagen proporcionada.
    # Es posible que debas ajustar estas proporciones si cambia la resolución o si la interfaz de usuario es diferente.
    
    y_start = int(height * 0.30)
    y_end = int(height * 0.35)  
    
    x_start = int(width * 0.42)  
    x_end = int(width * 0.58)    
    
    return gray_image[y_start:y_end, x_start:x_end]

def get_my_chips_roi(gray_image: np.ndarray):
    """Extraer zonas de interés de mis fichas."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.735):int(height * 0.78), int(width * 0.47):int(width * 0.57)]

def get_my_game_roi(gray_image: np.ndarray):
    """Extraer zonas de interés de mi juego (par, color, o lo que tenga formado)."""
    height, width = gray_image.shape
    return gray_image[int(height * 0.728):int(height * 0.77), int(width * 0.75):int(width * 0.98)]

def get_bet_zone_roi(original_image):
    """Recibe una grey image roi con la zona donde apuesta un jugador, busca el signo de $ y retorna un roi con únicamente la zona del dinero apostado"""
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

