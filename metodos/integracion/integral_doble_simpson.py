"""Integral doble por la regla compuesta de Simpson 1/3 (U-II 2.4.1).

Aproxima

    ∫_a^b ∫_c^d f(x, y) dy dx

sobre un rectángulo [a, b] × [c, d] aplicando la regla compuesta de
Simpson 1/3 en cada dirección. El error global es O(h^4 + k^4), donde
``h`` y ``k`` son los pasos en x e y respectivamente.

La fórmula bidimensional resulta del producto tensorial de los pesos de
Simpson en cada eje:

    ∫∫ f ≈ (h·k/9) · Σ_i Σ_j w_i · w_j · f(x_i, y_j)

con pesos w = [1, 4, 2, 4, ..., 4, 1] y número de subintervalos par en
ambas direcciones.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def _pesos_simpson(n: int) -> list[float]:
    """Devuelve los pesos compuestos de Simpson 1/3 para ``n`` subintervalos.

    Los pesos son [1, 4, 2, 4, ..., 4, 1]; ``n`` debe ser par.
    """
    pesos = [1.0] * (n + 1)
    for i in range(1, n):
        pesos[i] = 4.0 if i % 2 == 1 else 2.0
    return pesos


def integral_doble_simpson(
    f: Callable[[float, float], float],
    a: float,
    b: float,
    c: float,
    d: float,
    n: int = 4,
    m: int = 4,
) -> dict:
    """Aproxima ∫_a^b ∫_c^d f(x, y) dy dx con Simpson 1/3 compuesto en 2D.

    Args:
        f: Función integrando f(x, y).
        a: Límite inferior en x.
        b: Límite superior en x (b > a).
        c: Límite inferior en y.
        d: Límite superior en y (d > c).
        n: Subintervalos en x (par, >= 2).
        m: Subintervalos en y (par, >= 2).

    Returns:
        Diccionario con:
            - ``integral`` (float): Valor aproximado de la integral doble.
            - ``n`` (int), ``m`` (int): Subintervalos usados en cada eje.
            - ``hx`` (float), ``hy`` (float): Pasos en x e y.

    Raises:
        EntradaInvalidaError: Si los intervalos son inválidos o ``n``/``m``
            no son enteros pares positivos.

    Example:
        >>> # ∫_0^1 ∫_0^1 (x + y) dy dx = 1
        >>> r = integral_doble_simpson(lambda x, y: x + y, 0, 1, 0, 1)
        >>> round(r["integral"], 10)
        1.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_intervalo(c, d)
    validar_entero_positivo(n, "n")
    validar_entero_positivo(m, "m")
    if n % 2 != 0 or m % 2 != 0:
        raise EntradaInvalidaError(
            "Simpson 1/3 requiere un número par de subintervalos en cada eje."
        )

    hx = (b - a) / n
    hy = (d - c) / m
    wx = _pesos_simpson(n)
    wy = _pesos_simpson(m)

    suma = 0.0
    for i in range(n + 1):
        x = a + i * hx
        for j in range(m + 1):
            y = c + j * hy
            suma += wx[i] * wy[j] * f(x, y)

    integral = (hx * hy / 9.0) * suma
    return {"integral": integral, "n": n, "m": m, "hx": hx, "hy": hy}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.integral_doble_simpson import integral_doble_simpson
#
# # ∫_0^2 ∫_0^1 x·y dy dx = 1.0
# integral_doble_simpson(lambda x, y: x * y, 0, 2, 0, 1)["integral"]  # ~1.0
