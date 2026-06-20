"""Interpolación básica (lineal por tramos).

Dada una tabla de puntos (x_i, y_i), estima el valor de la función en un
punto intermedio uniendo con una recta los dos nodos que lo encierran. Es
la forma más simple de interpolación y sirve como referencia/base para los
métodos polinómicos de orden superior.

Complejidad: O(n) por evaluación (búsqueda lineal del intervalo).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def interpolacion_basica(
    x_datos: list[float], y_datos: list[float], x_evaluar: float
) -> float:
    """Interpola linealmente `y` en `x_evaluar` a partir de una tabla.

    Los nodos no necesitan estar ordenados; la función los ordena
    internamente por `x`. Si `x_evaluar` queda fuera del rango de los
    nodos se realiza extrapolación lineal con el tramo extremo más cercano.

    Args:
        x_datos: Coordenadas x conocidas (sin repetidos).
        y_datos: Coordenadas y conocidas, misma longitud que `x_datos`.
        x_evaluar: Punto donde se desea estimar el valor.

    Returns:
        Valor interpolado (float).

    Raises:
        EntradaInvalidaError: Si las listas están vacías, tienen distinta
            longitud, hay menos de 2 nodos o `x_datos` tiene repetidos.

    Example:
        >>> interpolacion_basica([0, 1, 2], [0, 10, 20], 0.5)
        5.0
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_sin_duplicados(list(x_datos), "x_datos")
    if len(x_datos) < 2:
        raise EntradaInvalidaError("Se requieren al menos 2 puntos para interpolar.")

    puntos = sorted(zip(x_datos, y_datos), key=lambda p: p[0])

    # Selección del tramo [x0, x1] que contiene (o más se acerca a) x_evaluar.
    indice = 0
    for i in range(len(puntos) - 1):
        if puntos[i][0] <= x_evaluar <= puntos[i + 1][0]:
            indice = i
            break
    else:
        indice = 0 if x_evaluar < puntos[0][0] else len(puntos) - 2

    x0, y0 = puntos[indice]
    x1, y1 = puntos[indice + 1]
    return y0 + (y1 - y0) * (x_evaluar - x0) / (x1 - x0)


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.interpolacion_basica import interpolacion_basica
#
# # Entrada: tabla (0,0), (1,10), (2,20); evaluar en x = 0.5
# interpolacion_basica([0, 1, 2], [0, 10, 20], 0.5)   # Salida: 5.0
# interpolacion_basica([0, 1, 2], [0, 10, 20], 1.5)   # Salida: 15.0
