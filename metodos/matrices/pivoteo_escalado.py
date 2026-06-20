"""Eliminación gaussiana con pivoteo parcial escalado.

Mejora el pivoteo parcial teniendo en cuenta la magnitud relativa de cada
fila. Para cada fila se calcula un factor de escala (el mayor valor absoluto
de sus coeficientes); en cada columna se elige como pivote la fila que
maximiza el cociente |a[r][col]| / escala[r]. Así se evita que filas con
coeficientes intrínsecamente grandes dominen artificialmente la elección del
pivote, mejorando la estabilidad numérica.

Complejidad: O(n^3).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_sistema_lineal

EPS = 1e-12


def pivoteo_escalado(matriz_a: list[list[float]], vector_b: list[float]) -> list[float]:
    """Resuelve A·x = b por eliminación gaussiana con pivoteo escalado.

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Vector solución x (largo n).

    Raises:
        EntradaInvalidaError: Si las dimensiones no son compatibles, alguna
            fila es nula (escala 0) o la matriz es singular.

    Example:
        >>> pivoteo_escalado([[2, 1], [1, 3]], [3, 4])
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    n = len(matriz_a)
    m = [
        [float(v) for v in fila] + [float(vector_b[i])]
        for i, fila in enumerate(matriz_a)
    ]

    # Factor de escala de cada fila (mayor |coeficiente| en A).
    escalas = [max(abs(m[i][j]) for j in range(n)) for i in range(n)]
    if any(s < EPS for s in escalas):
        raise EntradaInvalidaError(
            "Una fila es completamente nula: la matriz es singular."
        )

    for col in range(n):
        # Fila que maximiza |a[r][col]| / escala[r].
        pivote = max(range(col, n), key=lambda r: abs(m[r][col]) / escalas[r])
        if abs(m[pivote][col]) < EPS:
            raise EntradaInvalidaError(
                f"Matriz singular: columna {col} sin pivote no nulo."
            )
        m[col], m[pivote] = m[pivote], m[col]
        escalas[col], escalas[pivote] = escalas[pivote], escalas[col]

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
# from metodos.matrices.pivoteo_escalado import pivoteo_escalado
#
# # Sistema 3x3 mal escalado:
# A = [[3, -13, 9], [-6, 4, 1], [6, -2, 2]]
# b = [-19, -8, 0]
# pivoteo_escalado(A, b)   # solución estable del sistema
