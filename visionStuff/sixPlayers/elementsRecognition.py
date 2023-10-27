import cv2 as cv
from visionStuff.allPlayers.elementsRecognition import recognize_text
from visionStuff.allPlayers.roiExtractors import get_bet_zone_roi
from config.constants import DEALER_TEMPLATE

def recognize_bets_sixP(gray_image):
    """Six Player Table: A partir de la gray image de la mesa, detecta las zonas de apuesta de los villanos y retorna las apuestas (si es que hubo)"""
    positions = {
        'V1': (.49, .57, .23, .44),
        'V2': (.30, .36, .25, .46),
        'V3': (.21, .30, .46, .67),
        'V4': (.28, .345, .55, .73),
        'V-1': (.52, .57, .61, .81)
    }
    bets = {}
    
    for villano, (top, bottom, left, right) in positions.items():
        h, w = gray_image.shape
        roi = gray_image[int(top*h):int(bottom*h), int(left*w):int(right*w)]
        
        bet_zone=get_bet_zone_roi(roi)
        if bet_zone is None:
            bet_value = None
        else:
            # cv.imshow('Match', bet_zone)
            # cv.waitKey(0)
            bet_value = recognize_text(bet_zone)
        
        if bet_value:
            # Convertir a formato numérico si es necesario (ejemplo: "$0.02" -> 0.02)
            try:
                bet_value = float(bet_value.replace('$', ''))
            except ValueError:
                pass
            
            bets[villano] = bet_value

    return bets

def recognize_dealer_position_sixP(gray_image):
    """Six Player Table: A partir de la gray image de la mesa, detecta la posición de la ficha del dealer"""
    positions = {
        'D': (.58, .68, .35, .45), # me
        'D+1': (.40, .50, .15, .20), # one
        'D+2': (.30, .40, .19, .27), # two-
        'D+3': (.22, .32, .50, .60), # three
        'D+4': (.30, .40, .72, .82), # four
        'D-1': (.52, .62, .68, .78) # five
    }

    h, w = gray_image.shape
    w_t, h_t = DEALER_TEMPLATE.shape[::-1]

    max_correlation = 0
    dealer_position = None

    for position, (top, bottom, left, right) in positions.items():
        roi = gray_image[int(top*h):int(bottom*h), int(left*w):int(right*w)]
        
        if roi.shape[0] < h_t or roi.shape[1] < w_t:
            continue  # Skip this ROI if it's smaller than the template

        result = cv.matchTemplate(roi, DEALER_TEMPLATE, cv.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv.minMaxLoc(result)

        if max_val > max_correlation:
            max_correlation = max_val
            dealer_position = position

    return dealer_position

def recognize_chips_sixP(chips_roi):
    chips = {
            'yo': recognize_text(chips_roi['yo']),
            'V1': recognize_text(chips_roi['V1']),
            'V2': recognize_text(chips_roi['V2']),
            'V3': recognize_text(chips_roi['V3']),
            'V4': recognize_text(chips_roi['V4']),
            'V-1': recognize_text(chips_roi['V-1']),
        }
    
    return chips