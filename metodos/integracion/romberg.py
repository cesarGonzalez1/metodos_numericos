"""Integración de Romberg.

Combina la regla del trapecio compuesta con extrapolación de Richardson
para acelerar la convergencia. La primera columna son trapecios con
1, 2, 4, ... subintervalos; cada columna siguiente cancela el siguiente
término del error:

    R[i][j] = (4^j · R[i][j-1] - R[i-1][j-1]) / (4^j - 1)

Complejidad: O(2^niveles) evaluaciones de f.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def romberg(
    f: Callable[[float], float],
    a: float,
    b: float,
    niveles: int = 5,
) -> dict:
    """Aproxima ∫_a^b f(x) dx por el método de Romberg.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        niveles: Número de filas de la tabla (>= 1).

    Returns:
        Diccionario con:
            - ``valor`` (float): Mejor aproximación de la integral.
            - ``tabla`` (list[list[float]]): Tabla triangular de Romberg.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b o niveles <= 0.

    Example:
        >>> r = romberg(lambda x: x**3, 0, 2, niveles=4)
        >>> round(r["valor"], 6)
        4.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(niveles, "niveles")

    tabla = [[0.0] * niveles for _ in range(niveles)]
    h = b - a
    tabla[0][0] = h / 2 * (f(a) + f(b))

    for i in range(1, niveles):
        h /= 2
        # Suma de los nuevos puntos intermedios (trapecio compuesto refinado).
        suma = sum(f(a + (2 * k - 1) * h) for k in range(1, 2 ** (i - 1) + 1))
        tabla[i][0] = tabla[i - 1][0] / 2 + h * suma
        for j in range(1, i + 1):
            potencia = 4**j
            tabla[i][j] = (potencia * tabla[i][j - 1] - tabla[i - 1][j - 1]) / (
                potencia - 1
            )

    return {"valor": tabla[niveles - 1][niveles - 1], "tabla": tabla}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.romberg import romberg
#
# # ∫_0^2 x^3 dx = 4 (exacto)
# r = romberg(lambda x: x**3, 0, 2, niveles=4)
# r["valor"]   # Salida: 4.0
