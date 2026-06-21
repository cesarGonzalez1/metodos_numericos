"""Aproximación de Fourier por mínimos cuadrados discretos (Práctica 16).

Construye el polinomio trigonométrico de grado ``n`` que mejor aproxima
(en el sentido de mínimos cuadrados) un conjunto de ``2m`` muestras
igualmente espaciadas de una función sobre un intervalo [a, b]:

    S_n(x) = a_0/2 + a_n·cos(n t) + Σ_{k=1}^{n-1} ( a_k·cos(k t) + b_k·sin(k t) )

donde t ∈ [−π, π] es la variable reescalada y los coeficientes discretos son

    a_k = (1/m) Σ_{j=0}^{2m-1} y_j·cos(k t_j)
    b_k = (1/m) Σ_{j=0}^{2m-1} y_j·sin(k t_j),   t_j = −π + j·(π/m)

(ver Burden & Faires, *Análisis Numérico*, aproximación trigonométrica
discreta). Requiere n < m.
"""

from __future__ import annotations

import math
from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def fourier(
    f: Callable[[float], float],
    a: float,
    b: float,
    m: int = 8,
    n: int = 3,
    x_evaluar: float | None = None,
) -> dict:
    """Aproximación trigonométrica discreta de ``f`` por mínimos cuadrados.

    Args:
        f: Función a aproximar.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo (b > a).
        m: Mitad del número de muestras; se toman ``2m`` puntos. (m >= 1).
        n: Grado del polinomio trigonométrico (1 <= n < m).
        x_evaluar: Punto opcional del intervalo [a, b] donde evaluar S_n.

    Returns:
        Diccionario con:
            - ``a`` (list[float]): Coeficientes a_0, a_1, ..., a_n.
            - ``b`` (list[float]): Coeficientes b_1, ..., b_{n-1}
              (b_0 y b_n son 0 en el esquema discreto y no se incluyen).
            - ``valor`` (float, opcional): S_n(x_evaluar) si se proporcionó.

    Raises:
        EntradaInvalidaError: Si el intervalo es inválido, m o n no son
            enteros positivos, o no se cumple n < m.

    Example:
        >>> import math
        >>> # f(x)=cos(x) en [-π, π] -> a_1 ≈ 1, resto ≈ 0
        >>> r = fourier(math.cos, -math.pi, math.pi, m=8, n=3)
        >>> round(r["a"][1], 4)
        1.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(m, "m")
    validar_entero_positivo(n, "n")
    if n >= m:
        raise EntradaInvalidaError(f"Debe cumplirse n < m; se recibió n={n}, m={m}.")

    num = 2 * m

    def a_x(t: float) -> float:
        """Reescala t ∈ [−π, π] al intervalo original [a, b]."""
        return a + (t + math.pi) * (b - a) / (2.0 * math.pi)

    # Muestras igualmente espaciadas en t y sus imágenes y_j = f(x_j).
    t_muestras = [-math.pi + j * (math.pi / m) for j in range(num)]
    y_muestras = [f(a_x(t)) for t in t_muestras]

    coef_a = []
    for k in range(n + 1):
        suma = sum(y * math.cos(k * t) for y, t in zip(y_muestras, t_muestras))
        coef_a.append(suma / m)
    coef_b = []
    for k in range(1, n):
        suma = sum(y * math.sin(k * t) for y, t in zip(y_muestras, t_muestras))
        coef_b.append(suma / m)

    resultado: dict = {"a": coef_a, "b": coef_b}

    if x_evaluar is not None:
        # t correspondiente a x_evaluar en [a, b].
        t = -math.pi + (x_evaluar - a) * (2.0 * math.pi) / (b - a)
        valor = coef_a[0] / 2.0 + coef_a[n] * math.cos(n * t)
        for k in range(1, n):
            valor += coef_a[k] * math.cos(k * t) + coef_b[k - 1] * math.sin(k * t)
        resultado["valor"] = valor

    return resultado


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.fourier import fourier
# import math
#
# # Aproximar f(x)=x^2 en [-π, π] con grado 4
# fourier(lambda x: x**2, -math.pi, math.pi, m=16, n=4)["a"]
