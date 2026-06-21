"""Factorización de Cholesky (U-IV 4.3.3).

Para una matriz simétrica y definida positiva A, calcula A = L·Lᵀ con L
triangular inferior de diagonal positiva:

    l_{jj} = sqrt( a_{jj} − Σ_{k<j} l_{jk}² )
    l_{ij} = ( a_{ij} − Σ_{k<j} l_{ik} l_{jk} ) / l_{jj}   (i > j)

Es aproximadamente el doble de eficiente que LU porque aprovecha la
simetría, y el propio algoritmo certifica si A es definida positiva (falla
al intentar la raíz de un número no positivo). Complejidad O(n³/3).
"""

from __future__ import annotations

import math

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_matriz_cuadrada, validar_sistema_lineal

EPS = 1e-12


def _validar_simetrica(a: list[list[float]]) -> None:
    """Valida que la matriz sea (numéricamente) simétrica."""
    n = len(a)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(a[i][j] - a[j][i]) > 1e-9:
                raise EntradaInvalidaError(
                    "Cholesky requiere una matriz simétrica "
                    f"(a[{i}][{j}] != a[{j}][{i}])."
                )


def cholesky(matriz_a: list[list[float]]) -> dict:
    """Factoriza A = L·Lᵀ (A simétrica definida positiva).

    Args:
        matriz_a: Matriz simétrica definida positiva (n×n).

    Returns:
        Diccionario con:
            - ``L`` (list[list[float]]): Triangular inferior tal que L·Lᵀ = A.
            - ``n`` (int): Dimensión.

    Raises:
        EntradaInvalidaError: Si la matriz no es cuadrada, no es simétrica
            o no es definida positiva.

    Example:
        >>> r = cholesky([[4, 2], [2, 2]])
        >>> r["L"]
        [[2.0, 0.0], [1.0, 1.0]]
    """
    validar_matriz_cuadrada(matriz_a, "matriz_a")
    a = [[float(v) for v in fila] for fila in matriz_a]
    _validar_simetrica(a)
    n = len(a)
    L = [[0.0] * n for _ in range(n)]

    for j in range(n):
        suma_diag = a[j][j] - sum(L[j][k] ** 2 for k in range(j))
        if suma_diag <= EPS:
            raise EntradaInvalidaError(
                "La matriz no es definida positiva: no admite factorización "
                "de Cholesky."
            )
        L[j][j] = math.sqrt(suma_diag)
        for i in range(j + 1, n):
            L[i][j] = (a[i][j] - sum(L[i][k] * L[j][k] for k in range(j))) / L[j][j]

    return {"L": L, "n": n}


def resolver_cholesky(matriz_a: list[list[float]], vector_b: list[float]) -> dict:
    """Resuelve A·x = b con la factorización de Cholesky de A.

    Args:
        matriz_a: Matriz simétrica definida positiva (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Diccionario con ``solucion`` (list[float]) y ``L``.

    Raises:
        EntradaInvalidaError: Si el sistema es incompatible o A no es
            simétrica definida positiva.

    Example:
        >>> resolver_cholesky([[4, 2], [2, 2]], [6, 4])["solucion"]
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    L = cholesky(matriz_a)["L"]
    n = len(vector_b)
    b = [float(v) for v in vector_b]

    # L·y = b (hacia adelante).
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    # Lᵀ·x = y (hacia atrás).
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
    return {"solucion": x, "L": L}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.matrices.cholesky import cholesky, resolver_cholesky
#
# cholesky([[25, 15, -5], [15, 18, 0], [-5, 0, 11]])["L"]
