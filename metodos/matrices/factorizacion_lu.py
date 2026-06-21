"""Factorización LU por el método de Doolittle (U-IV 4.3.1).

Descompone A = L·U, con L triangular inferior de diagonal unitaria
(l_ii = 1) y U triangular superior:

    u_{ij} = a_{ij} − Σ_{k<i} l_{ik} u_{kj}        (j >= i)
    l_{ij} = (a_{ij} − Σ_{k<j} l_{ik} u_{kj}) / u_{jj}   (i > j)

Una vez factorizada, resolver A·x = b se reduce a dos sustituciones:
L·y = b (hacia adelante) y U·x = y (hacia atrás). Esto es muy eficiente
cuando se resuelven varios sistemas con la misma A y distintos b.

No realiza pivoteo: si aparece un pivote nulo lanza un error. Complejidad
O(n³) para factorizar, O(n²) por cada sistema resuelto.
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_matriz_cuadrada, validar_sistema_lineal

EPS = 1e-12


def factorizacion_lu(matriz_a: list[list[float]]) -> dict:
    """Factoriza A = L·U por Doolittle (sin pivoteo).

    Args:
        matriz_a: Matriz cuadrada (n×n).

    Returns:
        Diccionario con:
            - ``L`` (list[list[float]]): Triangular inferior, diagonal 1.
            - ``U`` (list[list[float]]): Triangular superior.
            - ``n`` (int): Dimensión.

    Raises:
        EntradaInvalidaError: Si la matriz no es cuadrada o requiere
            pivoteo (pivote nulo durante la factorización).

    Example:
        >>> r = factorizacion_lu([[4, 3], [6, 3]])
        >>> r["U"][0][0]
        4.0
    """
    validar_matriz_cuadrada(matriz_a, "matriz_a")
    n = len(matriz_a)
    a = [[float(v) for v in fila] for fila in matriz_a]
    L = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    U = [[0.0] * n for _ in range(n)]

    for i in range(n):
        # Fila i de U.
        for j in range(i, n):
            U[i][j] = a[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        if abs(U[i][i]) < EPS:
            raise EntradaInvalidaError(
                f"Pivote nulo en la posición {i}: la matriz requiere pivoteo "
                "o es singular (no admite factorización LU directa)."
            )
        # Columna i de L.
        for j in range(i + 1, n):
            L[j][i] = (a[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

    return {"L": L, "U": U, "n": n}


def _sustitucion_adelante(L: list[list[float]], b: list[float]) -> list[float]:
    """Resuelve L·y = b con L triangular inferior de diagonal unitaria."""
    n = len(b)
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][k] * y[k] for k in range(i))
    return y


def _sustitucion_atras(U: list[list[float]], y: list[float]) -> list[float]:
    """Resuelve U·x = y con U triangular superior."""
    n = len(y)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]
    return x


def resolver_lu(matriz_a: list[list[float]], vector_b: list[float]) -> dict:
    """Resuelve A·x = b usando la factorización LU de A.

    Args:
        matriz_a: Matriz de coeficientes (n×n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Diccionario con ``solucion`` (list[float]), ``L`` y ``U``.

    Raises:
        EntradaInvalidaError: Si el sistema es incompatible dimensionalmente
            o A no admite factorización LU directa.

    Example:
        >>> resolver_lu([[4, 3], [6, 3]], [10, 12])["solucion"]
        [1.0, 2.0]
    """
    validar_sistema_lineal(matriz_a, vector_b)
    factor = factorizacion_lu(matriz_a)
    L, U = factor["L"], factor["U"]
    y = _sustitucion_adelante(L, [float(v) for v in vector_b])
    x = _sustitucion_atras(U, y)
    return {"solucion": x, "L": L, "U": U}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.matrices.factorizacion_lu import factorizacion_lu, resolver_lu
#
# resolver_lu([[2, 1], [1, 3]], [3, 4])["solucion"]   # [1.0, 1.0]
