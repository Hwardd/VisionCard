import cv2 as cv
import numpy as np

def image_to_mat(image_path: str):
    """Procesa imagen y la convierte a matriz Mat"""
    mat_image = cv.imread(image_path)
    gray_image = cv.cvtColor(mat_image, cv.COLOR_BGR2GRAY)
    return gray_image

def roi_tester(roi: np.ndarray ):
    """Muestra la imagen capturada de la region de interes (roi) dada"""
    cv.imshow('roi_tester', roi)
    cv.waitKey(0)
    cv.destroyAllWindows()