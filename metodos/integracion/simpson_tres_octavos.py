"""Regla de Simpson 3/8 (simple).

Aproxima la integral ajustando una cúbica por cuatro puntos igualmente
espaciados (h = (b - a)/3):

    ∫_a^b f(x) dx ≈ (3h/8) · (f(a) + 3·f(a+h) + 3·f(a+2h) + f(b))

Error: O((b-a)^5 · f⁗). Exacta para polinomios de hasta grado 3.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import validar_funcion, validar_intervalo


def simpson_tres_octavos(f: Callable[[float], float], a: float, b: float) -> float:
    """Aproxima ∫_a^b f(x) dx con la regla de Simpson 3/8 simple.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable o a >= b.

    Example:
        >>> round(simpson_tres_octavos(lambda x: x**2, 0, 2), 6)
        2.666667
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    h = (b - a) / 3
    return 3 * h / 8 * (f(a) + 3 * f(a + h) + 3 * f(a + 2 * h) + f(b))


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.simpson_tres_octavos import simpson_tres_octavos
#
# # ∫_0^2 x^2 dx = 8/3 ≈ 2.6667
# simpson_tres_octavos(lambda x: x**2, 0, 2)   # Salida: 2.6666...
