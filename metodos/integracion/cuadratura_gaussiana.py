"""Cuadratura gaussiana (Gauss-Legendre).

Aproxima la integral como una suma ponderada de evaluaciones de f en nodos
óptimos (raíces de los polinomios de Legendre):

    ∫_a^b f(x) dx ≈ (b-a)/2 · Σ w_i · f( (b-a)/2·ξ_i + (a+b)/2 )

Con n puntos integra exactamente polinomios de grado hasta 2n-1, lo que la
hace muy eficiente para funciones suaves. Se incluyen nodos y pesos
precalculados para n = 2..5.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_intervalo

# Nodos (ξ_i) y pesos (w_i) de Gauss-Legendre en el intervalo [-1, 1].
NODOS_PESOS: dict[int, tuple[tuple[float, ...], tuple[float, ...]]] = {
    2: (
        (-0.5773502691896257, 0.5773502691896257),
        (1.0, 1.0),
    ),
    3: (
        (-0.7745966692414834, 0.0, 0.7745966692414834),
        (0.5555555555555556, 0.8888888888888888, 0.5555555555555556),
    ),
    4: (
        (
            -0.8611363115940526,
            -0.3399810435848563,
            0.3399810435848563,
            0.8611363115940526,
        ),
        (
            0.3478548451374538,
            0.6521451548625461,
            0.6521451548625461,
            0.3478548451374538,
        ),
    ),
    5: (
        (
            -0.9061798459386640,
            -0.5384693101056831,
            0.0,
            0.5384693101056831,
            0.9061798459386640,
        ),
        (
            0.2369268850561891,
            0.4786286704993665,
            0.5688888888888889,
            0.4786286704993665,
            0.2369268850561891,
        ),
    ),
}

PUNTOS_VALIDOS = tuple(sorted(NODOS_PESOS))


def cuadratura_gaussiana(
    f: Callable[[float], float], a: float, b: float, puntos: int = 3
) -> float:
    """Aproxima ∫_a^b f(x) dx con cuadratura de Gauss-Legendre.

    Args:
        f: Función a integrar.
        a: Límite inferior de integración.
        b: Límite superior de integración (b > a).
        puntos: Número de nodos de Gauss (2, 3, 4 o 5).

    Returns:
        Aproximación numérica de la integral.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, a >= b o `puntos` no
            está entre los soportados.

    Example:
        >>> round(cuadratura_gaussiana(lambda x: x**3, 0, 2, puntos=2), 6)
        4.0
    """
    validar_funcion(f)
    validar_intervalo(a, b)
    if puntos not in NODOS_PESOS:
        raise EntradaInvalidaError(
            f"'puntos' debe ser uno de {PUNTOS_VALIDOS}, se recibió: {puntos}."
        )

    nodos, pesos = NODOS_PESOS[puntos]
    media = (a + b) / 2
    semiancho = (b - a) / 2
    total = sum(w * f(semiancho * xi + media) for xi, w in zip(nodos, pesos))
    return semiancho * total


# --- Ejemplos comentados ------------------------------------------------
# from metodos.integracion.cuadratura_gaussiana import cuadratura_gaussiana
#
# # ∫_0^2 x^3 dx = 4; con 2 puntos ya es exacta (grado 3 <= 2·2-1)
# cuadratura_gaussiana(lambda x: x**3, 0, 2, puntos=2)   # Salida: 4.0
