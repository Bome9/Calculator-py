from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import Signal
from ..config import TOP_BUTTON_SIZE


class TopButtonsWidget(QWidget):
    clear_history_clicked = Signal()
    theme_toggled = Signal()

    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.clear_history_btn = QPushButton("🗑️")
        self.clear_history_btn.setFixedSize(*TOP_BUTTON_SIZE)
        self.clear_history_btn.setObjectName("top_button")
        self.clear_history_btn.clicked.connect(self.clear_history_clicked.emit)

        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(*TOP_BUTTON_SIZE)
        self.theme_btn.setObjectName("top_button")
        self.theme_btn.clicked.connect(self.theme_toggled.emit)

        self.layout.addWidget(self.clear_history_btn)
        self.layout.addStretch()
        self.layout.addWidget(self.theme_btn)

    def set_theme_icon(self, is_dark: bool):
        self.theme_btn.setText("☀️" if is_dark else "🌙")
