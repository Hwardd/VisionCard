from config.configHelpers import take_table_screenshot
from config.constants import ALL_CARD_TEMPLATES, DEALER_TEMPLATE, TABLE_SCREENSHOT_PATH
from visionStuff.otherOperations import image_to_mat
from visionStuff.positioExtractors import (get_my_chips_roi, get_my_game_roi, get_my_hand_roi,
    get_pot_amount_roi, get_table_cards_roi, roi_detector_tester)
from visionStuff.imageRecognition import (detect_dealer_position, extract_bets_from_positions,
    recognize_cards, recognize_text_from_mat)
from utils.stringUtils import string_text_cleaner
import pyperclip

def gameExtractor():
    take_table_screenshot(TABLE_SCREENSHOT_PATH)
    gray_image = image_to_mat(TABLE_SCREENSHOT_PATH)


    bets = extract_bets_from_positions(gray_image)

    my_hand_roi = get_my_hand_roi(gray_image)
    my_hand = recognize_cards(my_hand_roi, ALL_CARD_TEMPLATES)
    
    table_cards_roi = get_table_cards_roi(gray_image)
    table_cards = recognize_cards(table_cards_roi, ALL_CARD_TEMPLATES)
    
    pot_amount_roi = get_pot_amount_roi(gray_image)
    pot_amount = recognize_text_from_mat(pot_amount_roi)

    my_chips_roi = get_my_chips_roi(gray_image)
    my_chips = recognize_text_from_mat(my_chips_roi)
    
    position = detect_dealer_position(gray_image, DEALER_TEMPLATE)

    my_game_roi = get_my_game_roi(gray_image)
    my_game = recognize_text_from_mat(my_game_roi)
    # roi_tester(my_chips_roi)


    text_to_print = '\n\n' + str({
        "mano": my_hand,
        "cartas_mesa": table_cards,
        "mis_fichas": my_chips,
        "juego_formado_con_mesa": string_text_cleaner(my_game),
        "posicion": position,
        "pot": pot_amount,
        "Apuestas_aprox_villanos": bets
    }) + '\nSolo dime accion inmediata recomendada primero (check, fold, call, rise (con la cantidad) y en caso de que sea check o call cuanto pagar máximo)'
    # }) + '\nSolo dime accion inmediata recomendada primero (check, fold, call, rise (con la cantidad) y en caso de que sea check o call cuanto pagar máximo)\nDespues tambien dime una estrategia resumida para siguientes fases de este juego (check fold, no pagues mas de tanto, etc) '

    print(text_to_print)

    # Copiar al portapapeles
    pyperclip.copy(text_to_print)

