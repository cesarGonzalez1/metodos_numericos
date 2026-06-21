"""Trazadores cúbicos (splines) naturales (U-V 5.2.4).

Construye un spline cúbico S(x) que pasa por todos los nodos y es de clase
C² (continuo con primera y segunda derivada continuas). En cada subintervalo
[x_j, x_{j+1}] el spline es un polinomio cúbico

    S_j(x) = a_j + b_j (x − x_j) + c_j (x − x_j)² + d_j (x − x_j)³

Los coeficientes c_j (proporcionales a la segunda derivada) se obtienen de
un sistema tridiagonal. Se usan las condiciones de frontera **naturales**
S''(x_0) = S''(x_n) = 0, resuelto con el algoritmo de Thomas (O(n)).
"""

from __future__ import annotations

import bisect

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def splines_cubicos(
    x_datos: list[float], y_datos: list[float], x_evaluar: float
) -> dict:
    """Construye el spline cúbico natural y lo evalúa en ``x_evaluar``.

    Args:
        x_datos: Nodos x en orden estrictamente creciente (longitud n >= 3).
        y_datos: Valores f(x_i) (longitud n).
        x_evaluar: Punto donde se evalúa el spline (dentro de [x_0, x_n]).

    Returns:
        Diccionario con:
            - ``valor`` (float): S(x_evaluar).
            - ``coeficientes`` (list[list[float]]): Filas [a, b, c, d], una
              por subintervalo j = 0..n-2.

    Raises:
        EntradaInvalidaError: Si hay menos de 3 puntos, las longitudes
            difieren, hay nodos repetidos, los nodos no están ordenados de
            forma creciente o ``x_evaluar`` queda fuera del rango.

    Example:
        >>> # f(x)=x^2 en 0,1,2,3 -> S(1.5) cercano a 2.25
        >>> r = splines_cubicos([0, 1, 2, 3], [0, 1, 4, 9], 1.5)
        >>> round(r["valor"], 4)
        2.25
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_sin_duplicados(x_datos, "x_datos")
    n = len(x_datos)
    if n < 3:
        raise EntradaInvalidaError("El spline cúbico requiere al menos 3 puntos.")
    if any(x_datos[i] >= x_datos[i + 1] for i in range(n - 1)):
        raise EntradaInvalidaError(
            "Los nodos x deben estar en orden estrictamente creciente."
        )
    if not (x_datos[0] <= x_evaluar <= x_datos[-1]):
        raise EntradaInvalidaError(
            f"x_evaluar={x_evaluar} está fuera del rango "
            f"[{x_datos[0]}, {x_datos[-1]}]."
        )

    x = [float(v) for v in x_datos]
    a = [float(v) for v in y_datos]
    h = [x[i + 1] - x[i] for i in range(n - 1)]

    # Lado derecho del sistema tridiagonal para c (segunda derivada/3).
    alpha = [0.0] * n
    for i in range(1, n - 1):
        alpha[i] = 3.0 / h[i] * (a[i + 1] - a[i]) - 3.0 / h[i - 1] * (a[i] - a[i - 1])

    # Algoritmo de Thomas (Burden, frontera natural).
    ell = [1.0] * n
    mu = [0.0] * n
    z = [0.0] * n
    for i in range(1, n - 1):
        ell[i] = 2.0 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / ell[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / ell[i]

    c = [0.0] * n
    b = [0.0] * (n - 1)
    d = [0.0] * (n - 1)
    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (a[j + 1] - a[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    coeficientes = [[a[j], b[j], c[j], d[j]] for j in range(n - 1)]

    # Localiza el subintervalo y evalúa S_j.
    j = bisect.bisect_right(x, x_evaluar) - 1
    j = max(0, min(j, n - 2))
    dx = x_evaluar - x[j]
    valor = a[j] + b[j] * dx + c[j] * dx**2 + d[j] * dx**3

    return {"valor": valor, "coeficientes": coeficientes}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.splines_cubicos import splines_cubicos
#
# splines_cubicos([0, 1, 2, 3], [0, 1, 4, 9], 2.5)["valor"]
