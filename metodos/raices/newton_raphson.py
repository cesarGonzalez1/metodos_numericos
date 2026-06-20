"""Método de Newton-Raphson para búsqueda de raíces.

Método abierto que usa la derivada para aproximar la raíz mediante la
recta tangente: x_{n+1} = x_n - f(x_n) / f'(x_n). Converge cuadráticamente
cerca de raíces simples, pero requiere f'(x) y una buena estimación
inicial.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_funcion,
    validar_max_iteraciones,
    validar_tolerancia,
)


def newton_raphson(
    f: Callable[[float], float],
    df: Callable[[float], float],
    x0: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra una raíz de `f` usando Newton-Raphson.

    Args:
        f: Función de la cual se busca la raíz.
        df: Derivada de `f`.
        x0: Aproximación inicial.
        tolerancia: Error absoluto máximo aceptado entre iteraciones.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con las claves ``raiz``, ``iteraciones``, ``convergio``,
        ``error`` e ``historial`` (lista de dicts con ``i``, ``x``,
        ``fx``, ``dfx`` y ``error``).

    Raises:
        EntradaInvalidaError: Si los parámetros no son válidos o si la
            derivada se anula (división por cero) durante la iteración.

    Example:
        >>> resultado = newton_raphson(
        ...     lambda x: x**2 - 2, lambda x: 2 * x, x0=1.5
        ... )
        >>> round(resultado["raiz"], 6)
        1.414214
    """
    validar_funcion(f)
    validar_funcion(df, nombre="df")
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)

    historial: list[dict] = []
    x = x0
    error = float("inf")
    convergio = False

    for i in range(1, max_iteraciones + 1):
        fx = f(x)
        dfx = df(x)
        if dfx == 0:
            raise EntradaInvalidaError(
                f"La derivada se anuló en x = {x}; Newton-Raphson no puede "
                "continuar (división por cero)."
            )
        x_nuevo = x - fx / dfx
        error = abs(x_nuevo - x)
        historial.append({"i": i, "x": x, "fx": fx, "dfx": dfx, "error": error})
        x = x_nuevo

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
# from metodos.raices.newton_raphson import newton_raphson
#
# # Raíz de x^2 - 2  ->  sqrt(2) ~1.414214
# resultado = newton_raphson(lambda x: x**2 - 2, lambda x: 2 * x, x0=1.5)
# resultado["raiz"]
