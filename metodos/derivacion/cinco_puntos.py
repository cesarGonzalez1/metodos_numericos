"""Fórmulas de derivación numérica de 5 puntos.

Aproximan f'(x) usando cinco nodos igualmente espaciados. La fórmula
centrada (punto medio) tiene error O(h^4), la más precisa de las incluidas
en el paquete:

* Punto medio (centrada):
    f'(x) ≈ (f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)) / (12h)
* Hacia adelante:
    f'(x) ≈ (-25f(x) + 48f(x+h) - 36f(x+2h) + 16f(x+3h) - 3f(x+4h)) / (12h)
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_paso

TIPOS_VALIDOS = ("medio", "adelante")


def cinco_puntos(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-2,
    tipo: str = "medio",
) -> float:
    """Aproxima f'(x) con una fórmula de 5 puntos.

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso (> 0).
        tipo: ``"medio"`` (centrada, O(h^4)) o ``"adelante"`` (O(h^4)).

    Returns:
        Aproximación numérica de f'(x).

    Raises:
        EntradaInvalidaError: Si `tipo` no es válido, `f` no es invocable
            o h <= 0.

    Example:
        >>> round(cinco_puntos(lambda x: x**4, 2.0, 1e-2, "medio"), 4)
        32.0
    """
    validar_funcion(f)
    validar_paso(h)
    if tipo not in TIPOS_VALIDOS:
        raise EntradaInvalidaError(
            f"tipo debe ser uno de {TIPOS_VALIDOS}, se recibió: {tipo!r}."
        )

    if tipo == "medio":
        return (f(x - 2 * h) - 8 * f(x - h) + 8 * f(x + h) - f(x + 2 * h)) / (12 * h)
    return (
        -25 * f(x)
        + 48 * f(x + h)
        - 36 * f(x + 2 * h)
        + 16 * f(x + 3 * h)
        - 3 * f(x + 4 * h)
    ) / (12 * h)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.derivacion.cinco_puntos import cinco_puntos
#
# # f(x)=x^4, f'(2)=32
# cinco_puntos(lambda x: x**4, 2.0, h=1e-2, tipo="medio")  # ~32.0
