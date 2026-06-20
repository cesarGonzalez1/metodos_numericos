"""Plantilla: método de bisección.

Esqueleto de referencia para los métodos de búsqueda de raíces. Cada
método (Newton-Raphson, secante, punto fijo, regla falsa, ...) va en su
propio archivo dentro de `metodos/raices/`.
"""

from __future__ import annotations

from collections.abc import Callable


def biseccion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra una raíz de `f` en el intervalo [a, b] por bisección.

    Args:
        f: Función continua de la cual se busca la raíz.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        tolerancia: Error absoluto máximo aceptado.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con, al menos, las claves: `raiz`, `iteraciones`,
        `convergio`. El detalle final queda a criterio de quien lo
        implemente, pero debe documentarse en el docstring.

    Raises:
        ValueError: Si f(a) y f(b) no tienen signos opuestos.

    TODO(equipo): implementar el algoritmo y sus pruebas en
    `tests/test_biseccion.py`.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
