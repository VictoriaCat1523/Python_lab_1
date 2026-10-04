"""Конвертер единиц измерения."""

from decimal import Decimal, InvalidOperation, getcontext

from .constants import (
    ABSOLUTE_ZERO_C,
    ABSOLUTE_ZERO_ERROR,
    ABSOLUTE_ZERO_F,
    ABSOLUTE_ZERO_K,
    C_TO_F_RATIO,
    CELSIUS_TO_KELVIN,
    DECIMAL_PRECISION,
    F_TO_C_RATIO,
    FAHRENHEIT_OFFSET,
    INCOMPATIBLE_UNITS_ERROR,
    INVALID_NUMBER_ERROR,
    LENGTH_COEFFICIENTS,
    LENGTH_UNITS,
    MASS_COEFFICIENTS,
    MASS_UNITS,
    SUPPORTED_UNITS,
    TEMPERATURE_UNITS,
    UNKNOWN_UNIT_ERROR,
)

getcontext().prec = DECIMAL_PRECISION


def convert_length(
    num: Decimal,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Преобразует значение между единицами длины."""
    return (
        num
        * LENGTH_COEFFICIENTS[from_unit]
        / LENGTH_COEFFICIENTS[to_unit]
    )


def convert_mass(
    num: Decimal,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Преобразует значение между единицами массы."""
    return (
        num
        * MASS_COEFFICIENTS[from_unit]
        / MASS_COEFFICIENTS[to_unit]
    )


def convert_temperature(
    num: Decimal,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Преобразует температуру между поддерживаемыми шкалами."""
    if from_unit == "c":
        if num < ABSOLUTE_ZERO_C:
            raise ValueError(ABSOLUTE_ZERO_ERROR)

        if to_unit == "c":
            return num

        if to_unit == "k":
            return num + CELSIUS_TO_KELVIN

        if to_unit == "f":
            return num * C_TO_F_RATIO + FAHRENHEIT_OFFSET

    if from_unit == "k":
        if num < ABSOLUTE_ZERO_K:
            raise ValueError(ABSOLUTE_ZERO_ERROR)

        if to_unit == "k":
            return num

        if to_unit == "c":
            return num - CELSIUS_TO_KELVIN

        if to_unit == "f":
            return (
                (num - CELSIUS_TO_KELVIN)
                * C_TO_F_RATIO
                + FAHRENHEIT_OFFSET
            )

    if from_unit == "f":
        if num < ABSOLUTE_ZERO_F:
            raise ValueError(ABSOLUTE_ZERO_ERROR)

        if to_unit == "f":
            return num

        if to_unit == "c":
            return (num - FAHRENHEIT_OFFSET) * F_TO_C_RATIO

        if to_unit == "k":
            return (
                (num - FAHRENHEIT_OFFSET)
                * F_TO_C_RATIO
                + CELSIUS_TO_KELVIN
            )

    raise ValueError(INCOMPATIBLE_UNITS_ERROR)


def convert(
    num: str | float | Decimal,
    from_unit: str,
    to_unit: str,
) -> Decimal:
    """Преобразует значение из одной поддерживаемой единицы в другую."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    try:
        value = Decimal(str(num))
    except InvalidOperation as error:
        raise ValueError(INVALID_NUMBER_ERROR) from error

    if not value.is_finite():
        raise ValueError(INVALID_NUMBER_ERROR)

    if from_unit not in SUPPORTED_UNITS or to_unit not in SUPPORTED_UNITS:
        raise ValueError(UNKNOWN_UNIT_ERROR)

    if from_unit in LENGTH_UNITS:
        if to_unit not in LENGTH_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_length(value, from_unit, to_unit)

    if from_unit in MASS_UNITS:
        if to_unit not in MASS_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_mass(value, from_unit, to_unit)

    if from_unit in TEMPERATURE_UNITS:
        if to_unit not in TEMPERATURE_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_temperature(value, from_unit, to_unit)

    raise ValueError(UNKNOWN_UNIT_ERROR)
