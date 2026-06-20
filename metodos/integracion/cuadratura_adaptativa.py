"""Cuadratura adaptativa (Simpson adaptativo).

Refina recursivamente solo donde la función lo necesita: aplica Simpson 1/3
a un intervalo, lo divide a la mitad y compara. Si la diferencia entre la
estimación gruesa y la fina supera la tolerancia, subdivide; si no, acepta
el resultado. Concentra el esfuerzo en las zonas de mayor curvatura.

Complejidad: depende de la función; O(número de subdivisiones).
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
    validar_tolerancia,
)


def _simpson(f: Callable[[float], float], a: float, b: float) -> float:
    """Simpson 1/3 simple sobre [a, b]."""
    medio = (a + b) / 2
    return (b - a) / 6 * (f(a) + 4 * f(medio) + f(b))


def _recursion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float,
    estimacion: float,
    profundidad: int,
    max_profundidad: int,
) -> float:
    """Paso recursivo del Simpson adaptativo sobre [a, b]."""
    medio = (a + b) / 2
    izquierda = _simpson(f, a, medio)
    derecha = _simpson(f, medio, b)
    if (
        profundidad >= max_profundidad
        or abs(izquierda + derecha - estimacion) <= 15 * tolerancia
    ):
        # Corrección de Richardson para Simpson.
        return izquierda + derecha + (izquierda + derecha - estimacion) / 15
    return _recursion(
        f, a, medio, tolerancia / 2, izquierda, profundidad + 1, max_profundidad
    ) + _recursion(
        f, medio, b, tolerancia / 2, derecha, profundidad + 1, max_profundidad
    )


def cuadratura_adaptativa(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-8,
    max_profundidad: int = 50,
) -> float:
    """Aproxima ∫_a^b f(x) dx con cuadratura adaptativa de Simpson.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        tolerancia: Error absoluto deseado (> 0).
        max_profundidad: Límite de recursión para evitar bucles infinitos.

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b, tolerancia <= 0
            o max_profundidad <= 0.

    Example:
        >>> import math
        >>> round(cuadratura_adaptativa(math.sin, 0, math.pi), 8)
        2.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_tolerancia(tolerancia)
    validar_entero_positivo(max_profundidad, "max_profundidad")

    estimacion_inicial = _simpson(f, a, b)
    return _recursion(f, a, b, tolerancia, estimacion_inicial, 0, max_profundidad)


# --- Ejemplos comentados ------------------------------------------------
# import math
# from metodos.integracion.cuadratura_adaptativa import cuadratura_adaptativa
#
# # ∫_0^pi sin(x) dx = 2 (exacto)
# cuadratura_adaptativa(math.sin, 0, math.pi)   # Salida: ~2.0
