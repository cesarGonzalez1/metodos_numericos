"""Subpaquete `metodos.derivacion`.

Derivación numérica (diferencias finitas, Richardson, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.derivacion.cinco_puntos import cinco_puntos
from metodos.derivacion.cuatro_puntos import cuatro_puntos
from metodos.derivacion.diferencias_finitas import (
    derivada,
    diferencia_adelante,
    diferencia_atras,
    diferencia_centrada,
)
from metodos.derivacion.richardson import richardson
from metodos.derivacion.tres_puntos import tres_puntos

__all__ = [
    "cinco_puntos",
    "cuatro_puntos",
    "derivada",
    "diferencia_adelante",
    "diferencia_atras",
    "diferencia_centrada",
    "richardson",
    "tres_puntos",
]
