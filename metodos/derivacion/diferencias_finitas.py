"""Derivación numérica general por diferencias finitas.

Módulo base de derivación: aproxima f'(x) mediante diferencias finitas
hacia adelante, hacia atrás o centradas. Las diferencias centradas son de
orden O(h^2); las laterales (adelante/atrás) de orden O(h).

API consistente con el resto del paquete de derivación: todas las
funciones reciben una función `f`, un punto `x` y un paso `h`, y devuelven
un float con la aproximación de la derivada.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_paso

# Tipos de diferencia soportados por `derivada`.
TIPOS_VALIDOS = ("centrada", "adelante", "atras")


def diferencia_centrada(
    f: Callable[[float], float], x: float, h: float = 1e-5
) -> float:
    """Aproxima f'(x) usando la fórmula de diferencias centradas.

    f'(x) ≈ (f(x + h) - f(x - h)) / (2h).   Error: O(h^2).

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso (> 0).

    Returns:
        Aproximación numérica de f'(x).

    Raises:
        EntradaInvalidaError: Si `f` no es invocable o h <= 0.

    Example:
        >>> round(diferencia_centrada(lambda x: x**2, 3.0, 1e-4), 4)
        6.0
    """
    validar_funcion(f)
    validar_paso(h)
    return (f(x + h) - f(x - h)) / (2 * h)


def diferencia_adelante(
    f: Callable[[float], float], x: float, h: float = 1e-5
) -> float:
    """Aproxima f'(x) con diferencias hacia adelante. Error: O(h).

    f'(x) ≈ (f(x + h) - f(x)) / h.
    """
    validar_funcion(f)
    validar_paso(h)
    return (f(x + h) - f(x)) / h


def diferencia_atras(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Aproxima f'(x) con diferencias hacia atrás. Error: O(h).

    f'(x) ≈ (f(x) - f(x - h)) / h.
    """
    validar_funcion(f)
    validar_paso(h)
    return (f(x) - f(x - h)) / h


def derivada(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-5,
    tipo: str = "centrada",
) -> float:
    """Despachador general de derivación por diferencias finitas.

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso (> 0).
        tipo: Una de ``"centrada"``, ``"adelante"`` o ``"atras"``.

    Returns:
        Aproximación numérica de f'(x).

    Raises:
        EntradaInvalidaError: Si `tipo` no es válido, `f` no es invocable
            o h <= 0.

    Example:
        >>> round(derivada(lambda x: x**3, 2.0, 1e-4, "centrada"), 3)
        12.0
    """
    if tipo not in TIPOS_VALIDOS:
        raise EntradaInvalidaError(
            f"tipo debe ser uno de {TIPOS_VALIDOS}, se recibió: {tipo!r}."
        )
    if tipo == "centrada":
        return diferencia_centrada(f, x, h)
    if tipo == "adelante":
        return diferencia_adelante(f, x, h)
    return diferencia_atras(f, x, h)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.derivacion.diferencias_finitas import derivada
#
# # f(x) = x^2, f'(3) = 6
# derivada(lambda x: x**2, 3.0, h=1e-4)                 # ~6.0 (centrada)
# derivada(lambda x: x**2, 3.0, h=1e-4, tipo="adelante")  # ~6.0001
