from decimal import Decimal, ROUND_FLOOR, getcontext
getcontext().prec = 50

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Некорректное выражение")
        return self.items.pop()

    def is_empty(self):
        return self.items == []

def add_number(tokens, number):
    if number == "":
        return

    if number.startswith(".") or number.endswith("."):
        raise ValueError("Некорректная запись вещественного числа")

    tokens.append(("NUMBER", number))


def tokenize_char(expr: str):
    if expr.strip() == "":
        raise ValueError("Введена пустая строка")

    tokens = []
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


def to_rpn(tokens):
    rpn = []
    i = 0

    def current():
        if i >= len(tokens):
            return None
        return tokens[i]

    def match(value):
        nonlocal i

        token = current()
        if token is not None and token[1] == value:
            i += 1
            return True
        return False

    def expr():
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

    def term():
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

    def unary():
        if match("+"):
            unary()
            rpn.append(("OPERATOR", "u+"))

        elif match("-"):
            unary()
            rpn.append(("OPERATOR", "u-"))

        else:
            power()

    def power():
        primary()

        if match("**"):
            unary()
            rpn.append(("OPERATOR", "**"))

    def primary():
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
        if current()[1] == ")":
            raise ValueError("Лишняя закрывающая скобка")

        raise ValueError("Некорректное выражение")

    return rpn

def calculate_rpn(rpn):
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
                    rounding=ROUND_FLOOR
                )

                stack.push(result)

            elif value == "%":
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")

                q = (a / b).to_integral_value(
                    rounding=ROUND_FLOOR
                )

                stack.push(a - b * q)

            elif value == "":
                stack.push(a ** b)

    if len(stack.items) != 1:
        raise ValueError("Некорректное выражение")

    return stack.pop()


def calculator(expr):
    tokens = tokenize_char(expr)

    rpn = to_rpn(tokens)

    result = calculate_rpn(rpn)

    return result