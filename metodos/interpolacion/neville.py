"""Interpolación de Neville.

Evalúa el polinomio interpolante en un punto mediante un esquema recursivo
que combina interpolaciones de orden creciente, construyendo una tabla
triangular. No produce explícitamente los coeficientes del polinomio, pero
es numéricamente estable y aporta una estimación del valor junto con la
tabla intermedia.

Complejidad: O(n^2) en tiempo y memoria.
"""

from __future__ import annotations

from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def neville(x_datos: list[float], y_datos: list[float], x_evaluar: float) -> dict:
    """Interpola con el algoritmo de Neville y devuelve valor y tabla.

    Args:
        x_datos: Coordenadas x conocidas (sin repetidos).
        y_datos: Coordenadas y conocidas, misma longitud que `x_datos`.
        x_evaluar: Punto donde se evalúa el polinomio interpolante.

    Returns:
        Diccionario con:
            - ``valor`` (float): Aproximación en `x_evaluar`.
            - ``tabla`` (list[list[float]]): Tabla triangular de Neville
              (``tabla[i][j]``), lista para mostrarse en la GUI.

    Raises:
        EntradaInvalidaError: Si las listas están vacías, difieren en
            longitud o `x_datos` tiene repetidos.

    Example:
        >>> resultado = neville([1, 2, 3], [1, 4, 9], 2.5)
        >>> round(resultado["valor"], 4)
        6.25
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_sin_duplicados(list(x_datos), "x_datos")

    n = len(x_datos)
    # Q[i][0] = y_i; Q[i][j] combina los nodos i-j .. i.
    q = [[0.0] * n for _ in range(n)]
    for i in range(n):
        q[i][0] = float(y_datos[i])

    for j in range(1, n):
        for i in range(j, n):
            numerador = (x_evaluar - x_datos[i - j]) * q[i][j - 1] - (
                x_evaluar - x_datos[i]
            ) * q[i - 1][j - 1]
            q[i][j] = numerador / (x_datos[i] - x_datos[i - j])

    return {"valor": q[n - 1][n - 1], "tabla": q}


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.neville import neville
#
# # Entrada: nodos de f(x)=x^2 en x=1,2,3; evaluar en 2.5
# r = neville([1, 2, 3], [1, 4, 9], 2.5)
# r["valor"]   # Salida: 6.25 (exacto, pues x^2 es polinomio de grado 2)
