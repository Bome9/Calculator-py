import sys
from PySide6.QtWidgets import QApplication
from calculator_logic import CalculatorLogic
from calculator_history import CalculatorHistory
from calculator_ui import CalculatorUI

def main():
    """
    Основная функция приложения.
    """
    app = QApplication(sys.argv)

    logic = CalculatorLogic()
    history = CalculatorHistory()
    ui = CalculatorUI(logic, history)

    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
