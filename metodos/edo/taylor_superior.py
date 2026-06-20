"""Método de Taylor de orden superior para EDO de primer orden.

Generaliza Euler incluyendo más términos de la serie de Taylor de la
solución. Si se conocen las derivadas totales sucesivas de y respecto de x
(f, f', f'', ...), el avance de orden m es:

    y_{i+1} = y_i + Σ_{k=1}^{m} h^k / k! · f^(k-1)(x_i, y_i)

donde f^(0) = f(x,y), f^(1) = df/dx (derivada total), etc. El error local es
O(h^{m+1}). Las derivadas totales se pasan como lista de funciones para
mantener separada la lógica simbólica del método numérico.
"""

from __future__ import annotations

from collections.abc import Callable
from math import factorial

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_no_vacia,
)


def taylor_superior(
    derivadas: list[Callable[[float, float], float]],
    x0: float,
    y0: float,
    x_final: float,
    n: int = 100,
) -> list[tuple[float, float]]:
    """Resuelve dy/dx = f(x, y) por el método de Taylor de orden m.

    Args:
        derivadas: Lista ``[f, f', f'', ...]`` de derivadas totales de y
            respecto de x, todas con firma ``(x, y) -> float``. El orden del
            método es ``len(derivadas)`` (1 = Euler).
        x0: Valor inicial de x.
        y0: Valor inicial de y, y(x0) = y0.
        x_final: Valor de x hasta donde se propaga la solución (≠ x0).
        n: Número de pasos (n >= 1).

    Returns:
        Lista de tuplas (x_i, y_i); longitud n + 1.

    Raises:
        EntradaInvalidaError: Si `derivadas` está vacía, n <= 0 o
            x_final == x0.

    Example:
        >>> # dy/dx = y -> todas las derivadas totales son y; orden 2
        >>> sol = taylor_superior(
        ...     [lambda x, y: y, lambda x, y: y], 0, 1, 1, n=100
        ... )
        >>> round(sol[-1][1], 3)
        2.718
    """
    validar_no_vacia(derivadas, "derivadas")
    validar_entero_positivo(n, "n")
    if x_final == x0:
        raise EntradaInvalidaError("x_final debe ser distinto de x0.")

    h = (x_final - x0) / n
    orden = len(derivadas)
    x, y = x0, y0
    solucion = [(x, y)]
    for _ in range(n):
        incremento = 0.0
        for k in range(1, orden + 1):
            incremento += (h**k) / factorial(k) * derivadas[k - 1](x, y)
        y = y + incremento
        x = x + h
        solucion.append((x, y))
    return solucion


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.taylor_superior import taylor_superior
#
# # dy/dx = y; f = y, f' = d/dx(y) = y'(x) = y. Orden 2:
# sol = taylor_superior([lambda x, y: y, lambda x, y: y], 0, 1, 1, n=100)
# sol[-1]   # (1.0, ~2.7181) -> aprox. de e
