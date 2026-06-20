"""Plantilla: método de Euler para EDO de primer orden.

Esqueleto de referencia. Variantes (Euler mejorado/Heun, Runge-Kutta 4,
etc.) van en archivos independientes dentro de `metodos/edo/`.
"""

from __future__ import annotations

from collections.abc import Callable


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
        x_final: Valor de x hasta donde se desea propagar la solución.
        n: Número de pasos (n >= 1).

    Returns:
        Lista de tuplas (x_i, y_i) con la solución aproximada en cada paso.

    Raises:
        ValueError: Si n < 1 o x_final == x0.

    TODO(equipo): implementar el algoritmo.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
