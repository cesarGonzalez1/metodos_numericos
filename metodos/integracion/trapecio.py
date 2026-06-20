"""Plantilla: regla del trapecio.

Esqueleto de referencia. Otros métodos (Simpson 1/3, Simpson 3/8,
cuadratura de Gauss, Romberg) van en archivos independientes dentro de
`metodos/integracion/`.
"""

from __future__ import annotations

from collections.abc import Callable


def trapecio(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """Aproxima la integral definida de `f` en [a, b] por la regla del trapecio.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración.
        n: Número de subintervalos (n >= 1).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        ValueError: Si n < 1.

    TODO(equipo): implementar el algoritmo.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
