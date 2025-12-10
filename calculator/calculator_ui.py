from PySide6.QtWidgets import QWidget, QVBoxLayout
from .config import BUTTONS, WINDOW_TITLE, WINDOW_SIZE
from .ui.ui_display import DisplayWidget
from .ui.ui_top_buttons import TopButtonsWidget
from .ui.ui_history import HistoryWidget
from .ui.ui_themes import ThemeManager
from .ui.ui_buttons import ButtonHandler, ButtonGrid


class CalculatorUI(QWidget):
    def __init__(self, logic, history):
        super().__init__()
        self.logic = logic
        self.history = history

        self._setup_components()
        self._setup_ui()
        self._connect_signals()

    def _setup_components(self):
        self.theme_manager = ThemeManager(self)
        self.button_handler = ButtonHandler(self.logic, self.history)
        self.display = DisplayWidget()
        self.top_buttons = TopButtonsWidget()
        self.history_widget = HistoryWidget()
        self.button_grid = ButtonGrid(BUTTONS, self.button_handler)

    def _setup_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(300, 300, *WINDOW_SIZE)

        layout = QVBoxLayout(self)
        layout.addWidget(self.top_buttons)
        layout.addWidget(self.display)
        layout.addWidget(self.history_widget)
        layout.addLayout(self.button_grid)

        self.theme_manager.apply_theme()
        self._update_history()
        self.display.setText("0")

    def _connect_signals(self):
        self.top_buttons.clear_history_clicked.connect(self._clear_history)
        self.top_buttons.theme_toggled.connect(self._toggle_theme)
        self.button_handler.expression_changed.connect(self.display.setText)
        self.button_handler.history_updated.connect(self._update_history)
        self.button_handler.trig_toggled.connect(self._on_trig_toggled)

    def _toggle_theme(self):
        is_dark = self.theme_manager.toggle_theme()
        self.top_buttons.set_theme_icon(is_dark)

    def _clear_history(self):
        self.history.history = []
        self.history.save_history()
        self._update_history()

    def _update_history(self):
        hist = self.history.get_history()
        self.history_widget.update_history(hist)

    def _on_trig_toggled(self, show: bool):
        self.button_grid.update_trig_visibility(show)
        new_height = WINDOW_SIZE[1] + 70 if show else WINDOW_SIZE[1]
        self.setGeometry(300, 300, WINDOW_SIZE[0], new_height)
