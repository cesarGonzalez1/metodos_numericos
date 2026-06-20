"""Método de la secante para búsqueda de raíces.

Método abierto que aproxima la derivada de Newton-Raphson mediante una
diferencia finita entre dos puntos, evitando así calcular f'(x):
x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1})).
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_funcion,
    validar_max_iteraciones,
    validar_tolerancia,
)


def secante(
    f: Callable[[float], float],
    x0: float,
    x1: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra una raíz de `f` usando el método de la secante.

    Args:
        f: Función de la cual se busca la raíz.
        x0: Primera aproximación inicial.
        x1: Segunda aproximación inicial (distinta de x0).
        tolerancia: Error absoluto máximo aceptado entre iteraciones.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con las claves ``raiz``, ``iteraciones``, ``convergio``,
        ``error`` e ``historial`` (lista de dicts con ``i``, ``x0``,
        ``x1``, ``x2`` y ``error``).

    Raises:
        EntradaInvalidaError: Si los parámetros no son válidos, si x0 == x1
            o si f(x1) - f(x0) se anula durante la iteración.

    Example:
        >>> resultado = secante(lambda x: x**2 - 2, x0=1, x1=2)
        >>> round(resultado["raiz"], 6)
        1.414214
    """
    validar_funcion(f)
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)
    if x0 == x1:
        raise EntradaInvalidaError(
            f"Las aproximaciones iniciales deben ser distintas: x0=x1={x0}."
        )

    historial: list[dict] = []
    error = abs(x1 - x0)
    convergio = False
    x2 = x1

    for i in range(1, max_iteraciones + 1):
        fx0 = f(x0)
        fx1 = f(x1)
        if fx1 - fx0 == 0:
            raise EntradaInvalidaError(
                f"f(x1) - f(x0) se anuló en la iteración {i}; la secante es "
                "horizontal y el método no puede continuar."
            )
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x2 - x1)
        historial.append({"i": i, "x0": x0, "x1": x1, "x2": x2, "error": error})

        if error < tolerancia:
            convergio = True
            break

        x0, x1 = x1, x2

    return {
        "raiz": x2,
        "iteraciones": len(historial),
        "convergio": convergio,
        "error": error,
        "historial": historial,
    }


# --- Ejemplos de uso (comentados) ---------------------------------------
# from metodos.raices.secante import secante
#
# # Raíz de x^2 - 2  ->  sqrt(2) ~1.414214
# resultado = secante(lambda x: x**2 - 2, x0=1, x1=2)
# resultado["raiz"]
