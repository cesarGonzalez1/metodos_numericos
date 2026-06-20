"""Método de Euler para EDO de primer orden.

Resuelve el problema de valor inicial dy/dx = f(x, y), y(x0) = y0, avanzando
con pasos de tamaño fijo h:

    y_{i+1} = y_i + h · f(x_i, y_i)

Es el método más simple (orden 1, error local O(h^2), global O(h)). Sirve de
base y referencia para los métodos de mayor orden del paquete.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_entero_positivo, validar_funcion


def euler(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_final: float,
    n: int = 100,
) -> list[tuple[float, float]]:
    """Resuelve dy/dx = f(x, y) con condición inicial (x0, y0) por Euler.

    Args:
        f: Función f(x, y) que define la EDO dy/dx = f(x, y).
        x0: Valor inicial de x.
        y0: Valor inicial de y, y(x0) = y0.
        x_final: Valor de x hasta donde se propaga la solución (≠ x0).
        n: Número de pasos (n >= 1).

    Returns:
        Lista de tuplas (x_i, y_i) con la solución aproximada, incluyendo el
        punto inicial. Su longitud es n + 1.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, n <= 0 o x_final == x0.

    Example:
        >>> # dy/dx = y, y(0)=1 -> y(1) ≈ e
        >>> sol = euler(lambda x, y: y, 0, 1, 1, n=1000)
        >>> round(sol[-1][1], 2)
        2.72
    """
    validar_funcion(f)
    validar_entero_positivo(n, "n")
    if x_final == x0:
        raise EntradaInvalidaError("x_final debe ser distinto de x0.")

    h = (x_final - x0) / n
    x, y = x0, y0
    solucion = [(x, y)]
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
        solucion.append((x, y))
    return solucion


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.euler import euler
#
# # dy/dx = y, y(0)=1; solución exacta y=e^x
# sol = euler(lambda x, y: y, 0, 1, 1, n=1000)
# sol[-1]   # (1.0, ~2.7169)  -> aprox. de e ≈ 2.71828
