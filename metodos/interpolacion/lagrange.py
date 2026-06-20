"""Plantilla: interpolación de Lagrange.

Esqueleto de referencia. Otros métodos (Newton en diferencias divididas,
splines cúbicos, etc.) van en archivos independientes dentro de
`metodos/interpolacion/`.
"""

from __future__ import annotations


def lagrange(x_datos: list[float], y_datos: list[float], x_evaluar: float) -> float:
    """Evalúa el polinomio interpolante de Lagrange en `x_evaluar`.

    Args:
        x_datos: Coordenadas x conocidas (nodos), sin valores repetidos.
        y_datos: Coordenadas y conocidas, mismo largo que `x_datos`.
        x_evaluar: Punto donde se desea evaluar el polinomio interpolante.

    Returns:
        Valor aproximado de la función en `x_evaluar`.

    Raises:
        ValueError: Si `x_datos` y `y_datos` no tienen la misma longitud,
            o si `x_datos` contiene valores repetidos.

    TODO(equipo): implementar el algoritmo.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
