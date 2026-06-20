"""Fórmulas de derivación numérica de 4 puntos.

Aproximan f'(x) usando cuatro nodos igualmente espaciados. Tienen error
O(h^3), superior a las fórmulas de 3 puntos:

* Hacia adelante:
    f'(x) ≈ (-11f(x) + 18f(x+h) - 9f(x+2h) + 2f(x+3h)) / (6h)
* Hacia atrás:
    f'(x) ≈ (11f(x) - 18f(x-h) + 9f(x-2h) - 2f(x-3h)) / (6h)
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_paso

TIPOS_VALIDOS = ("adelante", "atras")


def cuatro_puntos(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-3,
    tipo: str = "adelante",
) -> float:
    """Aproxima f'(x) con una fórmula de 4 puntos (error O(h^3)).

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso (> 0).
        tipo: ``"adelante"`` o ``"atras"``.

    Returns:
        Aproximación numérica de f'(x).

    Raises:
        EntradaInvalidaError: Si `tipo` no es válido, `f` no es invocable
            o h <= 0.

    Example:
        >>> round(cuatro_puntos(lambda x: x**3, 2.0, 1e-3, "adelante"), 3)
        12.0
    """
    validar_funcion(f)
    validar_paso(h)
    if tipo not in TIPOS_VALIDOS:
        raise EntradaInvalidaError(
            f"tipo debe ser uno de {TIPOS_VALIDOS}, se recibió: {tipo!r}."
        )

    if tipo == "adelante":
        return (-11 * f(x) + 18 * f(x + h) - 9 * f(x + 2 * h) + 2 * f(x + 3 * h)) / (
            6 * h
        )
    return (11 * f(x) - 18 * f(x - h) + 9 * f(x - 2 * h) - 2 * f(x - 3 * h)) / (6 * h)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.derivacion.cuatro_puntos import cuatro_puntos
#
# # f(x)=x^3, f'(2)=12
# cuatro_puntos(lambda x: x**3, 2.0, h=1e-3, tipo="adelante")  # ~12.0
