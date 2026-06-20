"""Método de iteración de punto fijo para búsqueda de raíces.

Reescribe la ecuación f(x) = 0 como x = g(x) y genera la sucesión
x_{n+1} = g(x_n). Converge a un punto fijo (raíz de f) cuando |g'(x)| < 1
en un entorno de la raíz.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_funcion,
    validar_max_iteraciones,
    validar_tolerancia,
)


def punto_fijo(
    g: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra un punto fijo de `g` (raíz de f con f(x) = g(x) - x).

    Args:
        g: Función de iteración tal que x = g(x) en la raíz buscada.
        x0: Aproximación inicial.
        tolerancia: Error absoluto máximo aceptado entre iteraciones.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con las claves ``raiz``, ``iteraciones``, ``convergio``,
        ``error`` e ``historial`` (lista de dicts con ``i``, ``x``,
        ``gx`` y ``error``).

    Raises:
        EntradaInvalidaError: Si los parámetros de entrada no son válidos.

    Example:
        >>> import math
        >>> # x = cos(x)  ->  punto fijo ~0.7390851
        >>> resultado = punto_fijo(math.cos, x0=0.5)
        >>> round(resultado["raiz"], 4)
        0.7391
    """
    validar_funcion(g, nombre="g")
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)

    historial: list[dict] = []
    x = x0
    error = float("inf")
    convergio = False

    for i in range(1, max_iteraciones + 1):
        gx = g(x)
        error = abs(gx - x)
        historial.append({"i": i, "x": x, "gx": gx, "error": error})
        x = gx

        if error < tolerancia:
            convergio = True
            break

    return {
        "raiz": x,
        "iteraciones": len(historial),
        "convergio": convergio,
        "error": error,
        "historial": historial,
    }


# --- Ejemplos de uso (comentados) ---------------------------------------
# import math
# from metodos.raices.punto_fijo import punto_fijo
#
# # Resolver x = cos(x)  ->  ~0.739085
# resultado = punto_fijo(math.cos, x0=0.5)
# resultado["raiz"]
