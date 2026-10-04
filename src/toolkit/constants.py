from decimal import Decimal

DECIMAL_PRECISION = 50

LENGTH_UNITS = ("km", "m", "cm", "mm")
MASS_UNITS = ("kg", "g")
TEMPERATURE_UNITS = ("c", "f", "k")

SUPPORTED_UNITS = (
    LENGTH_UNITS
    + MASS_UNITS
    + TEMPERATURE_UNITS
)

LENGTH_COEFFICIENTS = {
    "km": Decimal("1000"),
    "m": Decimal("1"),
    "cm": Decimal("0.01"),
    "mm": Decimal("0.001"),
}

MASS_COEFFICIENTS = {
    "kg": Decimal("1000"),
    "g": Decimal("1"),
}


ABSOLUTE_ZERO_C = Decimal("-273.15")
ABSOLUTE_ZERO_K = Decimal("0")
ABSOLUTE_ZERO_F = Decimal("-459.67")

CELSIUS_TO_KELVIN = Decimal("273.15")
FAHRENHEIT_OFFSET = Decimal("32")

C_TO_F_RATIO = Decimal("9") / Decimal("5")
F_TO_C_RATIO = Decimal("5") / Decimal("9")

UNKNOWN_UNIT_ERROR = "Неизвестная единица измерения"
INCOMPATIBLE_UNITS_ERROR = "Несовместимые единицы измерения"
ABSOLUTE_ZERO_ERROR = "Температура ниже абсолютного нуля"
INVALID_NUMBER_ERROR = "Некорректное число"