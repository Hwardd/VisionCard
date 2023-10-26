import cv2 as cv
import numpy as np

def image_to_mat(image_path: str):
    """Procesa imagen y la convierte a matriz Mat"""
    mat_image = cv.imread(image_path)
    gray_image = cv.cvtColor(mat_image, cv.COLOR_BGR2GRAY)
    return gray_image

