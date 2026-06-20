"""Regla del punto medio (simple).

Aproxima la integral evaluando la función en el punto medio del intervalo:

    ∫_a^b f(x) dx ≈ (b - a) · f((a + b) / 2)

Error: O((b-a)^3 · f''). Es una regla abierta (no evalúa en los extremos).
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import validar_funcion, validar_intervalo


def punto_medio(f: Callable[[float], float], a: float, b: float) -> float:
    """Aproxima ∫_a^b f(x) dx con la regla del punto medio.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable o a >= b.

    Example:
        >>> punto_medio(lambda x: x, 0, 2)
        2.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    return (b - a) * f((a + b) / 2)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.punto_medio import punto_medio
#
# # ∫_0^2 x dx = 2 (exacto, f lineal)
# punto_medio(lambda x: x, 0, 2)   # Salida: 2.0
