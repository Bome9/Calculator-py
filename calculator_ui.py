from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class CalculatorUI(QWidget):
    """
    Класс пользовательского интерфейса калькулятора.
    """

    def __init__(self, logic, history):
        super().__init__()
        self.logic = logic
        self.history = history
        self.current_expression = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calculator")
        self.setGeometry(300, 300, 300, 570)  # Увеличить высоту для кнопок
        self.show_trig = False  # Показывать ли тригонометрию
        self.dark_mode = False  # Темная тема

        # Основной layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Кнопки вверху
        top_layout = QHBoxLayout()
        self.clear_history_btn = QPushButton("🗑️")
        self.clear_history_btn.setFixedSize(40, 35)
        self.clear_history_btn.setObjectName("top_button")
        self.clear_history_btn.clicked.connect(self.clear_history)
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedSize(40, 35)
        self.theme_btn.setObjectName("top_button")
        self.theme_btn.clicked.connect(self.toggle_theme)
        top_layout.addWidget(self.clear_history_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.theme_btn)
        layout.addLayout(top_layout)

        # Дисплей
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Arial", 24))
        layout.addWidget(self.display)

        # История
        self.history_display = QTextEdit()
        self.history_display.setMaximumHeight(100)
        self.history_display.setReadOnly(True)
        layout.addWidget(self.history_display)

        # Кнопки в grid
        buttons_layout = QGridLayout()

        buttons = [
            ('C', 0, 0), ('±', 0, 1), ('%', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('trig', 4, 0), ('0', 4, 1), ('.', 4, 2), ('=', 4, 3),
            ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('sqrt', 5, 3),
        ]

        self.buttons = {}
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFont(QFont("Arial", 14))
            button.setFixedSize(60, 60)  # Круглые кнопки
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            buttons_layout.addWidget(button, row, col)
            self.buttons[text] = button
            if text in ['/', '*', '-', '+', '=']:
                button.setObjectName("operation")
                button.setFont(QFont("Arial", 18))  # Больше шрифт для операций
            elif row >= 1:  # Начиная со второй строки, не оранжевые
                button.setObjectName("secondary")
            if row == 5:  # Скрыть ряд тригонометрии
                button.setVisible(False)

        layout.addLayout(buttons_layout)

        self.apply_theme()

        self.update_history_display()

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
        if self.show_trig:
            self.setGeometry(300, 300, 300, 550 + 70)  # + высота ряда
        else:
            self.setGeometry(300, 300, 300, 550)

    def apply_theme(self):
        """
        Применяет текущую тему.
        """
        if self.dark_mode:
            self.setStyleSheet("""
                QWidget {
                    background-color: #1c1c1e;
                }
                QLineEdit {
                    background-color: #2c2c2e;
                    border: 2px solid #3c3c3e;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                    color: white;
                }
                QPushButton {
                    background-color: #48484a;
                    border: none;
                    border-radius: 30px;
                    font-size: 20px;
                    color: white;
                }
                QPushButton:hover {
                    background-color: #5c5c5e;
                }
                QPushButton:pressed {
                    background-color: #6c6c6e;
                }
                QPushButton#secondary {
                    background-color: #3c3c3e;
                }
                QPushButton#secondary:hover {
                    background-color: #4c4c4e;
                }
                QPushButton#secondary:pressed {
                    background-color: #5c5c5e;
                }
                QPushButton#operation {
                    background-color: #ff9500;
                    font-size: 30px;
                    color: white;
                }
                QPushButton#operation:hover {
                    background-color: #e67e00;
                }
                QPushButton#operation:pressed {
                    background-color: #cc6600;
                }
                QPushButton#top_button {
                    border-radius: 8px;
                }
                QTextEdit {
                    background-color: #2c2c2e;
                    border: 2px solid #3c3c3e;
                    border-radius: 10px;
                    font-size: 12px;
                    padding: 2px;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f5f5f7;
                }
                QLineEdit {
                    background-color: white;
                    border: 2px solid #ccc;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 24px;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    border: none;
                    border-radius: 30px;
                    font-size: 20px;
                    color: black;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #c0c0c0;
                }
                QPushButton#secondary {
                    background-color: #c0c0c0;
                }
                QPushButton#secondary:hover {
                    background-color: #b0b0b0;
                }
                QPushButton#secondary:pressed {
                    background-color: #a0a0a0;
                }
                QPushButton#operation {
                    background-color: #ff9500;
                    font-size: 30px;
                    color: white;
                }
                QPushButton#operation:hover {
                    background-color: #e67e00;
                }
                QPushButton#operation:pressed {
                    background-color: #cc6600;
                }
                QPushButton#top_button {
                    border-radius: 8px;
                }
                QTextEdit {
                    background-color: white;
                    border: 2px solid #ccc;
                    border-radius: 10px;
                    font-size: 12px;
                    padding: 2px;
                }
            """)

    def toggle_theme(self):
        """
        Переключает тему.
        """
        self.dark_mode = not self.dark_mode
        self.theme_btn.setText("☀️" if self.dark_mode else "🌙")
        self.apply_theme()

    def clear_history(self):
        """
        Очищает историю вычислений.
        """
        self.history.history = []
        self.history.save_history()
        self.update_history_display()

    def update_history_display(self):
        """
        Обновляет отображение истории.
        """
        hist = self.history.get_history()
        self.history_display.setText('\n'.join(hist[-5:]))  # Показать последние 5 записей
