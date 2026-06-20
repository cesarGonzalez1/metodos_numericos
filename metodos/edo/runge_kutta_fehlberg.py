"""Método de Runge-Kutta-Fehlberg (RKF45) con paso adaptativo.

Combina un par de fórmulas Runge-Kutta de orden 4 y 5 que comparten
evaluaciones de f. La diferencia entre ambas estima el error local de cada
paso y permite ajustar h automáticamente: se reduce donde la solución
cambia rápido y se agranda donde es suave, manteniendo el error bajo la
tolerancia pedida.

Integra hacia adelante (x_final > x0).
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_paso,
    validar_tolerancia,
)


def runge_kutta_fehlberg(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_final: float,
    tolerancia: float = 1e-6,
    h_inicial: float = 0.1,
    h_min: float = 1e-8,
    max_pasos: int = 100000,
) -> list[tuple[float, float]]:
    """Resuelve dy/dx = f(x, y) con RKF45 y control de paso adaptativo.

    Args:
        f: Función f(x, y) que define la EDO.
        x0: Valor inicial de x.
        y0: Valor inicial de y, y(x0) = y0.
        x_final: Valor final de x (debe ser > x0).
        tolerancia: Error local permitido por paso (> 0).
        h_inicial: Tamaño de paso inicial (> 0).
        h_min: Paso mínimo permitido; por debajo se lanza error.
        max_pasos: Cota de pasos para evitar bucles infinitos.

    Returns:
        Lista de tuplas (x_i, y_i) en los puntos aceptados (no equiespaciados).

    Raises:
        EntradaInvalidaError: Si los parámetros son inválidos, x_final <= x0
            o no se alcanza la tolerancia con h >= h_min.

    Example:
        >>> # dy/dx = y, y(0)=1 -> y(1) = e
        >>> sol = runge_kutta_fehlberg(lambda x, y: y, 0, 1, 1)
        >>> round(sol[-1][1], 5)
        2.71828
    """
    validar_funcion(f)
    validar_tolerancia(tolerancia)
    validar_paso(h_inicial, "h_inicial")
    validar_entero_positivo(max_pasos, "max_pasos")
    if x_final <= x0:
        raise EntradaInvalidaError("x_final debe ser mayor que x0 (RKF45).")

    x, y, h = x0, y0, h_inicial
    solucion = [(x, y)]

    for _ in range(max_pasos):
        if x >= x_final:
            break
        if x + h > x_final:
            h = x_final - x

        k1 = h * f(x, y)
        k2 = h * f(x + h / 4, y + k1 / 4)
        k3 = h * f(x + 3 * h / 8, y + 3 * k1 / 32 + 9 * k2 / 32)
        k4 = h * f(
            x + 12 * h / 13,
            y + 1932 * k1 / 2197 - 7200 * k2 / 2197 + 7296 * k3 / 2197,
        )
        k5 = h * f(
            x + h,
            y + 439 * k1 / 216 - 8 * k2 + 3680 * k3 / 513 - 845 * k4 / 4104,
        )
        k6 = h * f(
            x + h / 2,
            y
            - 8 * k1 / 27
            + 2 * k2
            - 3544 * k3 / 2565
            + 1859 * k4 / 4104
            - 11 * k5 / 40,
        )

        y4 = y + 25 * k1 / 216 + 1408 * k3 / 2565 + 2197 * k4 / 4104 - k5 / 5
        y5 = (
            y
            + 16 * k1 / 135
            + 6656 * k3 / 12825
            + 28561 * k4 / 56430
            - 9 * k5 / 50
            + 2 * k6 / 55
        )

        error = abs(y5 - y4)
        if error <= tolerancia or h <= h_min:
            x = x + h
            y = y5  # se acepta la estimación de mayor orden
            solucion.append((x, y))

        # Ajuste del paso (factor de seguridad 0.84, acotado).
        if error == 0:
            factor = 4.0
        else:
            factor = 0.84 * (tolerancia / error) ** 0.25
        factor = min(max(factor, 0.1), 4.0)
        h = h * factor

        if h < h_min and error > tolerancia:
            raise EntradaInvalidaError(
                "No se alcanzó la tolerancia: el paso requerido es menor que "
                f"h_min ({h_min}). Relaje la tolerancia o revise f."
            )

    return solucion


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.runge_kutta_fehlberg import runge_kutta_fehlberg
#
# # dy/dx = y, y(0)=1; integra de 0 a 1 con control de error
# sol = runge_kutta_fehlberg(lambda x, y: y, 0, 1, 1, tolerancia=1e-8)
# sol[-1]   # (1.0, ~2.718282)
