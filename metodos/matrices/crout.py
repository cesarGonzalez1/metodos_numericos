"""Factorización de Crout (U-IV 4.3.4).

Descompone A = L·U, pero a diferencia de Doolittle aquí es U la que tiene
diagonal unitaria (u_ii = 1) y L absorbe los pivotes:

    l_{ij} = a_{ij} − Σ_{k<j} l_{ik} u_{kj}              (i >= j)
    u_{ij} = ( a_{ij} − Σ_{k<i} l_{ik} u_{kj} ) / l_{ii}  (i < j)

Como en LU, una vez factorizada A·x = b se resuelve con dos sustituciones
(L·y = b hacia adelante, U·x = y hacia atrás). Complejidad O(n³).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_matriz_cuadrada, validar_sistema_lineal

EPS = 1e-12


def crout(matriz_a: list[list[float]]) -> dict:
    """Factoriza A = L·U por el método de Crout (U con diagonal unitaria).

    Args:
        matriz_a: Matriz cuadrada (n×n).

    Returns:
        Diccionario con:
            - ``L`` (list[list[float]]): Triangular inferior.
            - ``U`` (list[list[float]]): Triangular superior, diagonal 1.
            - ``n`` (int): Dimensión.

    Raises:
        EntradaInvalidaError: Si la matriz no es cuadrada o aparece un
            pivote nulo (requiere pivoteo o es singular).

    Example:
        >>> r = crout([[2, 1], [1, 3]])
        >>> r["U"][0][0]
        1.0
    """
    validar_matriz_cuadrada(matriz_a, "matriz_a")
    a = [[float(v) for v in fila] for fila in matriz_a]
    n = len(a)
    L = [[0.0] * n for _ in range(n)]
    U = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for j in range(n):
        # Columna j de L (parte inferior, i >= j).
        for i in range(j, n):
            L[i][j] = a[i][j] - sum(L[i][k] * U[k][j] for k in range(j))
        if abs(L[j][j]) < EPS:
            raise EntradaInvalidaError(
                f"Pivote nulo en la posición {j}: la matriz requiere pivoteo "
                "o es singular (no admite factorización de Crout directa)."
            )
        # Fila j de U (parte superior, i < ... ).
        for i in range(j + 1, n):
            U[j][i] = (a[j][i] - sum(L[j][k] * U[k][i] for k in range(j))) / L[j][j]

    return {"L": L, "U": U, "n": n}


def resolver_crout(matriz_a: list[list[float]], vector_b: list[float]) -> dict:
    """Resuelve A·x = b con la factorización de Crout de A.

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Diccionario con ``solucion`` (list[float]), ``L`` y ``U``.

    Raises:
        EntradaInvalidaError: Si el sistema es incompatible o A no admite
            la factorización.

    Example:
        >>> resolver_crout([[2, 1], [1, 3]], [3, 4])["solucion"]
        [1.0, 1.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    factor = crout(matriz_a)
    L, U = factor["L"], factor["U"]
    n = len(vector_b)
    b = [float(v) for v in vector_b]

    # L·y = b (hacia adelante).
    y = [0.0] * n
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i))) / L[i][i]
    # U·x = y (hacia atrás, U diagonal unitaria).
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))
    return {"solucion": x, "L": L, "U": U}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.matrices.crout import crout, resolver_crout
#
# resolver_crout([[2, 1], [1, 3]], [3, 4])["solucion"]   # [1.0, 1.0]
