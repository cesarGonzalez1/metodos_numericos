"""Subpaquete `metodos.interpolacion`.

Métodos de interpolación (Lagrange, Newton, splines, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.interpolacion.aproximacion_polinomial import aproximacion_polinomial
from metodos.interpolacion.diferencias_divididas import diferencias_divididas
from metodos.interpolacion.interpolacion_basica import interpolacion_basica
from metodos.interpolacion.lagrange import lagrange
from metodos.interpolacion.minimos_cuadrados import minimos_cuadrados
from metodos.interpolacion.neville import neville
from metodos.interpolacion.taylor import taylor

__all__ = [
    "aproximacion_polinomial",
    "diferencias_divididas",
    "interpolacion_basica",
    "lagrange",
    "minimos_cuadrados",
    "neville",
    "taylor",
]
