import cv2 as cv
import numpy

def simple_roi_tester(roi: numpy.ndarray ):
    """Muestra la imagen capturada de la region de interes (roi) dada"""
    cv.imshow('roi_tester', roi)
    cv.waitKey(0)
    cv.destroyAllWindows()

def roi_coordinates_tester(gray_image: numpy.ndarray, coordinates=(.10,.20,.30,.40)):
    """Dado una gray image, muestra en ventana el segmento roi denotado por las coordenadas en decimales (porciento) en el segundo parámetro"""
    height, width = gray_image.shape
    subImage= gray_image[int(height *coordinates[0]):int(height *coordinates[1]), int(width * coordinates[2]):int(width *coordinates[3])]
    simple_roi_tester(subImage)