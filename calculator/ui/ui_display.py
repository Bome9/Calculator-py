from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from ..config import DISPLAY_FONT_SIZE


class DisplayWidget(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setAlignment(Qt.AlignRight)
        self.setFont(QFont("Arial", DISPLAY_FONT_SIZE))
