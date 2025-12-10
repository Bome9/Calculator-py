from PySide6.QtWidgets import QTextEdit
from ..config import HISTORY_DISPLAY_HEIGHT


class HistoryWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(HISTORY_DISPLAY_HEIGHT)
        self.setReadOnly(True)

    def update_history(self, history_list: list[str]):
        self.setText("\n".join(reversed(history_list[-5:])))
