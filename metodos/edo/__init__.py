"""Subpaquete `metodos.edo`.

Solución numérica de ecuaciones diferenciales ordinarias (Euler, Runge-Kutta, etc.).

Convención: cada método numérico se implementa en su propio archivo
`snake_case.py` dentro de esta carpeta (ej. una función pública principal
por archivo, con type hints y docstring).
"""

from __future__ import annotations

from metodos.edo.adams import adams
from metodos.edo.adams_variable import adams_variable
from metodos.edo.euler import euler
from metodos.edo.runge_kutta import runge_kutta
from metodos.edo.runge_kutta_fehlberg import runge_kutta_fehlberg
from metodos.edo.taylor_superior import taylor_superior

__all__ = [
    "adams",
    "adams_variable",
    "euler",
    "runge_kutta",
    "runge_kutta_fehlberg",
    "taylor_superior",
]
