"""Regla compuesta del punto medio (U-II 2.3.3).

Para ``h = (b-a)/n`` y ``x_i* = a + (i+1/2)h``:

    integral_a^b f(x) dx ~= h sum_{i=0}^{n-1} f(x_i*).

Si ``f`` tiene segunda derivada continua, el error global es O(h^2).
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_intervalo,
)


def punto_medio_compuesto(
    f: Callable[[float], float], a: float, b: float, n: int = 100
) -> dict:
    """Aproxima una integral con ``n`` paneles por punto medio compuesto."""
    validar_funcion(f)
    validar_intervalo(a, b)
    validar_entero_positivo(n, "n")
    h = (b - a) / n
    nodos = [a + (i + 0.5) * h for i in range(n)]
    integral = h * sum(f(x) for x in nodos)
    return {
        "integral": integral,
        "n": n,
        "h": h,
        "evaluaciones": n,
        "cota de error": "|(b-a) h^2 f''(ξ)| / 24",
    }
