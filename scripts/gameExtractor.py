from config.configHelpers import take_table_screenshot
from config.constants import ALL_CARD_TEMPLATES, TABLE_SCREENSHOT_PATH
from visionStuff.otherOperations import image_to_mat
from visionStuff.positioExtractors import get_my_hand_roi, get_pot_amount_roi, get_table_cards_roi
from visionStuff.imageRecognition import recognize_cards, recognize_text_from_mat

def gameExtractor():
    take_table_screenshot(TABLE_SCREENSHOT_PATH)
    gray_image = image_to_mat(TABLE_SCREENSHOT_PATH)

    my_hand_roi = get_my_hand_roi(gray_image)
    table_cards_roi = get_table_cards_roi(gray_image)
    pot_amount_roi = get_pot_amount_roi(gray_image)

    my_hand = recognize_cards(my_hand_roi, ALL_CARD_TEMPLATES)
    table_cards = recognize_cards(table_cards_roi, ALL_CARD_TEMPLATES)
    pot_amount = recognize_text_from_mat(pot_amount_roi)

    print({
        "myHand": my_hand,
        "tableCards": table_cards,
        "potAmount": pot_amount
    })


