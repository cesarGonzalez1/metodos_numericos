"""Subpaquete `metodos.matrices`.

Operaciones con matrices y solución de sistemas de ecuaciones lineales
(Gauss, Gauss-Jordan, LU, Jacobi, Gauss-Seidel, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.matrices.eliminacion_aritmetica import eliminacion_aritmetica
from metodos.matrices.eliminacion_gaussiana import eliminacion_gaussiana
from metodos.matrices.pivoteo_escalado import pivoteo_escalado
from metodos.matrices.pivoteo_parcial import pivoteo_parcial

__all__ = [
    "eliminacion_aritmetica",
    "eliminacion_gaussiana",
    "pivoteo_escalado",
    "pivoteo_parcial",
]
