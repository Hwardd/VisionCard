from config.configHelpers import take_table_screenshot
from config.constants import ALL_CARD_TEMPLATES, DEALER_TEMPLATE, TABLE_SCREENSHOT_PATH
from utils.stringUtils import string_text_cleaner
import pyperclip
from visionStuff.allPlayers.otherHelpers import image_to_mat
from visionStuff.sixPlayers.elementsRecognition import (recognize_bets_sixP, recognize_chips_sixP,
    recognize_dealer_position_sixP)
from visionStuff.allPlayers.roiExtractors import (get_my_chips_roi, get_my_game_roi,
    get_my_hand_roi, get_pot_amount_roi, get_table_cards_roi)
from visionStuff.allPlayers.elementsRecognition import recognize_cards, recognize_text
from visionStuff.sixPlayers.roiExtractors import get_chips_sixP

def six_players_normal_table_extractor():
    take_table_screenshot(TABLE_SCREENSHOT_PATH)
    gray_image = image_to_mat(TABLE_SCREENSHOT_PATH)
    
    chips_roi=get_chips_sixP(gray_image)
    chips=recognize_chips_sixP(chips_roi)

    bets = recognize_bets_sixP(gray_image)

    my_hand_roi = get_my_hand_roi(gray_image)
    my_hand = recognize_cards(my_hand_roi)
    
    table_cards_roi = get_table_cards_roi(gray_image)
    table_cards = recognize_cards(table_cards_roi)
    
    pot_amount_roi = get_pot_amount_roi(gray_image)
    pot_amount = recognize_text(pot_amount_roi)

    position = recognize_dealer_position_sixP(gray_image)

    my_game_roi = get_my_game_roi(gray_image)
    my_game = recognize_text(my_game_roi)
    # roi_tester(my_chips_roi)


    text_to_print = str({
        "mano": my_hand,
        "cartas_mesa": table_cards,
        "juego_formado_con_mesa": string_text_cleaner(my_game),
        "posicion": position,
        "pot": pot_amount,
        "fichas": chips,
        "Apuestas_aprox_villanos": bets
    # }) + '\nSolo dime accion inmediata recomendada primero (check, fold, call, rise (con la cantidad) y en caso de que sea check o call cuanto pagar máximo)'
    }) + '\nSolo dime accion inmediata recomendada primero (check, fold, call, rise (con la cantidad) y en caso de que sea check o call cuanto pagar máximo)\nDespues tambien dime una estrategia resumida para siguientes fases de este juego (check fold, no pagues mas de tanto, etc) '

    print('\n\n',text_to_print)

    # Copiar al portapapeles
    pyperclip.copy(text_to_print)

