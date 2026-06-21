"""Factorización LDLᵀ (U-IV 4.3.2).

Para una matriz simétrica A, calcula A = L·D·Lᵀ con L triangular inferior
de diagonal unitaria y D diagonal. A diferencia de Cholesky, no requiere
raíces cuadradas ni que A sea definida positiva (basta que sea simétrica y
que los pivotes d_j no se anulen):

    d_j   = a_{jj} − Σ_{k<j} l_{jk}² · d_k
    l_{ij} = ( a_{ij} − Σ_{k<j} l_{ik} d_k l_{jk} ) / d_j   (i > j)

Complejidad O(n³/3).
"""

from __future__ import annotations

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
                    "LDLᵀ requiere una matriz simétrica "
                    f"(a[{i}][{j}] != a[{j}][{i}])."
                )


def factorizacion_ldl(matriz_a: list[list[float]]) -> dict:
    """Factoriza A = L·D·Lᵀ (A simétrica).

    Args:
        matriz_a: Matriz simétrica (n×n).

    Returns:
        Diccionario con:
            - ``L`` (list[list[float]]): Triangular inferior, diagonal 1.
            - ``D`` (list[float]): Diagonal de D.
            - ``n`` (int): Dimensión.

    Raises:
        EntradaInvalidaError: Si la matriz no es cuadrada, no es simétrica
            o aparece un pivote nulo.

    Example:
        >>> r = factorizacion_ldl([[4, 2], [2, 2]])
        >>> r["D"]
        [4.0, 1.0]
    """
    validar_matriz_cuadrada(matriz_a, "matriz_a")
    a = [[float(v) for v in fila] for fila in matriz_a]
    _validar_simetrica(a)
    n = len(a)
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    D = [0.0] * n

    for j in range(n):
        D[j] = a[j][j] - sum(L[j][k] ** 2 * D[k] for k in range(j))
        if abs(D[j]) < EPS:
            raise EntradaInvalidaError(
                f"Pivote nulo (D[{j}] ≈ 0): la matriz no admite factorización "
                "LDLᵀ directa."
            )
        for i in range(j + 1, n):
            L[i][j] = (a[i][j] - sum(L[i][k] * D[k] * L[j][k] for k in range(j))) / D[j]

    return {"L": L, "D": D, "n": n}


def resolver_ldl(matriz_a: list[list[float]], vector_b: list[float]) -> dict:
    """Resuelve A·x = b con la factorización LDLᵀ de A.

    Args:
        matriz_a: Matriz simétrica (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Diccionario con ``solucion`` (list[float]), ``L`` y ``D``.

    Raises:
        EntradaInvalidaError: Si el sistema es incompatible o A no admite
            la factorización.

    Example:
        >>> resolver_ldl([[4, 2], [2, 2]], [6, 4])["solucion"]
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    factor = factorizacion_ldl(matriz_a)
    L, D = factor["L"], factor["D"]
    n = len(vector_b)
    b = [float(v) for v in vector_b]

    # L·z = b (hacia adelante, L diagonal unitaria).
    z = [0.0] * n
    for i in range(n):
        z[i] = b[i] - sum(L[i][k] * z[k] for k in range(i))
    # D·y = z (diagonal).
    y = [z[i] / D[i] for i in range(n)]
    # Lᵀ·x = y (hacia atrás).
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - sum(L[k][i] * x[k] for k in range(i + 1, n))
    return {"solucion": x, "L": L, "D": D}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.matrices.factorizacion_ldl import factorizacion_ldl, resolver_ldl
#
# factorizacion_ldl([[4, 12, -16], [12, 37, -43], [-16, -43, 98]])
