"""Regla de Simpson 1/3 (simple).

Aproxima la integral ajustando una parábola por tres puntos igualmente
espaciados (los extremos y el punto medio):

    ∫_a^b f(x) dx ≈ (b - a)/6 · (f(a) + 4·f((a+b)/2) + f(b))

Error: O((b-a)^5 · f⁗). Es exacta para polinomios de hasta grado 3.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import validar_funcion, validar_intervalo


def simpson_un_tercio(f: Callable[[float], float], a: float, b: float) -> float:
    """Aproxima ∫_a^b f(x) dx con la regla de Simpson 1/3 simple.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable o a >= b.

    Example:
        >>> simpson_un_tercio(lambda x: x**2, 0, 2)
        2.6666666666666665
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    medio = (a + b) / 2
    return (b - a) / 6 * (f(a) + 4 * f(medio) + f(b))


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.simpson_un_tercio import simpson_un_tercio
#
# # ∫_0^2 x^2 dx = 8/3 ≈ 2.6667 (exacto: Simpson integra grado <= 3)
# simpson_un_tercio(lambda x: x**2, 0, 2)   # Salida: 2.6666...
