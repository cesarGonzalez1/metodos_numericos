"""Método de falsa posición (regula falsi) para búsqueda de raíces.

Método cerrado similar a bisección, pero en lugar de tomar el punto medio
toma la intersección con el eje X de la recta que une (a, f(a)) y
(b, f(b)). Suele converger más rápido que bisección.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_cambio_signo,
    validar_funcion,
    validar_intervalo,
    validar_max_iteraciones,
    validar_tolerancia,
)


def falsa_posicion(
    f: Callable[[float], float],
    a: float,
    b: float,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra una raíz de `f` en [a, b] por falsa posición.

    Args:
        f: Función continua de la cual se busca la raíz.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        tolerancia: Error absoluto máximo aceptado entre aproximaciones.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con las claves ``raiz``, ``iteraciones``, ``convergio``,
        ``error`` e ``historial`` (lista de dicts con ``i``, ``a``, ``b``,
        ``c``, ``fc`` y ``error``).

    Raises:
        EntradaInvalidaError: Si los parámetros no son válidos o si f(a) y
            f(b) no tienen signos opuestos.

    Example:
        >>> resultado = falsa_posicion(lambda x: x**3 - x - 2, a=1, b=2)
        >>> round(resultado["raiz"], 4)
        1.5214
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)
    validar_cambio_signo(f, a, b)

    historial: list[dict] = []
    c = a
    c_anterior = a
    error = abs(b - a)
    convergio = False

    for i in range(1, max_iteraciones + 1):
        fa = f(a)
        fb = f(b)
        c = b - fb * (a - b) / (fa - fb)
        fc = f(c)
        error = abs(c - c_anterior) if i > 1 else abs(b - a)
        historial.append({"i": i, "a": a, "b": b, "c": c, "fc": fc, "error": error})

        if fc == 0 or error < tolerancia:
            convergio = True
            break

        if fa * fc < 0:
            b = c
        else:
            a = c
        c_anterior = c

    return {
        "raiz": c,
        "iteraciones": len(historial),
        "convergio": convergio,
        "error": error,
        "historial": historial,
    }


# --- Ejemplos de uso (comentados) ---------------------------------------
# from metodos.raices.falsa_posicion import falsa_posicion
#
# # Raíz de x^3 - x - 2 en [1, 2]  ->  ~1.5214
# resultado = falsa_posicion(lambda x: x**3 - x - 2, a=1, b=2)
# resultado["raiz"]
