"""Regla de Simpson 3/8 compuesta.

Aplica Simpson 3/8 sobre n subintervalos (n múltiplo de 3), agrupándolos de
tres en tres:

    ∫_a^b f(x) dx ≈ 3h/8·(f(a) + 3·Σ_{i no mult. de 3} + 2·Σ_{mult. de 3}
                          + f(b)),   h=(b-a)/n

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


def simpson_tres_octavos_compuesto(
    f: Callable[[float], float], a: float, b: float, n: int = 99
) -> float:
    """Aproxima ∫_a^b f(x) dx con Simpson 3/8 compuesto.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        n: Número de subintervalos, debe ser MÚLTIPLO DE 3 y >= 3.

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b, n <= 0 o n
            no es múltiplo de 3.

    Example:
        >>> round(simpson_tres_octavos_compuesto(lambda x: x**3, 0, 2, 9), 6)
        4.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(n, "n")
    if n % 3 != 0:
        raise EntradaInvalidaError(
            f"Simpson 3/8 compuesto requiere n múltiplo de 3, se recibió: {n}."
        )

    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n):
        coeficiente = 2 if i % 3 == 0 else 3
        total += coeficiente * f(a + i * h)
    return total * 3 * h / 8


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.simpson_tres_octavos_compuesto import (
#     simpson_tres_octavos_compuesto,
# )
#
# # ∫_0^2 x^3 dx = 4 (exacto)
# simpson_tres_octavos_compuesto(lambda x: x**3, 0, 2, n=9)   # Salida: 4.0
