from decimal import Decimal, InvalidOperation, getcontext

from .constants import (
    DECIMAL_PRECISION,
    SUPPORTED_UNITS,
    LENGTH_UNITS,
    MASS_UNITS,
    TEMPERATURE_UNITS,
    LENGTH_COEFFICIENTS,
    MASS_COEFFICIENTS,
    ABSOLUTE_ZERO_C,
    ABSOLUTE_ZERO_K,
    ABSOLUTE_ZERO_F,
    CELSIUS_TO_KELVIN,
    FAHRENHEIT_OFFSET,
    C_TO_F_RATIO,
    F_TO_C_RATIO,
    UNKNOWN_UNIT_ERROR,
    INCOMPATIBLE_UNITS_ERROR,
    ABSOLUTE_ZERO_ERROR,
    INVALID_NUMBER_ERROR,
)


getcontext().prec = DECIMAL_PRECISION


def convert_length(num, from_unit, to_unit):
    return (
        num
        * LENGTH_COEFFICIENTS[from_unit]
        / LENGTH_COEFFICIENTS[to_unit]
    )


def convert_mass(num, from_unit, to_unit):
    return (
        num
        * MASS_COEFFICIENTS[from_unit]
        / MASS_COEFFICIENTS[to_unit]
    )


def convert_temperature(num, from_unit, to_unit):
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
            return (
                num - FAHRENHEIT_OFFSET
            ) * F_TO_C_RATIO

        if to_unit == "k":
            return (
                (num - FAHRENHEIT_OFFSET)
                * F_TO_C_RATIO
                + CELSIUS_TO_KELVIN
            )


def convert(num, from_unit, to_unit):
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    try:
        num = Decimal(str(num))
    except InvalidOperation:
        raise ValueError(INVALID_NUMBER_ERROR)

    if not num.is_finite():
        raise ValueError(INVALID_NUMBER_ERROR)

    if from_unit not in SUPPORTED_UNITS or to_unit not in SUPPORTED_UNITS:
        raise ValueError(UNKNOWN_UNIT_ERROR)

    if from_unit in LENGTH_UNITS:
        if to_unit not in LENGTH_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_length(num, from_unit, to_unit)

    if from_unit in MASS_UNITS:
        if to_unit not in MASS_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_mass(num, from_unit, to_unit)

    if from_unit in TEMPERATURE_UNITS:
        if to_unit not in TEMPERATURE_UNITS:
            raise ValueError(INCOMPATIBLE_UNITS_ERROR)

        return convert_temperature(num, from_unit, to_unit)


