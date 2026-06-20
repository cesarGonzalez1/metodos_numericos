"""Plantilla: eliminación gaussiana para sistemas de ecuaciones lineales.

Esqueleto de referencia. Otros métodos (Gauss-Jordan, factorización LU,
Jacobi, Gauss-Seidel) van en archivos independientes dentro de
`metodos/matrices/`.
"""

from __future__ import annotations


def eliminacion_gaussiana(
    matriz_a: list[list[float]], vector_b: list[float]
) -> list[float]:
    """Resuelve el sistema A·x = b mediante eliminación gaussiana simple.

    Args:
        matriz_a: Matriz de coeficientes (n x n).
        vector_b: Vector de términos independientes (largo n).

    Returns:
        Vector solución x (largo n).

    Raises:
        ValueError: Si las dimensiones no son compatibles o el sistema
            no tiene solución única (matriz singular).

    TODO(equipo): implementar el algoritmo. Considerar pivoteo parcial.
    """
    raise NotImplementedError("Pendiente de implementar por el equipo.")
