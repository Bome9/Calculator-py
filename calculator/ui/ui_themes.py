import os
from PySide6.QtWidgets import QWidget
from ..config import THEME_DIR, LIGHT_THEME_FILE, DARK_THEME_FILE


class ThemeManager:
    def __init__(self, widget: QWidget):
        self.widget = widget
        self.dark_mode = False

    def apply_theme(self):
        filename = os.path.join(
            THEME_DIR, DARK_THEME_FILE if self.dark_mode else LIGHT_THEME_FILE
        )
        try:
            with open(filename, "r", encoding="utf-8") as file:
                self.widget.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Файл стиля {filename} не найден.")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        return self.dark_mode
