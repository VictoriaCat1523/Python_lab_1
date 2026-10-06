"""Пользовательские исключения пакета toolkit."""


class ToolkitError(ValueError):
    """Базовая ошибка пакета toolkit."""


class CalculatorError(ToolkitError):
    """Ошибка при разборе или вычислении выражения."""


class ConverterError(ToolkitError):
    """Ошибка при конвертации величин."""