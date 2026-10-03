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

        elif char in "+-*%":
            add_number(tokens, number)
            number = ""

            tokens.append(("OPERATOR", char))
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

