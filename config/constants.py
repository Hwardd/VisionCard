from config.configHelpers import load_card_templates


TEMPLATE_DIR = "./images/handCards"

ALL_CARD_TEMPLATES = load_card_templates(TEMPLATE_DIR)

TABLE_SCREENSHOT_PATH = "screenshot.png"

ALL_CONSTS = {
    "TEMPLATE_DIR": TEMPLATE_DIR,
    "ALL_CARD_TEMPLATES": ALL_CARD_TEMPLATES,
    "TABLE_SCREENSHOT_PATH": TABLE_SCREENSHOT_PATH
}
