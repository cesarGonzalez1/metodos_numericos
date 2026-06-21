"""Cuadratura de Gauss-Legendre para integrales dobles (U-II 2.4.2).

Aproxima

    ∫_a^b ∫_c^d f(x, y) dy dx

mediante el producto tensorial de la cuadratura de Gauss-Legendre en cada
dimensión. Con ``p`` puntos por eje, integra exactamente polinomios de
grado hasta 2p-1 en cada variable, por lo que es muy precisa para
integrandos suaves con muy pocas evaluaciones.

    ∫∫ f ≈ (b-a)/2 · (d-c)/2 · Σ_i Σ_j w_i·w_j·f(X(ξ_i), Y(η_j))

donde X y Y mapean los nodos de [-1, 1] a [a, b] y [c, d].
"""

from __future__ import annotations

from collections.abc import Callable

from metodos.integracion.cuadratura_gaussiana import NODOS_PESOS
from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_intervalo


def cuadratura_gaussiana_doble(
    f: Callable[[float, float], float],
    a: float,
    b: float,
    c: float,
    d: float,
    puntos: int = 3,
) -> dict:
    """Aproxima ∫_a^b ∫_c^d f(x, y) dy dx con Gauss-Legendre 2D.

    Args:
        f: Función integrando f(x, y).
        a: Límite inferior en x.
        b: Límite superior en x (b > a).
        c: Límite inferior en y.
        d: Límite superior en y (d > c).
        puntos: Nodos de Gauss por eje (2 a 5).

    Returns:
        Diccionario con:
            - ``integral`` (float): Valor aproximado de la integral doble.
            - ``puntos`` (int): Nodos por eje usados.
            - ``evaluaciones`` (int): Total de evaluaciones de f (puntos²).

    Raises:
        EntradaInvalidaError: Si los intervalos son inválidos o ``puntos``
            no está entre 2 y 5.

    Example:
        >>> # ∫_0^1 ∫_0^1 (x^2 + y^2) dy dx = 2/3
        >>> r = cuadratura_gaussiana_doble(lambda x, y: x**2 + y**2, 0, 1, 0, 1)
        >>> round(r["integral"], 10)
        0.6666666667
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_intervalo(c, d)
    if puntos not in NODOS_PESOS:
        raise EntradaInvalidaError(
            f"'puntos' debe estar entre 2 y 5; se recibió {puntos}."
        )

    nodos, pesos = NODOS_PESOS[puntos]
    mx, cx = (b - a) / 2.0, (a + b) / 2.0
    my, cy = (d - c) / 2.0, (c + d) / 2.0

    suma = 0.0
    for ni, wi in zip(nodos, pesos):
        x = mx * ni + cx
        for nj, wj in zip(nodos, pesos):
            y = my * nj + cy
            suma += wi * wj * f(x, y)

    integral = mx * my * suma
    return {"integral": integral, "puntos": puntos, "evaluaciones": puntos**2}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.cuadratura_gaussiana_doble import (
#     cuadratura_gaussiana_doble,
# )
#
# # ∫_0^2 ∫_0^3 x·y dy dx = 9.0
# cuadratura_gaussiana_doble(lambda x, y: x * y, 0, 2, 0, 3)["integral"]  # 9.0
