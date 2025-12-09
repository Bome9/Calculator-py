from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class CalculatorUI(QWidget):
    """
    Класс пользовательского интерфейса калькулятора.
    Стиль в духе Apple Calculator: серые цвета, округлые кнопки, минимализм.
    """

    def __init__(self, logic, history):
        super().__init__()
        self.logic = logic
        self.history = history
        self.current_expression = ""
        self.init_ui()

    def init_ui(self):
        """
        Инициализация интерфейса.
        """
        self.setWindowTitle("Calculator")
        self.setGeometry(300, 300, 300, 550)
        self.ac_mode = True  # Режим AC
        self.show_trig = False  # Показывать ли тригонометрию

        # Основной layout
        layout = QVBoxLayout()
        self.setLayout(layout)

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
            ('AC', 0, 0), ('±', 0, 1), ('%', 0, 2), ('/', 0, 3),
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
            if row == 5:  # Скрыть ряд тригонометрии
                button.setVisible(False)

        layout.addLayout(buttons_layout)

        # Стилизация
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
            QPushButton#operation {
                background-color: #ff9500;
                font-size: 20px;
                color: white;
            }
            QPushButton#operation:hover {
                background-color: #e67e00;
            }
            QPushButton#operation:pressed {
                background-color: #cc6600;
            }
            QTextEdit {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 10px;
                font-size: 12px;
            }
        """)

        self.update_history_display()

    def on_button_click(self, text):
        """
        Обработчик нажатия кнопки.
        """
        if text == 'AC':
            self.current_expression = ""
            self.ac_mode = True
            self.buttons['AC'].setText('AC')
        elif text == 'C':
            self.current_expression = self.current_expression[:-1]
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
            if self.ac_mode:
                self.ac_mode = False
                self.buttons['AC'].setText('C')
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

    def update_history_display(self):
        """
        Обновляет отображение истории.
        """
        hist = self.history.get_history()
        self.history_display.setText('\n'.join(hist[-10:]))  # Показать последние 10 записей
