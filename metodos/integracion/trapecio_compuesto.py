"""Regla del trapecio compuesta.

Divide [a, b] en n subintervalos iguales y aplica el trapecio en cada uno:

    ∫_a^b f(x) dx ≈ h·(f(a)/2 + Σ_{i=1}^{n-1} f(a+ih) + f(b)/2),  h=(b-a)/n

Error global: O((b-a)·h^2·f''). Complejidad: O(n) evaluaciones de f.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def trapecio_compuesto(
    f: Callable[[float], float], a: float, b: float, n: int = 100
) -> float:
    """Aproxima ∫_a^b f(x) dx con el trapecio compuesto.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        n: Número de subintervalos (>= 1).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b o n <= 0.

    Example:
        >>> round(trapecio_compuesto(lambda x: x**2, 0, 2, 1000), 4)
        2.6667
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(n, "n")

    h = (b - a) / n
    total = (f(a) + f(b)) / 2
    for i in range(1, n):
        total += f(a + i * h)
    return total * h


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.trapecio_compuesto import trapecio_compuesto
#
# # ∫_0^2 x^2 dx = 8/3 ≈ 2.6667
# trapecio_compuesto(lambda x: x**2, 0, 2, n=1000)   # Salida: ~2.6667
