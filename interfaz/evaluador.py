"""Evaluador seguro de expresiones para la interfaz.

Convierte el texto que el usuario escribe (p. ej. ``x**2 + sin(x)``) en
funciones de Python invocables. Pertenece a la capa de presentación: su
única responsabilidad es traducir entrada de texto a `Callable`, sin
contener lógica numérica.

Por seguridad, las expresiones se evalúan con los ``__builtins__``
deshabilitados y un espacio de nombres restringido a funciones de `math`.
"""

from __future__ import annotations

import math
from collections.abc import Callable

# Espacio de nombres permitido: funciones y constantes de `math` + utilidades.
_NOMBRES_PERMITIDOS: dict[str, object] = {
    nombre: getattr(math, nombre) for nombre in dir(math) if not nombre.startswith("_")
}
_NOMBRES_PERMITIDOS.update({"abs": abs, "min": min, "max": max, "pow": pow})


class ExpresionInvalidaError(ValueError):
    """Se lanza cuando una expresión no puede compilarse o evaluarse."""


def _compilar(expresion: str) -> object:
    """Compila la expresión, validando que sea sintácticamente correcta."""
    if not isinstance(expresion, str) or not expresion.strip():
        raise ExpresionInvalidaError("La expresión no puede estar vacía.")
    try:
        # Se recorta para evitar errores de "unexpected indent" por espacios.
        return compile(expresion.strip(), "<expresion>", "eval")
    except SyntaxError as exc:
        raise ExpresionInvalidaError(f"Expresión inválida: {exc.msg}.") from exc


def crear_funcion_x(expresion: str) -> Callable[[float], float]:
    """Crea una función de una variable f(x) a partir de texto.

    Args:
        expresion: Cadena con la expresión en términos de ``x``.

    Returns:
        Función ``f(x) -> float``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def f(x: float) -> float:
        return eval(codigo, {"__builtins__": {}}, {**_NOMBRES_PERMITIDOS, "x": x})

    return f


def crear_funcion_xy(expresion: str) -> Callable[[float, float], float]:
    """Crea una función de dos variables f(x, y) a partir de texto.

    Args:
        expresion: Cadena con la expresión en términos de ``x`` e ``y``.

    Returns:
        Función ``f(x, y) -> float``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def f(x: float, y: float) -> float:
        return eval(
            codigo, {"__builtins__": {}}, {**_NOMBRES_PERMITIDOS, "x": x, "y": y}
        )

    return f


def parsear_lista(texto: str) -> list[float]:
    """Convierte ``"1, 2, 3"`` o ``"1 2 3"`` en ``[1.0, 2.0, 3.0]``.

    Raises:
        ExpresionInvalidaError: Si algún elemento no es numérico.
    """
    crudo = texto.replace(",", " ").split()
    if not crudo:
        raise ExpresionInvalidaError("La lista de valores está vacía.")
    try:
        return [float(valor) for valor in crudo]
    except ValueError as exc:
        raise ExpresionInvalidaError(
            "La lista debe contener solo números separados por comas o espacios."
        ) from exc


def parsear_matriz(texto: str) -> list[list[float]]:
    """Convierte filas (una por línea o separadas por ``;``) en una matriz.

    Ejemplo: ``"2 1; 1 3"`` -> ``[[2.0, 1.0], [1.0, 3.0]]``.

    Raises:
        ExpresionInvalidaError: Si hay valores no numéricos o filas vacías.
    """
    filas_texto = [
        fila for fila in texto.replace(";", "\n").splitlines() if fila.strip()
    ]
    if not filas_texto:
        raise ExpresionInvalidaError("La matriz está vacía.")
    return [parsear_lista(fila) for fila in filas_texto]


def parsear_lista_funciones_xy(texto: str) -> list[Callable[[float, float], float]]:
    """Convierte expresiones separadas por ``;`` en funciones f(x, y).

    Útil para el método de Taylor de orden superior, que recibe la lista de
    derivadas totales como funciones.
    """
    partes = [parte for parte in texto.split(";") if parte.strip()]
    if not partes:
        raise ExpresionInvalidaError("Debe ingresar al menos una función.")
    return [crear_funcion_xy(parte) for parte in partes]
