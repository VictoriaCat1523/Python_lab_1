"""Интерфейс командной строки пакета toolkit."""

import argparse
from decimal import Decimal

from .calculator import calculator
from .converter import convert


def format_decimal(value: Decimal) -> str:
    """Форматирует Decimal для вывода без лишних нулей."""
    text = format(value, "f")

    if "." in text:
        text = text.rstrip("0").rstrip(".")

    if text == "-0":
        text = "0"

    return text


def main() -> None:
    """Запускает интерфейс командной строки toolkit."""
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Калькулятор и конвертер величин",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    calc_parser = subparsers.add_parser(
        "calc",
        help="Вычислить математическое выражение",
    )
    calc_parser.add_argument(
        "expression",
        help="Математическое выражение",
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Конвертировать величину",
    )
    convert_parser.add_argument(
        "value",
        help="Значение",
    )
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Исходная единица измерения",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Конечная единица измерения",
    )

    args = parser.parse_args()

    try:
        if args.command == "calc":
            result = calculator(args.expression)
            print(format_decimal(result))

        elif args.command == "convert":
            result = convert(
                args.value,
                args.from_unit,
                args.to_unit,
            )
            print(format_decimal(result))

    except (ValueError, ZeroDivisionError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
