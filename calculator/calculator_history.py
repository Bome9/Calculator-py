import os
from .config import HISTORY_FILE

class CalculatorHistory:
    def __init__(self, filename=HISTORY_FILE):
        self.filename = filename
        self.history = []
        self.load_history()

    def add_entry(self, expression, result):
        entry = f"{expression} = {result}"
        self.history.append(entry)
        self.save_history()

    def get_history(self):
        return self.history.copy()

    def save_history(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                for entry in self.history:
                    f.write(entry + '\n')
        except Exception as e:
            print(f"Ошибка сохранения истории: {e}")

    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print(f"Ошибка загрузки истории: {e}")
                self.history = []
