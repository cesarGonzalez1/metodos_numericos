"""Método de Müller para búsqueda de raíces.

Generalización del método de la secante que ajusta una parábola a través
de tres puntos y toma como nueva aproximación la raíz de esa parábola más
cercana al último punto. Gracias a la aritmética compleja puede encontrar
raíces complejas aun partiendo de aproximaciones reales.
"""

from __future__ import annotations

import cmath
from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_funcion,
    validar_max_iteraciones,
    validar_tolerancia,
)


def muller(
    f: Callable[[complex], complex],
    x0: complex,
    x1: complex,
    x2: complex,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra una raíz (real o compleja) de `f` por el método de Müller.

    Args:
        f: Función de la cual se busca la raíz (puede ser compleja).
        x0: Primera aproximación inicial.
        x1: Segunda aproximación inicial.
        x2: Tercera aproximación inicial (las tres deben ser distintas).
        tolerancia: Error absoluto máximo aceptado entre iteraciones.
        max_iteraciones: Número máximo de iteraciones permitidas.

    Returns:
        Diccionario con las claves:
            - ``raiz`` (complex): Aproximación de la raíz. Puede ser real
              (parte imaginaria nula) o compleja.
            - ``iteraciones`` (int), ``convergio`` (bool), ``error`` (float)
            - ``historial`` (list[dict]) con ``i``, ``x`` y ``error``.

    Raises:
        EntradaInvalidaError: Si los parámetros no son válidos, si las
            aproximaciones iniciales no son distintas o si el denominador se
            anula durante la iteración.

    Example:
        >>> # x^2 + 1 = 0  ->  raíz compleja i
        >>> resultado = muller(lambda x: x**2 + 1, 0j, 0.5j, 1j)
        >>> abs(resultado["raiz"] - 1j) < 1e-4
        True
    """
    validar_funcion(f)
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)
    if len({x0, x1, x2}) < 3:
        raise EntradaInvalidaError(
            "Las tres aproximaciones iniciales (x0, x1, x2) deben ser "
            "distintas entre sí."
        )

    x0, x1, x2 = complex(x0), complex(x1), complex(x2)
    historial: list[dict] = []
    error = float("inf")
    convergio = False

    for i in range(1, max_iteraciones + 1):
        h0 = x1 - x0
        h1 = x2 - x1
        if h0 == 0 or h1 == 0:
            raise EntradaInvalidaError(
                f"Puntos repetidos en la iteración {i}; Müller no puede " "continuar."
            )
        d0 = (f(x1) - f(x0)) / h0
        d1 = (f(x2) - f(x1)) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a * h1 + d1
        c = f(x2)

        radical = cmath.sqrt(b * b - 4 * a * c)
        # Se elige el signo que maximiza el denominador (mayor estabilidad).
        denominador = (
            b + radical if abs(b + radical) >= abs(b - radical) else b - radical
        )
        if denominador == 0:
            raise EntradaInvalidaError(
                f"Denominador nulo en la iteración {i}; Müller no puede " "continuar."
            )

        dx = -2 * c / denominador
        x3 = x2 + dx
        error = abs(dx)
        historial.append({"i": i, "x": x3, "error": error})

        if error < tolerancia:
            convergio = True
            x2 = x3
            break

        x0, x1, x2 = x1, x2, x3

    return {
        "raiz": x2,
        "iteraciones": len(historial),
        "convergio": convergio,
        "error": error,
        "historial": historial,
    }


# --- Ejemplos de uso (comentados) ---------------------------------------
# from metodos.raices.muller import muller
#
# # Raíz real de x^3 - x^2 + x - 1  ->  1.0
# resultado = muller(lambda x: x**3 - x**2 + x - 1, 0, 0.5, 1.5)
# resultado["raiz"].real
#
# # Raíz compleja de x^2 + 1  ->  i
# resultado = muller(lambda x: x**2 + 1, 0j, 0.5j, 1j)
# resultado["raiz"]
