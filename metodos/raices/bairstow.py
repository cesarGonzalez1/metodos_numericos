"""Método de Bairstow para raíces de polinomios.

Encuentra factores cuadráticos (x^2 - r*x - s) de un polinomio con
coeficientes reales usando únicamente aritmética real. Cada factor
cuadrático aporta un par de raíces (reales o complejas conjugadas); el
polinomio se deflaciona y el proceso se repite hasta agotar el grado. Es
especialmente útil para obtener todas las raíces, incluidas las complejas,
de polinomios de coeficientes reales.

Convención de coeficientes: lista en orden de grado descendente
``[a_n, ..., a_1, a_0]`` (igual que ``numpy.roots`` y que el módulo
``deflacion``).
"""

from __future__ import annotations

import cmath

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_max_iteraciones, validar_tolerancia


def _raices_cuadratica(A: float, B: float, C: float) -> list[complex]:
    """Devuelve las dos raíces de A*x^2 + B*x + C (A != 0)."""
    disc = cmath.sqrt(B * B - 4 * A * C)
    return [(-B + disc) / (2 * A), (-B - disc) / (2 * A)]


def _factor_cuadratico(
    a: list[float], r: float, s: float, tolerancia: float, max_iteraciones: int
) -> tuple[float, float, list[float], bool, int]:
    """Refina un factor cuadrático (x^2 - r*x - s) sobre `a` (orden ascendente).

    Returns:
        Tupla ``(r, s, b, convergio, iteraciones)`` donde ``b`` contiene los
        coeficientes de la división sintética (el cociente deflactado vive
        en ``b[2:]``).
    """
    n = len(a) - 1
    convergio = False
    it = 0
    b = list(a)
    for it in range(1, max_iteraciones + 1):
        b = [0.0] * (n + 1)
        b[n] = a[n]
        b[n - 1] = a[n - 1] + r * b[n]
        for i in range(n - 2, -1, -1):
            b[i] = a[i] + r * b[i + 1] + s * b[i + 2]

        c = [0.0] * (n + 1)
        c[n] = b[n]
        c[n - 1] = b[n - 1] + r * c[n]
        for i in range(n - 2, 0, -1):
            c[i] = b[i] + r * c[i + 1] + s * c[i + 2]

        det = c[2] * c[2] - c[3] * c[1]
        if det == 0:
            # Singularidad: se perturban las estimaciones y se reintenta.
            r += 1.0
            s += 1.0
            continue

        dr = (-b[1] * c[2] + b[0] * c[3]) / det
        ds = (-b[0] * c[2] + b[1] * c[1]) / det
        r += dr
        s += ds

        if abs(dr) + abs(ds) < tolerancia:
            convergio = True
            break

    return r, s, b, convergio, it


def bairstow(
    coeficientes: list[float],
    r: float = 1.0,
    s: float = 1.0,
    tolerancia: float = 1e-6,
    max_iteraciones: int = 100,
) -> dict:
    """Encuentra todas las raíces de un polinomio por el método de Bairstow.

    Args:
        coeficientes: Coeficientes reales en orden de grado descendente.
        r: Estimación inicial para el coeficiente r del factor cuadrático.
        s: Estimación inicial para el coeficiente s del factor cuadrático.
        tolerancia: Criterio de paro sobre |Δr| + |Δs|.
        max_iteraciones: Iteraciones máximas por factor cuadrático.

    Returns:
        Diccionario con las claves:
            - ``raices`` (list[complex]): Todas las raíces encontradas.
            - ``convergio`` (bool): True si todos los factores convergieron.
            - ``iteraciones`` (int): Iteraciones totales acumuladas.
            - ``factores`` (list[dict]): Detalle por factor cuadrático con
              ``r``, ``s``, ``convergio`` e ``iteraciones``.

    Raises:
        EntradaInvalidaError: Si los coeficientes no representan un
            polinomio válido (grado >= 1, coeficiente principal != 0) o si
            los parámetros iterativos no son válidos.

    Example:
        >>> # x^2 + 1  ->  raíces +i, -i
        >>> resultado = bairstow([1, 0, 1])
        >>> sorted(round(z.imag, 4) for z in resultado["raices"])
        [-1.0, 1.0]
    """
    if not isinstance(coeficientes, (list, tuple)):
        raise EntradaInvalidaError("Los coeficientes deben darse como lista o tupla.")
    if len(coeficientes) < 2:
        raise EntradaInvalidaError(
            "Se requieren al menos 2 coeficientes (polinomio de grado >= 1)."
        )
    if coeficientes[0] == 0:
        raise EntradaInvalidaError(
            "El coeficiente principal (primer elemento) no puede ser 0."
        )
    validar_tolerancia(tolerancia)
    validar_max_iteraciones(max_iteraciones)

    # Internamente se trabaja en orden ascendente: a[0] es el término
    # independiente y a[-1] el coeficiente principal.
    a = [float(coef) for coef in reversed(coeficientes)]

    raices: list[complex] = []
    factores: list[dict] = []
    iteraciones_totales = 0
    convergio_global = True

    while len(a) - 1 > 2:
        r, s, b, convergio, its = _factor_cuadratico(
            a, r, s, tolerancia, max_iteraciones
        )
        iteraciones_totales += its
        convergio_global = convergio_global and convergio
        factores.append({"r": r, "s": s, "convergio": convergio, "iteraciones": its})
        # Raíces de x^2 - r*x - s  ->  A=1, B=-r, C=-s.
        raices.extend(_raices_cuadratica(1.0, -r, -s))
        # El cociente deflactado (grado n-2) vive en b[2:].
        a = b[2:]

    # Resolver el polinomio restante (grado 1 o 2) de forma directa.
    grado = len(a) - 1
    if grado == 2:
        raices.extend(_raices_cuadratica(a[2], a[1], a[0]))
    elif grado == 1:
        raices.append(complex(-a[0] / a[1]))

    return {
        "raices": raices,
        "convergio": convergio_global,
        "iteraciones": iteraciones_totales,
        "factores": factores,
    }


# --- Ejemplos de uso (comentados) ---------------------------------------
# from metodos.raices.bairstow import bairstow
#
# # x^3 - 6x^2 + 11x - 6  ->  raíces 1, 2, 3
# resultado = bairstow([1, -6, 11, -6])
# sorted(z.real for z in resultado["raices"])   # [1.0, 2.0, 3.0]
#
# # x^4 + 1  ->  cuatro raíces complejas
# resultado = bairstow([1, 0, 0, 0, 1])
# resultado["raices"]
