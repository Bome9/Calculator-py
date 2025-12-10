import math
from PySide6.QtWidgets import QGridLayout, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Signal, QObject
from ..config import BUTTON_FONT_SIZE, OPERATION_FONT_SIZE, BUTTON_SIZE
import re


class ButtonHandler(QObject):
    expression_changed = Signal(str)
    history_updated = Signal()

    def __init__(self, logic, history):
        super().__init__()
        self.logic = logic
        self.history = history
        self.current_expression = "0"
        self.show_trig = False
        self.last_operation = None
        self.last_operand = None
        self.last_was_equal = False

    def handle_button_click(self, text: str):
        if text == "AC":
            self._handle_clear()
        elif text == "del":
            self._handle_delete()
        elif text == "±":
            self._handle_toggle_sign()
        elif text in ("1/x", "x²", "√"):
            self._handle_unary_op(text)
        elif text in ("sin", "cos", "tan", "ctg"):
            self._handle_trig(text)
        elif text == "=":
            self._handle_equal()
        elif text == "trig":
            self.toggle_trig()
        else:
            self._handle_input(text)
        self.expression_changed.emit(self.current_expression)

    def _handle_clear(self):
        self.current_expression = "0"

    def _handle_delete(self):
        if not self.current_expression.startswith("Ошибка"):
            self.current_expression = self.current_expression[:-1] or "0"

    def _handle_toggle_sign(self):
        if not self.current_expression.startswith("Ошибка"):
            if self.current_expression.startswith("-"):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = "-" + self.current_expression

    def _handle_input(self, text: str):
        if self.current_expression.startswith("Ошибка"):
            self.current_expression = text
            self.last_operation = None
            self.last_operand = None
            self.last_was_equal = False
        else:
            if text.isdigit() or text == ".":
                if self.current_expression == "0" or self.last_was_equal:
                    self.current_expression = text
                    self.last_operation = None
                    self.last_operand = None
                    self.last_was_equal = False
                else:
                    self.current_expression += text
            else:
                self.current_expression += text
                self.last_was_equal = False

    def _handle_unary_op(self, op: str):
        if self.current_expression.startswith("Ошибка"):
            return
        try:
            val = float(self.current_expression)

            if op == "1/x":
                if val == 0:
                    raise ZeroDivisionError
                result = 1 / val
                expr = f"1/{self.current_expression}"

            elif op == "x²":
                result = val**2
                expr = f"{self.current_expression}²"

            else:  # √
                result = math.sqrt(val)
                expr = f"√{self.current_expression}"
            self.history.add_entry(expr, str(result))
            self.history_updated.emit()
            self.current_expression = str(result)

        except ZeroDivisionError:
            self.current_expression = "Ошибка: деление на ноль"
        except Exception:
            self.current_expression = "Ошибка"

    def _handle_trig(self, func: str):
        if self.current_expression.startswith("Ошибка"):
            return
        expr = f"{func}({self.current_expression})"
        result = self.logic.evaluate(expr)
        if not isinstance(result, str) or not result.startswith("Ошибка"):
            self.history.add_entry(expr, str(result))
            self.history_updated.emit()
        self.current_expression = str(result)

    def _handle_equal(self):
        if self.current_expression.startswith("Ошибка"):
            return

        if self.last_was_equal and self.last_operation and self.last_operand:
            expr = f"{self.current_expression} {self.last_operation} {self.last_operand}"
            result = self.logic.evaluate(expr)
            if not isinstance(result, str) or not result.startswith("Ошибка"):
                self.history.add_entry(expr, str(result))
                self.history_updated.emit()
        else:
            result = self.logic.evaluate(self.current_expression)
            if not isinstance(result, str) or not result.startswith("Ошибка"):
                self.history.add_entry(self.current_expression, str(result))
                self.history_updated.emit()
                self._parse_last_operation(self.current_expression)

        self.current_expression = str(result)
        self.last_was_equal = True

    def toggle_trig(self):
        self.show_trig = not self.show_trig
        self.trig_toggled.emit(self.show_trig)

    trig_toggled = Signal(bool)

    def _parse_last_operation(self, expr: str):
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)$', expr)
        if match:
            self.last_operation = match.group(2)
            self.last_operand = match.group(3)
        else:
            self.last_operation = None
            self.last_operand = None


class ButtonGrid(QGridLayout):
    def __init__(self, buttons_config: list, handler: ButtonHandler):
        super().__init__()
        self.buttons = {}
        self.handler = handler
        self._create_buttons(buttons_config)

    def _create_buttons(self, buttons_config: list):
        for text, row, col in buttons_config:
            button = QPushButton(text)
            button.setFont(QFont("Arial", BUTTON_FONT_SIZE))
            button.setFixedSize(*BUTTON_SIZE)

            # Подключение сигнала
            button.clicked.connect(lambda checked, t=text: self.handler.handle_button_click(t))

            self.addWidget(button, row, col)
            self.buttons[text] = button

            # Оформление кнопок
            if text in ["/", "*", "-", "+", "=", "del"]:
                button.setFont(QFont("Arial", OPERATION_FONT_SIZE))
                button.setObjectName("del" if text == "del" else "operation")
            elif row >= 2:
                button.setObjectName("secondary")

            # Скрытые триггерные
            if row == 6:
                button.setVisible(False)

    def update_trig_visibility(self, show: bool):
        for btn in ["sin", "cos", "tan", "ctg"]:
            if btn in self.buttons:
                self.buttons[btn].setVisible(show)
