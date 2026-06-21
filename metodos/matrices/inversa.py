"""Inversa de una matriz por Gauss-Jordan con pivoteo parcial (U-IV 4.2).

Calcula A⁻¹ formando la matriz aumentada [A | I] y aplicando eliminación de
Gauss-Jordan hasta llevar el bloque izquierdo a la identidad; el bloque
derecho queda transformado en A⁻¹. Se usa pivoteo parcial para mayor
estabilidad numérica.

    [A | I]  ──Gauss-Jordan──▶  [I | A⁻¹]

Complejidad: O(n³).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_matriz_cuadrada

EPS = 1e-12


def inversa(matriz_a: list[list[float]]) -> dict:
    """Calcula la inversa de una matriz cuadrada por Gauss-Jordan.

    Args:
        matriz_a: Matriz cuadrada (n×n) a invertir.

    Returns:
        Diccionario con:
            - ``inversa`` (list[list[float]]): Matriz A⁻¹ (n×n).
            - ``n`` (int): Dimensión de la matriz.

    Raises:
        EntradaInvalidaError: Si la matriz no es cuadrada o es singular
            (no invertible).

    Example:
        >>> r = inversa([[4, 7], [2, 6]])
        >>> [[round(v, 4) for v in fila] for fila in r["inversa"]]
        [[0.6, -0.7], [-0.2, 0.4]]
    """
    validar_matriz_cuadrada(matriz_a, "matriz_a")
    n = len(matriz_a)
    # Matriz aumentada [A | I] con copias en float.
    aum = [
        [float(v) for v in matriz_a[i]] + [1.0 if j == i else 0.0 for j in range(n)]
        for i in range(n)
    ]

    for col in range(n):
        # Pivoteo parcial: mayor |valor| en la columna actual.
        pivote = max(range(col, n), key=lambda r: abs(aum[r][col]))
        if abs(aum[pivote][col]) < EPS:
            raise EntradaInvalidaError("La matriz es singular: no tiene inversa.")
        aum[col], aum[pivote] = aum[pivote], aum[col]

        # Normaliza la fila del pivote.
        divisor = aum[col][col]
        aum[col] = [v / divisor for v in aum[col]]

        # Elimina la columna en las demás filas.
        for fila in range(n):
            if fila == col:
                continue
            factor = aum[fila][col]
            if factor != 0.0:
                aum[fila] = [
                    valor - factor * piv for valor, piv in zip(aum[fila], aum[col])
                ]

    inversa_a = [fila[n:] for fila in aum]
    return {"inversa": inversa_a, "n": n}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.matrices.inversa import inversa
#
# inversa([[2, 0], [0, 4]])["inversa"]   # [[0.5, 0.0], [0.0, 0.25]]
