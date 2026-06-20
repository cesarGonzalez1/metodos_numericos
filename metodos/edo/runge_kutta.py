"""Método de Runge-Kutta de cuarto orden (RK4) para EDO de primer orden.

El método clásico RK4 combina cuatro evaluaciones de f por paso para lograr
error local O(h^5) y global O(h^4), sin necesidad de calcular derivadas
adicionales (a diferencia de Taylor):

    k1 = f(x, y)
    k2 = f(x + h/2, y + h/2·k1)
    k3 = f(x + h/2, y + h/2·k2)
    k4 = f(x + h,   y + h·k3)
    y_{i+1} = y_i + h/6·(k1 + 2k2 + 2k3 + k4)
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_entero_positivo, validar_funcion


def runge_kutta(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_final: float,
    n: int = 100,
) -> list[tuple[float, float]]:
    """Resuelve dy/dx = f(x, y) con condición inicial (x0, y0) por RK4.

    Args:
        f: Función f(x, y) que define la EDO.
        x0: Valor inicial de x.
        y0: Valor inicial de y, y(x0) = y0.
        x_final: Valor de x hasta donde se propaga la solución (≠ x0).
        n: Número de pasos (n >= 1).

    Returns:
        Lista de tuplas (x_i, y_i); longitud n + 1.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, n <= 0 o x_final == x0.

    Example:
        >>> # dy/dx = y, y(0)=1 -> y(1) = e
        >>> sol = runge_kutta(lambda x, y: y, 0, 1, 1, n=10)
        >>> round(sol[-1][1], 5)
        2.71828
    """
    validar_funcion(f)
    validar_entero_positivo(n, "n")
    if x_final == x0:
        raise EntradaInvalidaError("x_final debe ser distinto de x0.")

    h = (x_final - x0) / n
    x, y = x0, y0
    solucion = [(x, y)]
    for _ in range(n):
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h / 2 * k1)
        k3 = f(x + h / 2, y + h / 2 * k2)
        k4 = f(x + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + h
        solucion.append((x, y))
    return solucion


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.runge_kutta import runge_kutta
#
# # dy/dx = y, y(0)=1; con solo 10 pasos RK4 ya es muy preciso
# sol = runge_kutta(lambda x, y: y, 0, 1, 1, n=10)
# sol[-1]   # (1.0, ~2.71828)
