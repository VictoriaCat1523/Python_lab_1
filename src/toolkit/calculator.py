"""Калькулятор математических выражений."""

from decimal import ROUND_FLOOR, Decimal, getcontext

getcontext().prec = 50

Token = tuple[str, str]


class Stack:
    """Простой стек для вычисления выражений в обратной польской записи."""

    def __init__(self) -> None:
        """Создаёт пустой стек."""
        self.items: list[Decimal] = []

    def push(self, item: Decimal) -> None:
        """Добавляет элемент на вершину стека."""
        self.items.append(item)

    def pop(self) -> Decimal:
        """Удаляет и возвращает верхний элемент стека."""
        if self.is_empty():
            raise ValueError("Некорректное выражение")

        return self.items.pop()

    def is_empty(self) -> bool:
        """Проверяет, является ли стек пустым."""
        return self.items == []


def add_number(tokens: list[Token], number: str) -> None:
    """Добавляет число в список токенов после проверки его записи."""
    if number == "":
        return

    if number.startswith(".") or number.endswith("."):
        raise ValueError("Некорректная запись вещественного числа")

    tokens.append(("NUMBER", number))


def tokenize_char(expr: str) -> list[Token]:
    """Разбивает математическое выражение на токены."""
    if expr.strip() == "":
        raise ValueError("Введена пустая строка")

    tokens: list[Token] = []
    number = ""
    i = 0

    while i < len(expr):
        char = expr[i]

        if char.isdigit() or char == ".":
            if char == "." and "." in number:
                raise ValueError("Некорректная запись вещественного числа")

            number += char
            i += 1

        elif char.isspace():
            add_number(tokens, number)
            number = ""
            i += 1

        elif char in "+-%":
            add_number(tokens, number)
            number = ""
            tokens.append(("OPERATOR", char))
            i += 1

        elif char == "*":
            add_number(tokens, number)
            number = ""

            if i + 1 < len(expr) and expr[i + 1] == "*":
                tokens.append(("OPERATOR", "**"))
                i += 2
            else:
                tokens.append(("OPERATOR", "*"))
                i += 1

        elif char == "/":
            add_number(tokens, number)
            number = ""

            if i + 1 < len(expr) and expr[i + 1] == "/":
                tokens.append(("OPERATOR", "//"))
                i += 2
            else:
                tokens.append(("OPERATOR", "/"))
                i += 1

        elif char in "()":
            add_number(tokens, number)
            number = ""
            tokens.append(("BRACKET", char))
            i += 1

        else:
            raise ValueError(f"Неизвестный символ: {char}")

    add_number(tokens, number)

    return tokens


def validate_tokens(tokens: list[Token]) -> None:
    """Проверяет синтаксическую корректность последовательности токенов."""
    if len(tokens) == 0:
        raise ValueError("Пустое выражение")

    balance = 0
    expect_value = True

    for token_type, value in tokens:
        if token_type == "NUMBER":
            if not expect_value:
                raise ValueError("Некорректная запись выражения")

            expect_value = False

        elif token_type == "BRACKET":
            if value == "(":
                if not expect_value:
                    raise ValueError("Некорректная запись выражения")

                balance += 1
                expect_value = True

            elif value == ")":
                if expect_value:
                    raise ValueError("Некорректная запись выражения")

                balance -= 1

                if balance < 0:
                    raise ValueError("Некорректная запись скобок")

                expect_value = False

        elif token_type == "OPERATOR":
            if value in ("+", "-") and expect_value:
                continue

            if expect_value:
                raise ValueError("Некорректная запись выражения")

            expect_value = True

        else:
            raise ValueError("Некорректный токен")

    if balance != 0:
        raise ValueError("Некорректная запись скобок")

    if expect_value:
        raise ValueError("Некорректная запись выражения")


def to_rpn(tokens: list[Token]) -> list[Token]:
    """Преобразует список токенов в обратную польскую запись."""
    rpn: list[Token] = []
    i = 0

    def current() -> Token | None:
        """Возвращает текущий токен."""
        if i >= len(tokens):
            return None

        return tokens[i]

    def match(value: str) -> bool:
        """Проверяет текущий токен и сдвигает позицию при совпадении."""
        nonlocal i

        token = current()

        if token is not None and token[1] == value:
            i += 1
            return True

        return False

    def expr() -> None:
        """Обрабатывает операции сложения и вычитания."""
        term()

        while True:
            if match("+"):
                term()
                rpn.append(("OPERATOR", "+"))

            elif match("-"):
                term()
                rpn.append(("OPERATOR", "-"))

            else:
                break

    def term() -> None:
        """Обрабатывает умножение, деление и остаток от деления."""
        unary()

        while True:
            if match("*"):
                unary()
                rpn.append(("OPERATOR", "*"))

            elif match("/"):
                unary()
                rpn.append(("OPERATOR", "/"))

            elif match("//"):
                unary()
                rpn.append(("OPERATOR", "//"))

            elif match("%"):
                unary()
                rpn.append(("OPERATOR", "%"))

            else:
                break

    def unary() -> None:
        """Обрабатывает унарные операторы плюс и минус."""
        if match("+"):
            unary()
            rpn.append(("OPERATOR", "u+"))

        elif match("-"):
            unary()
            rpn.append(("OPERATOR", "u-"))

        else:
            power()

    def power() -> None:
        """Обрабатывает операцию возведения в степень."""
        primary()

        if match("**"):
            unary()
            rpn.append(("OPERATOR", "**"))

    def primary() -> None:
        """Обрабатывает числа и выражения в скобках."""
        nonlocal i

        token = current()

        if token is None:
            raise ValueError("Ожидалось число или '('")

        if token[0] == "NUMBER":
            rpn.append(token)
            i += 1
            return

        if match("("):
            expr()

            if not match(")"):
                raise ValueError("Отсутствует закрывающая скобка")

            return

        raise ValueError("Ожидалось число или '('")

    expr()

    if i != len(tokens):
        raise ValueError("Некорректное выражение")

    return rpn


def calculate_rpn(rpn: list[Token]) -> Decimal:
    """Вычисляет выражение, записанное в обратной польской форме."""
    stack = Stack()

    for token_type, value in rpn:
        if token_type == "NUMBER":
            stack.push(Decimal(value))

        elif value == "u+":
            a = stack.pop()
            stack.push(a)

        elif value == "u-":
            a = stack.pop()
            stack.push(-a)

        else:
            b = stack.pop()
            a = stack.pop()

            if value == "+":
                stack.push(a + b)

            elif value == "-":
                stack.push(a - b)

            elif value == "*":
                stack.push(a * b)

            elif value == "/":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")

                stack.push(a / b)

            elif value == "//":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")

                result = (a / b).to_integral_value(
                    rounding=ROUND_FLOOR,
                )
                stack.push(result)

            elif value == "%":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")

                q = (a / b).to_integral_value(
                    rounding=ROUND_FLOOR,
                )
                stack.push(a - b * q)

            elif value == "**":
                stack.push(a**b)

            else:
                raise ValueError("Неизвестный оператор")

    if len(stack.items) != 1:
        raise ValueError("Некорректное выражение")

    return stack.pop()


def calculator(expr: str) -> Decimal:
    """Вычисляет математическое выражение и возвращает результат."""
    tokens = tokenize_char(expr)
    validate_tokens(tokens)
    rpn = to_rpn(tokens)

    return calculate_rpn(rpn)
