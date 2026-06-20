"""Excepciones propias del dominio del proyecto.

Usar estas excepciones (en vez de `Exception` genérica) en `metodos/` para
que `interfaz/` pueda capturarlas y mostrar mensajes claros al usuario.
"""

from __future__ import annotations


class MetodosNumericosError(Exception):
    """Excepción base para todos los errores del dominio del proyecto."""


class EntradaInvalidaError(MetodosNumericosError):
    """Se lanza cuando un parámetro de entrada no es válido.

    Ejemplos: intervalo [a, b] inválido, listas de distinto tamaño,
    número de iteraciones <= 0, etc.
    """


class NoConvergeError(MetodosNumericosError):
    """Se lanza cuando un método iterativo no converge en el límite dado."""
