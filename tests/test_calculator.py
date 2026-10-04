from decimal import Decimal

import pytest

from toolkit.calculator import calculator


def test_operations():
    assert calculator("2 + 3") == Decimal(5)
    assert calculator("10 - 4") == Decimal(6)
    assert calculator("3 * 4") == Decimal(12)
    assert calculator("10 / 4") == Decimal("2.5")
    assert calculator("7 // 3") == Decimal(2)
    assert calculator("7 % 3") == Decimal(1)

def test_operator_priority():
    assert calculator("2 + 3 * 4") == Decimal(14)
    assert calculator("10 - 2 * 3") == Decimal(4)
    assert calculator("2 + 3 * 4 - 6 / 2") == Decimal(11)


def test_parentheses():
    assert calculator("(2 + 3) * 4") == Decimal(20)
    assert calculator("2 * (3 + 4)") == Decimal(14)
    assert calculator("2 * (3 + (4 * 5))") == Decimal(46)
    assert calculator("(((2 + 3)))") == Decimal(5)


def test_unary_operators():
    assert calculator("-5") == Decimal(-5)
    assert calculator("+5") == Decimal(5)
    assert calculator("2 * -3") == Decimal(-6)
    assert calculator("2 - -3") == Decimal(5)
    assert calculator("--5") == Decimal(5)
    assert calculator("-(2 + 3)") == Decimal(-5)


def test_power():
    assert calculator("2 ** 3") == Decimal(8)
    assert calculator("2 * 3 ** 2") == Decimal(18)
    assert calculator("2 ** 3 ** 2") == Decimal(512)
    assert calculator("2 ** -2") == Decimal("0.25")
    assert calculator("-2 ** 2") == Decimal(-4)
    assert calculator("(-2) ** 2") == Decimal(4)


def test_decimal_numbers():
    assert calculator("0.1 + 0.2") == Decimal("0.3")
    assert calculator("1.5 * 2") == Decimal("3.0")
    assert calculator("2.5 + 1.25") == Decimal("3.75")


def test_negative_floor_division_and_modulo():
    assert calculator("-7 // 3") == Decimal(-3)
    assert calculator("-7 % 3") == Decimal(2)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculator("10 / 0")

    with pytest.raises(ZeroDivisionError):
        calculator("10 // 0")

    with pytest.raises(ZeroDivisionError):
        calculator("10 % 0")

    with pytest.raises(ZeroDivisionError):
        calculator("10 / (5 - 5)")


def test_invalid_parentheses():
    with pytest.raises(ValueError):
        calculator("(2 + 3")

    with pytest.raises(ValueError):
        calculator("2 + 3)")

    with pytest.raises(ValueError):
        calculator("()")

    with pytest.raises(ValueError):
        calculator(")(")


def test_invalid_expressions():
    with pytest.raises(ValueError):
        calculator("")

    with pytest.raises(ValueError):
        calculator("   ")

    with pytest.raises(ValueError):
        calculator("2 +")

    with pytest.raises(ValueError):
        calculator("* 2")

    with pytest.raises(ValueError):
        calculator("2 3")

    with pytest.raises(ValueError):
        calculator("2(3 + 4)")

    with pytest.raises(ValueError):
        calculator("(2 + 3)4")

    with pytest.raises(ValueError):
        calculator("(2)(3)")

    with pytest.raises(ValueError):
        calculator("2 * / 3")


def test_invalid_numbers():
    with pytest.raises(ValueError):
        calculator(".5 + 1")

    with pytest.raises(ValueError):
        calculator("5. + 1")

    with pytest.raises(ValueError):
        calculator("1.2.3 + 4")

    with pytest.raises(ValueError):
        calculator(".")


def test_unknown_symbols():
    with pytest.raises(ValueError):
        calculator("2 + a")

    with pytest.raises(ValueError):
        calculator("2 & 3")


def test_spaces():
    assert calculator("  2 + 3 * 4  ") == Decimal(14)
    assert calculator("2+3*4") == Decimal(14)