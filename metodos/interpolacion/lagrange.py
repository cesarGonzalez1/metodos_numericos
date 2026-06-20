"""Interpolación polinómica de Lagrange.

Construye implícitamente el polinomio interpolante de grado n-1 que pasa
por los n puntos dados, como combinación de los polinomios base de
Lagrange L_i(x), y lo evalúa en un punto.

Complejidad: O(n^2) por evaluación.
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def lagrange(x_datos: list[float], y_datos: list[float], x_evaluar: float) -> float:
    """Evalúa el polinomio interpolante de Lagrange en `x_evaluar`.

    Args:
        x_datos: Coordenadas x conocidas (nodos), sin valores repetidos.
        y_datos: Coordenadas y conocidas, mismo largo que `x_datos`.
        x_evaluar: Punto donde se desea evaluar el polinomio interpolante.

    Returns:
        Valor aproximado de la función en `x_evaluar`.

    Raises:
        EntradaInvalidaError: Si `x_datos` y `y_datos` no tienen la misma
            longitud, están vacías o `x_datos` contiene valores repetidos.

    Example:
        >>> # Polinomio que pasa por (0,1), (1,3), (2,7) -> evaluar en 1.5
        >>> round(lagrange([0, 1, 2], [1, 3, 7], 1.5), 4)
        4.75
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_sin_duplicados(list(x_datos), "x_datos")

    n = len(x_datos)
    resultado = 0.0
    for i in range(n):
        termino = y_datos[i]
        for j in range(n):
            if j != i:
                denominador = x_datos[i] - x_datos[j]
                termino *= (x_evaluar - x_datos[j]) / denominador
        resultado += termino
    return resultado


def polinomio_base_lagrange(x_datos: list[float], i: int, x_evaluar: float) -> float:
    """Evalúa el i-ésimo polinomio base de Lagrange L_i(x) en `x_evaluar`.

    Útil para inspeccionar/visualizar la construcción del interpolante.

    Args:
        x_datos: Nodos x (sin repetidos).
        i: Índice del polinomio base (0 <= i < len(x_datos)).
        x_evaluar: Punto de evaluación.

    Returns:
        Valor de L_i(x_evaluar).

    Raises:
        EntradaInvalidaError: Si `i` está fuera de rango.
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_sin_duplicados(list(x_datos), "x_datos")
    if not 0 <= i < len(x_datos):
        raise EntradaInvalidaError(
            f"Índice i={i} fuera de rango [0, {len(x_datos) - 1}]."
        )
    valor = 1.0
    for j in range(len(x_datos)):
        if j != i:
            valor *= (x_evaluar - x_datos[j]) / (x_datos[i] - x_datos[j])
    return valor


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.lagrange import lagrange
#
# # Entrada: nodos (0,1), (1,3), (2,7); evaluar en x = 1.5
# lagrange([0, 1, 2], [1, 3, 7], 1.5)   # Salida: 4.75
