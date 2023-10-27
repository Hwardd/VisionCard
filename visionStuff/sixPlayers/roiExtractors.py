import cv2 as cv
import numpy as np

def get_chips_sixP(gray_image: np.ndarray):
    """Extraer zonas de interés de mi juego (par, color, o lo que tenga formado)."""
    yo=(.73, .78, .465, .575)
    V1=(.558, .605, .035, .155)
    V2=(.265, .31, .075, .183)
    V3=(.17, .215, .41, .525)
    V4=(.26, .31, .805, .925)
    V5=(.555, .605, .838, .95)
    
    height, width = gray_image.shape

    roi_positions = {
        'yo': gray_image[int(height * yo[0] ):int(height * yo[1]), int(width * yo[2]):int(width * yo[3])],
        'V1': gray_image[int(height * V1[0] ):int(height * V1[1]), int(width * V1[2]):int(width * V1[3])],
        'V2': gray_image[int(height * V2[0] ):int(height * V2[1]), int(width * V2[2]):int(width * V2[3])],
        'V3': gray_image[int(height * V3[0] ):int(height * V3[1]), int(width * V3[2]):int(width * V3[3])],
        'V4': gray_image[int(height * V4[0] ):int(height * V4[1]), int(width * V4[2]):int(width * V4[3])],
        'V-1': gray_image[int(height * V5[0] ):int(height * V5[1]), int(width * V5[2]):int(width * V5[3])],
    }
    

    # cv.imshow('roi_tester_4', roi_positions['V-1'])
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return roi_positions
