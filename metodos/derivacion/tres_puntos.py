"""Fórmulas de derivación numérica de 3 puntos.

Aproximan f'(x) usando tres nodos igualmente espaciados. Existen dos
variantes según la posición del punto evaluado:

* Punto medio (centrada): error O(h^2), la más precisa de las tres.
    f'(x) ≈ (f(x + h) - f(x - h)) / (2h)
* Extremo hacia adelante: error O(h^2).
    f'(x) ≈ (-3f(x) + 4f(x + h) - f(x + 2h)) / (2h)
* Extremo hacia atrás: error O(h^2).
    f'(x) ≈ (3f(x) - 4f(x - h) + f(x - 2h)) / (2h)
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_paso

TIPOS_VALIDOS = ("medio", "adelante", "atras")


def tres_puntos(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-4,
    tipo: str = "medio",
) -> float:
    """Aproxima f'(x) con una fórmula de 3 puntos.

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso (> 0).
        tipo: ``"medio"`` (centrada), ``"adelante"`` o ``"atras"``.

    Returns:
        Aproximación numérica de f'(x).

    Raises:
        EntradaInvalidaError: Si `tipo` no es válido, `f` no es invocable
            o h <= 0.

    Example:
        >>> round(tres_puntos(lambda x: x**2, 3.0, 1e-4, "medio"), 4)
        6.0
        >>> round(tres_puntos(lambda x: x**2, 3.0, 1e-4, "adelante"), 4)
        6.0
    """
    validar_funcion(f)
    validar_paso(h)
    if tipo not in TIPOS_VALIDOS:
        raise EntradaInvalidaError(
            f"tipo debe ser uno de {TIPOS_VALIDOS}, se recibió: {tipo!r}."
        )

    if tipo == "medio":
        return (f(x + h) - f(x - h)) / (2 * h)
    if tipo == "adelante":
        return (-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h)
    return (3 * f(x) - 4 * f(x - h) + f(x - 2 * h)) / (2 * h)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.derivacion.tres_puntos import tres_puntos
#
# # f(x)=x^2, f'(3)=6
# tres_puntos(lambda x: x**2, 3.0, h=1e-4, tipo="medio")     # ~6.0
# tres_puntos(lambda x: x**2, 3.0, h=1e-4, tipo="adelante")  # ~6.0
