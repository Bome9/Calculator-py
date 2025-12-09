"""
Конфигурационные константы для калькулятора.
"""

import os

BUTTONS = [
    ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('/', 0, 3),
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
    ('trig', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
    ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('sqrt', 5, 3),
]

WINDOW_TITLE = "Calculator"
WINDOW_SIZE = (300, 570)
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
