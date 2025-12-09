import math

class CalculatorLogic:
    def __init__(self):
        self.safe_dict = {
            '__builtins__': None,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,
            'pow': math.pow,
            'pi': math.pi,
            'e': math.e,
        }

    def evaluate(self, expression):
        try:
            result = eval(expression, {"__builtins__": None}, self.safe_dict)
            return result
        except ZeroDivisionError:
            return "Ошибка: деление на ноль"
        except Exception:
            return "Ошибка: неверное выражение"
