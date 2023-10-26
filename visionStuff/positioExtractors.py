import numpy as np
from visionStuff.otherOperations import roi_tester

def roi_detector_tester(gray_image: np.ndarray, coordinates=(.10,.20,.30,.40)):
    """Extraer zonas de interés de mi juego (par, color, o lo que tenga formado)."""
    height, width = gray_image.shape
    subImage= gray_image[int(height *coordinates[0]):int(height *coordinates[1]), int(width * coordinates[2]):int(width *coordinates[3])]
    roi_tester(subImage)

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
