"""Subpaquete `metodos.raices`.

Métodos de búsqueda de raíces de ecuaciones no lineales (bisección,
Newton-Raphson, secante, punto fijo, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.raices.bairstow import bairstow
from metodos.raices.biseccion import biseccion
from metodos.raices.deflacion import deflacion
from metodos.raices.falsa_posicion import falsa_posicion
from metodos.raices.muller import muller
from metodos.raices.newton_raphson import newton_raphson
from metodos.raices.punto_fijo import punto_fijo
from metodos.raices.secante import secante

__all__ = [
    "bairstow",
    "biseccion",
    "deflacion",
    "falsa_posicion",
    "muller",
    "newton_raphson",
    "punto_fijo",
    "secante",
]
