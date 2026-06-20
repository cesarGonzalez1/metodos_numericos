"""Subpaquete `metodos.integracion`.

Integración numérica (trapecio, Simpson, cuadratura de Gauss, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.integracion.cuadratura_adaptativa import cuadratura_adaptativa
from metodos.integracion.cuadratura_gaussiana import cuadratura_gaussiana
from metodos.integracion.punto_medio import punto_medio
from metodos.integracion.romberg import romberg
from metodos.integracion.simpson_tres_octavos import simpson_tres_octavos
from metodos.integracion.simpson_tres_octavos_compuesto import (
    simpson_tres_octavos_compuesto,
)
from metodos.integracion.simpson_un_tercio import simpson_un_tercio
from metodos.integracion.simpson_un_tercio_compuesto import (
    simpson_un_tercio_compuesto,
)
from metodos.integracion.trapecio import trapecio
from metodos.integracion.trapecio_compuesto import trapecio_compuesto

__all__ = [
    "cuadratura_adaptativa",
    "cuadratura_gaussiana",
    "punto_medio",
    "romberg",
    "simpson_tres_octavos",
    "simpson_tres_octavos_compuesto",
    "simpson_un_tercio",
    "simpson_un_tercio_compuesto",
    "trapecio",
    "trapecio_compuesto",
]
