import os

BUTTONS = [
    ('%', 0, 0), ('±', 0, 1), ('AC', 0, 2), ('del', 0, 3),
    ('1/x', 1, 0), ('x²', 1, 1), ('√', 1, 2), ('/', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
    ('trig', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
    ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('sqrt', 6, 3),
]

WINDOW_TITLE = "Calculator"
WINDOW_SIZE = (300, 630)
DISPLAY_FONT_SIZE = 24
BUTTON_FONT_SIZE = 14
OPERATION_FONT_SIZE = 18
BUTTON_SIZE = (60, 60)
TOP_BUTTON_SIZE = (40, 35)

THEME_DIR = os.path.join(os.path.dirname(__file__), "themes")
LIGHT_THEME_FILE = "light.qss"
DARK_THEME_FILE = "dark.qss"
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.txt")
HISTORY_DISPLAY_HEIGHT = 100
