from config.configHelpers import load_card_templates
import cv2 as cv
from visionStuff.allPlayers.otherHelpers import image_to_mat


TEMPLATE_DIR = "./images/handCards"

ALL_CARD_TEMPLATES = load_card_templates(TEMPLATE_DIR)

TABLE_SCREENSHOT_PATH = "screenshot.png"

DEALER_TEMPLATE = image_to_mat('./images/others/dealer.png')

BET_DOLLAR_SIGN_TEMPLATE = dealer_template =image_to_mat('./images/others/betDolarSign.png')

AC_TEMPLATE=image_to_mat('./images/handCards/Ac.png')

AS_TEMPLATE=image_to_mat('./images/handCards/As.png')

ALL_CONSTS = {
    "TEMPLATE_DIR": TEMPLATE_DIR,
    "ALL_CARD_TEMPLATES": ALL_CARD_TEMPLATES,
    "TABLE_SCREENSHOT_PATH": TABLE_SCREENSHOT_PATH
}
