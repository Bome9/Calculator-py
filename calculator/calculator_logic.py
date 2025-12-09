import math
import operator

class CalculatorLogic:
    """
    Класс для логики калькулятора. Безопасные математические операции без eval().
    """

    def __init__(self):
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '%': operator.mod,
            '^': operator.pow,
        }
        self.functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'sqrt': math.sqrt,
            'log': math.log10,
        }

    def evaluate(self, expression):
        """
        Вычисляет математическое выражение.
        :param expression: str, математическое выражение
        :return: float or str (ошибка)
        """
        try:
            # Простой парсер для демонстрации. В реальности нужен полноценный парсер.
            # Для простоты, использовать eval с проверкой, но задача запрещает.
            # Реализовать базовый парсер.
            # Для junior, использовать ast.literal_eval, но для выражений.
            # Использовать библиотеку, но лучше ручной.

            # Токенизация
            tokens = self._tokenize(expression)
            result = self._parse_expression(tokens)
            return result
        except ZeroDivisionError:
            return "Ошибка: деление на ноль"
        except ValueError:
            return "Ошибка: неверное выражение"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    def _tokenize(self, expr):
        """
        Разбивает выражение на токены.
        """
        import re
        # Токенизация с функциями
        token_pattern = r'(\d+\.?\d*|sin|cos|tan|sqrt|log|[+\-*/%^()])'
        tokens = re.findall(token_pattern, expr)
        return tokens

    def _parse_expression(self, tokens):
        """
        Парсер выражений с использованием алгоритма Shunting-yard.
        Поддерживает операции, функции и скобки.
        """
        def shunting_yard(tokens):
            output = []
            operators = []
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
            functions = set(self.functions.keys())
            for token in tokens:
                if token.replace('.', '').isdigit():
                    output.append(float(token))
                elif token in functions:
                    operators.append(token)
                elif token in precedence:
                    while operators and operators[-1] in precedence and precedence[operators[-1]] >= precedence[token]:
                        output.append(operators.pop())
                    operators.append(token)
                elif token == '(':
                    operators.append(token)
                elif token == ')':
                    while operators and operators[-1] != '(':
                        output.append(operators.pop())
                    if operators:
                        operators.pop()  # Удалить '('
                    # Если предыдущий оператор - функция, применить её
                    if operators and operators[-1] in functions:
                        output.append(operators.pop())
            while operators:
                output.append(operators.pop())
            return output

        postfix = shunting_yard(tokens)

        # Вычислить постфикс
        stack = []
        for token in postfix:
            if isinstance(token, float):
                stack.append(token)
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Недостаточно операндов")
                b = stack.pop()
                a = stack.pop()
                if token == '/' and b == 0:
                    raise ZeroDivisionError
                stack.append(self.operators[token](a, b))
            elif token in self.functions:
                if not stack:
                    raise ValueError("Недостаточно операндов для функции")
                a = stack.pop()
                stack.append(self.functions[token](a))
        if len(stack) != 1:
            raise ValueError("Неверное выражение")
        return stack[0]
