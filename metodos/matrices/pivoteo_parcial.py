"""Eliminación gaussiana con pivoteo parcial.

Antes de eliminar cada columna, intercambia filas para colocar como pivote
el elemento de mayor valor absoluto de esa columna (de la fila actual hacia
abajo). Esto reduce los errores de redondeo y evita la división por pivotes
muy pequeños, haciendo el método mucho más estable que la eliminación
simple.

Complejidad: O(n^3).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_sistema_lineal

EPS = 1e-12


def pivoteo_parcial(matriz_a: list[list[float]], vector_b: list[float]) -> list[float]:
    """Resuelve A·x = b por eliminación gaussiana con pivoteo parcial.

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Vector solución x (largo n).

    Raises:
        EntradaInvalidaError: Si las dimensiones no son compatibles o la
            matriz es singular (mejor pivote (casi) nulo).

    Example:
        >>> # Sistema cuyo primer pivote es 0: requiere intercambio de filas
        >>> pivoteo_parcial([[0, 2], [1, 1]], [4, 3])
        [1.0, 2.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    n = len(matriz_a)
    m = [
        [float(v) for v in fila] + [float(vector_b[i])]
        for i, fila in enumerate(matriz_a)
    ]

    for col in range(n):
        # Fila con el mayor |valor| en la columna actual (desde col).
        pivote = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[pivote][col]) < EPS:
            raise EntradaInvalidaError(
                f"Matriz singular: columna {col} sin pivote no nulo."
            )
        m[col], m[pivote] = m[pivote], m[col]

        for fila in range(col + 1, n):
            factor = m[fila][col] / m[col][col]
            for k in range(col, n + 1):
                m[fila][k] -= factor * m[col][k]

    x = [0.0] * n
    for fila in range(n - 1, -1, -1):
        acumulado = m[fila][n] - sum(m[fila][k] * x[k] for k in range(fila + 1, n))
        x[fila] = acumulado / m[fila][fila]
    return x


# --- Ejemplos / matrices de prueba (comentados) -------------------------
# from metodos.matrices.pivoteo_parcial import pivoteo_parcial
#
# # Pivote inicial nulo -> el pivoteo intercambia filas y resuelve:
# pivoteo_parcial([[0, 2], [1, 1]], [4, 3])   # [1.0, 2.0]
