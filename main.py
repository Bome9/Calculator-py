import sys
from PySide6.QtWidgets import QApplication
from calculator import CalculatorLogic, CalculatorHistory, CalculatorUI

def main():

    app = QApplication(sys.argv)

    logic = CalculatorLogic()
    history = CalculatorHistory()
    ui = CalculatorUI(logic, history)

    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
