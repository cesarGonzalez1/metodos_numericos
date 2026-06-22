"""Mínimos cuadrados con funciones base arbitrarias (modelo lineal general).

Generaliza la regresión lineal: en lugar de ajustar solo una recta, ajusta
cualquier combinación lineal de funciones que el usuario proponga

    y(x) = c_1·g_1(x) + c_2·g_2(x) + ... + c_m·g_m(x)

donde cada ``g_j`` es una función de ``x`` (puede ser no lineal: ``sin(x)``,
``exp(x)``, ``x**2``, ``1``, ...). El modelo es lineal *en los coeficientes*,
así que se resuelven las ecuaciones normales AᵀA·c = Aᵀy, con A la matriz de
diseño cuyo elemento ``A[i][j] = g_j(x_i)`` (cada función evaluada en cada x).

Casos particulares:
* ``[1, x]``            -> recta (mínimos cuadrados lineal ordinario).
* ``[1, x, x**2, ...]`` -> aproximación polinómica.
* ``[1, sin(x), cos(x)]`` -> ajuste trigonométrico, etc.

Complejidad: O(n·m² + m³).
"""

from __future__ import annotations

from collections.abc import Callable

from metodos.matrices.inversa import inversa
from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_misma_longitud, validar_no_vacia


def _transpuesta(m: list[list[float]]) -> list[list[float]]:
    """Transpone una matriz rectangular."""
    return [list(col) for col in zip(*m)]


def _producto(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Producto matricial A·B."""
    bt = _transpuesta(b)
    return [[sum(x * y for x, y in zip(fila, col)) for col in bt] for fila in a]


def _matvec(a: list[list[float]], v: list[float]) -> list[float]:
    """Producto matriz-vector A·v."""
    return [sum(x * y for x, y in zip(fila, v)) for fila in a]


def minimos_cuadrados_general(
    funciones: list[Callable[[float], float]],
    x_datos: list[float],
    y_datos: list[float],
) -> dict:
    """Ajusta y = c1·g1(x) + ... + cm·gm(x) por mínimos cuadrados.

    Args:
        funciones: Lista de funciones base ``g_j(x)``. Cada una se evalúa en
            todos los ``x_datos`` para formar la matriz de diseño.
        x_datos: Coordenadas x observadas.
        y_datos: Coordenadas y observadas, misma longitud que ``x_datos``.

    Returns:
        Diccionario con:
            - ``coeficientes`` (list[float]): ``[c1, c2, ..., cm]``, uno por
              función base, en el mismo orden en que se entregaron.
            - ``r2`` (float): Coeficiente de determinación R².
            - ``predichos`` (list[float]): Valores ajustados ŷ_i.

    Raises:
        EntradaInvalidaError: Si no hay funciones, las listas están vacías o
            difieren en longitud, hay menos puntos que funciones, alguna
            función falla al evaluarse, o el sistema normal es singular
            (funciones base linealmente dependientes sobre los datos).

    Example:
        >>> import math
        >>> # Ajuste de y = 2 + 3·sin(x) con funciones base [1, sin(x)]
        >>> xs = [0.0, 1.0, 2.0, 3.0, 4.0]
        >>> ys = [2 + 3 * math.sin(x) for x in xs]
        >>> base = [lambda x: 1.0, math.sin]
        >>> r = minimos_cuadrados_general(base, xs, ys)
        >>> [round(c, 4) for c in r["coeficientes"]]
        [2.0, 3.0]
    """
    validar_no_vacia(funciones, "funciones")
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    n = len(x_datos)
    m = len(funciones)
    if n < m:
        raise EntradaInvalidaError(
            f"Se requieren al menos {m} puntos para ajustar {m} funciones "
            f"base; se recibieron {n}."
        )

    # Matriz de diseño A: cada función base evaluada en cada x.
    A: list[list[float]] = []
    for i, xi in enumerate(x_datos):
        fila = []
        for j, g in enumerate(funciones):
            try:
                fila.append(float(g(xi)))
            except (ValueError, ZeroDivisionError, OverflowError, TypeError) as exc:
                raise EntradaInvalidaError(
                    f"La función base #{j + 1} no se pudo evaluar en x = {xi}: {exc}."
                ) from exc
        A.append(fila)
    y = [float(v) for v in y_datos]

    At = _transpuesta(A)
    AtA = _producto(At, A)
    Aty = _matvec(At, y)

    try:
        inv = inversa(AtA)["inversa"]
    except EntradaInvalidaError as exc:
        raise EntradaInvalidaError(
            "El sistema de ecuaciones normales es singular: las funciones "
            "base son linealmente dependientes sobre los datos dados."
        ) from exc

    coeficientes = _matvec(inv, Aty)

    predichos = [sum(coeficientes[j] * A[i][j] for j in range(m)) for i in range(n)]
    media_y = sum(y) / n
    ss_total = sum((yi - media_y) ** 2 for yi in y)
    ss_residual = sum((yi - pi) ** 2 for yi, pi in zip(y, predichos))
    r2 = 1.0 if ss_total == 0 else 1 - ss_residual / ss_total

    return {"coeficientes": coeficientes, "r2": r2, "predichos": predichos}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.minimos_cuadrados_general import (
#     minimos_cuadrados_general,
# )
# import math
#
# # Ajuste y = c0 + c1·x + c2·x^2 con base [1, x, x^2]
# base = [lambda x: 1.0, lambda x: x, lambda x: x**2]
# minimos_cuadrados_general(base, [0, 1, 2, 3], [1, 2, 5, 10])["coeficientes"]
