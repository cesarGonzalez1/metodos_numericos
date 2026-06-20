"""Eliminación aritmética (Gauss-Jordan).

Variante de eliminación que reduce la matriz aumentada [A | b] a la forma
escalonada reducida (la parte de A queda como identidad), eliminando los
coeficientes tanto por debajo como por encima de cada pivote y normalizando
cada fila. Al terminar, la última columna contiene directamente la solución,
por lo que no requiere sustitución hacia atrás.

No realiza intercambios de fila: ante un pivote nulo sugiere usar pivoteo.
Complejidad: O(n^3).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_sistema_lineal

EPS = 1e-12


def eliminacion_aritmetica(
    matriz_a: list[list[float]], vector_b: list[float]
) -> list[float]:
    """Resuelve A·x = b por eliminación aritmética (Gauss-Jordan).

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Vector solución x (largo n).

    Raises:
        EntradaInvalidaError: Si las dimensiones no son compatibles o
            aparece un pivote (casi) nulo.

    Example:
        >>> eliminacion_aritmetica([[2, 1], [1, 3]], [3, 4])
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    n = len(matriz_a)
    m = [
        [float(v) for v in fila] + [float(vector_b[i])]
        for i, fila in enumerate(matriz_a)
    ]

    for col in range(n):
        if abs(m[col][col]) < EPS:
            raise EntradaInvalidaError(
                f"Pivote nulo en la columna {col}: use pivoteo parcial o "
                "escalado (la matriz puede ser singular)."
            )
        # Normaliza la fila pivote para dejar 1 en la diagonal.
        pivote = m[col][col]
        for k in range(col, n + 1):
            m[col][k] /= pivote
        # Anula la columna en todas las demás filas (arriba y abajo).
        for fila in range(n):
            if fila != col:
                factor = m[fila][col]
                for k in range(col, n + 1):
                    m[fila][k] -= factor * m[col][k]

    return [m[i][n] for i in range(n)]


# --- Ejemplos / matrices de prueba (comentados) -------------------------
# from metodos.matrices.eliminacion_aritmetica import eliminacion_aritmetica
#
# # Sistema 3x3:
# A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
# b = [8, -11, -3]
# eliminacion_aritmetica(A, b)   # [2.0, 3.0, -1.0]
