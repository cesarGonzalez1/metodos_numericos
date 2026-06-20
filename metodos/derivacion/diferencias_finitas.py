"""Plantilla: derivación numérica por diferencias finitas centradas.

Esqueleto de referencia. Variantes (diferencias hacia adelante, hacia
atrás, Richardson, derivadas de orden superior) van en archivos
independientes dentro de `metodos/derivacion/`.
"""

from __future__ import annotations

from collections.abc import Callable


def diferencia_centrada(
    f: Callable[[float], float], x: float, h: float = 1e-5
) -> float:
    """Aproxima f'(x) usando la fórmula de diferencias centradas.

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso usado en la aproximación.

    Returns:
        Aproximación numérica de f'(x).

    TODO(equipo): implementar el algoritmo.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
