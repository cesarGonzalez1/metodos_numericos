"""Cuadratura de Gauss-Legendre para integrales triples (U-II 2.4.2).

Aproxima

    ∫_a^b ∫_c^d ∫_e^g f(x, y, z) dz dy dx

mediante el producto tensorial de la cuadratura de Gauss-Legendre en las
tres dimensiones. Con ``p`` puntos por eje usa p³ evaluaciones e integra
exactamente polinomios de grado hasta 2p-1 en cada variable.
"""

from __future__ import annotations

from collections.abc import Callable

from metodos.integracion.cuadratura_gaussiana import NODOS_PESOS
from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_intervalo


def cuadratura_gaussiana_triple(
    f: Callable[[float, float, float], float],
    a: float,
    b: float,
    c: float,
    d: float,
    e: float,
    g: float,
    puntos: int = 3,
) -> dict:
    """Aproxima ∫∫∫ f(x, y, z) dz dy dx con Gauss-Legendre 3D.

    Args:
        f: Función integrando f(x, y, z).
        a: Límite inferior en x.
        b: Límite superior en x (b > a).
        c: Límite inferior en y.
        d: Límite superior en y (d > c).
        e: Límite inferior en z.
        g: Límite superior en z (g > e).
        puntos: Nodos de Gauss por eje (2 a 5).

    Returns:
        Diccionario con:
            - ``integral`` (float): Valor aproximado de la integral triple.
            - ``puntos`` (int): Nodos por eje usados.
            - ``evaluaciones`` (int): Total de evaluaciones de f (puntos³).

    Raises:
        EntradaInvalidaError: Si algún intervalo es inválido o ``puntos`` no
            está entre 2 y 5.

    Example:
        >>> # ∫_0^1 ∫_0^1 ∫_0^1 (x + y + z) dz dy dx = 1.5
        >>> f = lambda x, y, z: x + y + z
        >>> round(cuadratura_gaussiana_triple(f, 0, 1, 0, 1, 0, 1)["integral"], 9)
        1.5
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_intervalo(c, d)
    validar_intervalo(e, g)
    if puntos not in NODOS_PESOS:
        raise EntradaInvalidaError(
            f"'puntos' debe estar entre 2 y 5; se recibió {puntos}."
        )

    nodos, pesos = NODOS_PESOS[puntos]
    mx, ccx = (b - a) / 2.0, (a + b) / 2.0
    my, ccy = (d - c) / 2.0, (c + d) / 2.0
    mz, ccz = (g - e) / 2.0, (e + g) / 2.0

    suma = 0.0
    for ni, wi in zip(nodos, pesos):
        x = mx * ni + ccx
        for nj, wj in zip(nodos, pesos):
            y = my * nj + ccy
            for nk, wk in zip(nodos, pesos):
                z = mz * nk + ccz
                suma += wi * wj * wk * f(x, y, z)

    integral = mx * my * mz * suma
    return {"integral": integral, "puntos": puntos, "evaluaciones": puntos**3}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.cuadratura_gaussiana_triple import (
#     cuadratura_gaussiana_triple,
# )
#
# # ∫_0^1 ∫_0^1 ∫_0^1 x·y·z dz dy dx = 1/8
# f = lambda x, y, z: x * y * z
# cuadratura_gaussiana_triple(f, 0, 1, 0, 1, 0, 1)["integral"]  # 0.125
