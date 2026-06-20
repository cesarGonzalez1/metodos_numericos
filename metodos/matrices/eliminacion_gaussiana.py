"""Eliminación gaussiana simple (sin pivoteo).

Resuelve A·x = b transformando la matriz aumentada [A | b] a forma
triangular superior mediante operaciones de fila, seguida de sustitución
hacia atrás.

No realiza intercambios de fila: si aparece un pivote nulo, lanza un error
sugiriendo usar una variante con pivoteo. Complejidad: O(n^3).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_sistema_lineal

# Umbral por debajo del cual un pivote se considera nulo.
EPS = 1e-12


def eliminacion_gaussiana(
    matriz_a: list[list[float]], vector_b: list[float]
) -> list[float]:
    """Resuelve el sistema A·x = b mediante eliminación gaussiana simple.

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Vector solución x (largo n).

    Raises:
        EntradaInvalidaError: Si las dimensiones no son compatibles o
            aparece un pivote (casi) nulo (matriz singular o que requiere
            pivoteo).

    Example:
        >>> eliminacion_gaussiana([[2, 1], [1, 3]], [3, 4])
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    n = len(matriz_a)
    # Matriz aumentada con copias en float (no muta la entrada).
    m = [
        [float(v) for v in fila] + [float(vector_b[i])]
        for i, fila in enumerate(matriz_a)
    ]

    # Eliminación hacia adelante.
    for col in range(n):
        if abs(m[col][col]) < EPS:
            raise EntradaInvalidaError(
                f"Pivote nulo en la columna {col}: use pivoteo parcial o "
                "escalado (la matriz puede ser singular)."
            )
        for fila in range(col + 1, n):
            factor = m[fila][col] / m[col][col]
            for k in range(col, n + 1):
                m[fila][k] -= factor * m[col][k]

    return _sustitucion_atras(m, n)


def _sustitucion_atras(m: list[list[float]], n: int) -> list[float]:
    """Sustitución hacia atrás sobre una matriz aumentada triangular."""
    x = [0.0] * n
    for fila in range(n - 1, -1, -1):
        acumulado = m[fila][n] - sum(m[fila][k] * x[k] for k in range(fila + 1, n))
        x[fila] = acumulado / m[fila][fila]
    return x


# --- Ejemplos / matrices de prueba (comentados) -------------------------
# from metodos.matrices.eliminacion_gaussiana import eliminacion_gaussiana
#
# # Sistema 2x2:  2x + y = 3 ; x + 3y = 4   -> x = 1, y = 1
# eliminacion_gaussiana([[2, 1], [1, 3]], [3, 4])          # [1.0, 1.0]
# # Sistema 3x3:
# A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
# b = [8, -11, -3]
# eliminacion_gaussiana(A, b)                              # [2.0, 3.0, -1.0]
