from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
import os
from .config import (
    BUTTONS, WINDOW_TITLE, WINDOW_SIZE, DISPLAY_FONT_SIZE,
    BUTTON_FONT_SIZE, OPERATION_FONT_SIZE, BUTTON_SIZE,
    TOP_BUTTON_SIZE, THEME_DIR, LIGHT_THEME_FILE, DARK_THEME_FILE,
    HISTORY_DISPLAY_HEIGHT
)

class CalculatorUI(QWidget):
    """
    Класс пользовательского интерфейса калькулятора.
    """

    def __init__(self, logic, history):
        super().__init__()
        self.logic = logic
        self.history = history
        self.current_expression = ""
        self.buttons_config = BUTTONS
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(300, 300, *WINDOW_SIZE)
        self.show_trig = False
        self.dark_mode = False

        layout = QVBoxLayout()
        self.setLayout(layout)

        self._setup_top_buttons()
        self._setup_display()
        self._setup_history()
        self._setup_buttons()

        self.apply_theme()
        self.update_history_display()

    def _setup_top_buttons(self):
        """
        Настройка верхних кнопок (очистка истории и переключение темы).
        """
        top_layout = QHBoxLayout()
        self.clear_history_btn = QPushButton("🗑️")
        self.clear_history_btn.setFixedSize(*TOP_BUTTON_SIZE)
        self.clear_history_btn.setObjectName("top_button")
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(*TOP_BUTTON_SIZE)
        self.theme_btn.setObjectName("top_button")
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_layout.addWidget(self.clear_history_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)
        self.layout().addLayout(top_layout)

    def _setup_display(self):
        """
        Настройка дисплея выражения.
        """
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", DISPLAY_FONT_SIZE))
        self.layout().addWidget(self.display)

    def _setup_history(self):
        """
        Настройка дисплея истории.
        """
        self.history_display = QTextEdit()
        self.history_display.setMaximumHeight(HISTORY_DISPLAY_HEIGHT)
        self.history_display.setReadOnly(True)
        self.layout().addWidget(self.history_display)

    def _setup_buttons(self):
        """
        Настройка кнопок калькулятора.
        """
        buttons_layout = QGridLayout()
        self.buttons = {}
        for text, row, col in self.buttons_config:
            button = QPushButton(text)
            button.setFont(QFont("Arial", BUTTON_FONT_SIZE))
            button.setFixedSize(*BUTTON_SIZE)
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            buttons_layout.addWidget(button, row, col)
            self.buttons[text] = button
            if text in ['/', '*', '-', '+', '=']:
                button.setObjectName("operation")
                button.setFont(QFont("Arial", OPERATION_FONT_SIZE))
            elif row >= 1:
                button.setObjectName("secondary")
            if row == 5:
                button.setVisible(False)
        self.layout().addLayout(buttons_layout)

    def on_button_click(self, text):
        """
        Обработчик нажатия кнопки.
        """
        if text == 'C':
            self.current_expression = self.current_expression[:-1]  # Удалить последний символ
        elif text == 'trig':
            self.toggle_trig()
        elif text == '±':
            if self.current_expression and self.current_expression[-1].isdigit():
                # Найти последнее число и изменить знак
                # Простая реализация: добавить - в начало, но нужно парсить
                if self.current_expression.startswith('-'):
                    self.current_expression = self.current_expression[1:]
                else:
                    self.current_expression = '-' + self.current_expression
        elif text == '=':
            result = self.logic.evaluate(self.current_expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            if not isinstance(result, str) or not result.startswith("Ошибка"):
                self.history.add_entry(self.current_expression, str(result))
                self.update_history_display()
            self.current_expression = str(result)
        else:
            self.current_expression += text
        self.display.setText(self.current_expression)

    def toggle_trig(self):
        """
        Переключает видимость тригонометрических функций.
        """
        self.show_trig = not self.show_trig
        for btn in ['sin', 'cos', 'tan', 'sqrt']:
            if btn in self.buttons:
                self.buttons[btn].setVisible(self.show_trig)
        # Изменить высоту окна
        height = WINDOW_SIZE[1] + 70 if self.show_trig else WINDOW_SIZE[1]
        self.setGeometry(300, 300, WINDOW_SIZE[0], height)

    def apply_theme(self):
        """
        Применяет текущую тему, загружая QSS из файла.
        """
        filename = os.path.join(THEME_DIR, DARK_THEME_FILE if self.dark_mode else LIGHT_THEME_FILE)
        try:
            with open(filename, "r", encoding="utf-8") as f:
                style = f.read()
            self.setStyleSheet(style)
        except FileNotFoundError:
            print(f"Файл стиля {filename} не найден.")

    def toggle_theme(self):
        """
        Переключает тему.
        """
        self.dark_mode = not self.dark_mode
        self.theme_btn.setText("☀️" if self.dark_mode else "🌙")
        self.apply_theme()

    def clear_history(self):
        """
        Очищает историю вычислений и текущий ввод.
        """
        self.history.history = []
        self.history.save_history()
        self.update_history_display()
        self.current_expression = ""
        self.display.setText("")

    def update_history_display(self):
        """
        Обновляет отображение истории.
        """
        hist = self.history.get_history()
        self.history_display.setText('\n'.join(hist[-5:]))  # Показать последние 5 записей
