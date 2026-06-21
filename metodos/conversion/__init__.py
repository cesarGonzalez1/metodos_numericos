"""Subpaquete `metodos.conversion`.

Conversión entre bases numéricas (binario, octal, decimal, hexadecimal).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.conversion.analisis_errores import (
    analisis_errores,
    redondeo_y_truncamiento,
)
from metodos.conversion.binario_a_decimal import binario_a_decimal
from metodos.conversion.decimal_a_binario import decimal_a_binario

__all__ = [
    "analisis_errores",
    "binario_a_decimal",
    "decimal_a_binario",
    "redondeo_y_truncamiento",
]
