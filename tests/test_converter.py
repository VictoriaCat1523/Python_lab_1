from decimal import Decimal

import pytest

from toolkit.converter import convert


def test_length():
    assert convert("1", "km", "m") == Decimal(1000)
    assert convert("1000", "m", "km") == Decimal(1)
    assert convert("2", "m", "cm") == Decimal(200)
    assert convert("250", "cm", "m") == Decimal("2.5")
    assert convert("1", "cm", "mm") == Decimal(10)
    assert convert("10", "mm", "cm") == Decimal(1)
    assert convert("1", "km", "mm") == Decimal(1000000)
    assert convert("5", "m", "m") == Decimal(5)


def test_mass():
    assert convert("2", "kg", "g") == Decimal(2000)
    assert convert("1000", "g", "kg") == Decimal(1)
    assert convert("5", "kg", "kg") == Decimal(5)


def test_temperature():
    assert convert("0", "c", "k") == Decimal("273.15")
    assert convert("273.15", "k", "c") == Decimal(0)
    assert convert("100", "c", "f") == Decimal(212)
    assert convert("32", "f", "c") == Decimal(0)
    assert convert("273.15", "k", "f") == Decimal(32)
    assert convert("32", "f", "k") == Decimal("273.15")
    assert convert("20", "c", "c") == Decimal(20)
    assert convert("20", "k", "k") == Decimal(20)
    assert convert("20", "f", "f") == Decimal(20)


def test_negative_temperature():
    assert convert("-20", "c", "f") == Decimal(-4)
    assert convert("-40", "f", "c") == Decimal(-40)
    assert convert("-100", "c", "k") == Decimal("173.15")


def test_absolute_zero():
    assert convert("-273.15", "c", "k") == Decimal(0)
    assert convert("0", "k", "c") == Decimal("-273.15")

    result = convert("-459.67", "f", "c")

    assert result == pytest.approx(
        Decimal("-273.15"),
        abs=Decimal("0.0000001"),
    )


def test_below_absolute_zero():
    with pytest.raises(ValueError):
        convert("-274", "c", "k")

    with pytest.raises(ValueError):
        convert("-1", "k", "c")

    with pytest.raises(ValueError):
        convert("-500", "f", "c")


def test_incompatible_units():
    with pytest.raises(ValueError):
        convert("1", "kg", "m")

    with pytest.raises(ValueError):
        convert("1", "m", "kg")

    with pytest.raises(ValueError):
        convert("1", "m", "c")

    with pytest.raises(ValueError):
        convert("20", "c", "m")

    with pytest.raises(ValueError):
        convert("20", "c", "kg")


def test_unknown_units():
    with pytest.raises(ValueError):
        convert("1", "meter", "m")

    with pytest.raises(ValueError):
        convert("1", "m", "meter")

    with pytest.raises(ValueError):
        convert("1", "abc", "xyz")


def test_unit_case():
    assert convert("1", "KM", "M") == Decimal(1000)
    assert convert("1", "Kg", "G") == Decimal(1000)


def test_number_values():
    assert convert("1.25", "kg", "g") == Decimal(1250)
    assert convert("0.001", "m", "mm") == Decimal(1)
    assert convert("0", "km", "m") == Decimal(0)

def test_negative_length():
    with pytest.raises(
        ValueError,
        match="Длина не может быть отрицательной",
    ):
        convert("-2", "m", "cm")


def test_negative_mass():
    with pytest.raises(
        ValueError,
        match="Масса не может быть отрицательной",
    ):
        convert("-2", "kg", "g")

def test_invalid_number():
    with pytest.raises(ValueError):
        convert("abc", "kg", "g")