"""Regla de Simpson 1/3 compuesta.

Aplica Simpson 1/3 sobre n subintervalos (n par), agrupándolos de dos en
dos:

    ∫_a^b f(x) dx ≈ h/3·(f(a) + 4·Σ_impares + 2·Σ_pares + f(b)), h=(b-a)/n

Error global: O((b-a)·h^4·f⁗). Complejidad: O(n) evaluaciones de f.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def simpson_un_tercio_compuesto(
    f: Callable[[float], float], a: float, b: float, n: int = 100
) -> float:
    """Aproxima ∫_a^b f(x) dx con Simpson 1/3 compuesto.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        n: Número de subintervalos, debe ser PAR y >= 2.

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b, n <= 0 o n
            es impar.

    Example:
        >>> round(simpson_un_tercio_compuesto(lambda x: x**3, 0, 2, 10), 6)
        4.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(n, "n")
    if n % 2 != 0:
        raise EntradaInvalidaError(
            f"Simpson 1/3 compuesto requiere n par, se recibió: {n}."
        )

    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        coeficiente = 4 if i % 2 == 1 else 2
        total += coeficiente * f(a + i * h)
    return total * h / 3


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.simpson_un_tercio_compuesto import (
#     simpson_un_tercio_compuesto,
# )
#
# # ∫_0^2 x^3 dx = 4 (exacto)
# simpson_un_tercio_compuesto(lambda x: x**3, 0, 2, n=10)   # Salida: 4.0
