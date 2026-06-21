"""Método multipaso de Adams-Bashforth-Moulton (U-III 3.4).

Predictor-corrector de cuarto orden. A diferencia de los métodos de un paso
(Euler, RK), reutiliza valores ya calculados de f para avanzar, lo que lo
hace eficiente en evaluaciones de función:

Predictor (Adams-Bashforth de 4 pasos, explícito):

    y*_{i+1} = y_i + h/24·(55 f_i − 59 f_{i-1} + 37 f_{i-2} − 9 f_{i-3})

Corrector (Adams-Moulton de 3 pasos, implícito, evaluado con el predictor):

    y_{i+1} = y_i + h/24·(9 f_{i+1} + 19 f_i − 5 f_{i-1} + f_{i-2})

Los primeros cuatro valores (arranque) se generan con Runge-Kutta 4, que
tiene el mismo orden de error global O(h^4). El corrector se puede iterar
hasta que dos aproximaciones sucesivas difieran menos que la tolerancia.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_entero_positivo, validar_funcion


def _arranque_rk4(
    f: Callable[[float, float], float], x0: float, y0: float, h: float
) -> list[tuple[float, float]]:
    """Genera los primeros 4 puntos con RK4 para arrancar el multipaso."""
    puntos = [(x0, y0)]
    x, y = x0, y0
    for _ in range(3):
        k1 = f(x, y)
        k2 = f(x + h / 2, y + h / 2 * k1)
        k3 = f(x + h / 2, y + h / 2 * k2)
        k4 = f(x + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        x = x + h
        puntos.append((x, y))
    return puntos


def adams(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_final: float,
    n: int = 100,
    tolerancia: float = 1e-8,
    max_correcciones: int = 50,
) -> dict:
    """Resuelve dy/dx = f(x, y) con Adams-Bashforth-Moulton de 4º orden.

    Args:
        f: Función f(x, y) que define la EDO.
        x0: Valor inicial de x.
        y0: Valor inicial de y, y(x0) = y0.
        x_final: Valor final de x (distinto de x0).
        n: Número de pasos (n >= 4 para usar el esquema multipaso completo).
        tolerancia: Criterio de paro al iterar el corrector.
        max_correcciones: Máximo de iteraciones del corrector por paso.

    Returns:
        Diccionario con:
            - ``solucion`` (list[tuple[float, float]]): Puntos (x_i, y_i).
            - ``h`` (float): Tamaño de paso.
            - ``n`` (int): Número de pasos.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, n < 4 o x_final == x0.

    Example:
        >>> # dy/dx = y, y(0)=1 -> y(1)=e
        >>> r = adams(lambda x, y: y, 0, 1, 1, n=10)
        >>> round(r["solucion"][-1][1], 5)
        2.71828
    """
    validar_funcion(f)
    validar_entero_positivo(n, "n")
    if x_final == x0:
        raise EntradaInvalidaError("x_final debe ser distinto de x0.")
    if n < 4:
        raise EntradaInvalidaError(
            "Adams-Bashforth-Moulton de 4º orden requiere n >= 4 pasos."
        )

    h = (x_final - x0) / n
    solucion = _arranque_rk4(f, x0, y0, h)
    # Cache de evaluaciones f_i correspondientes a cada punto inicial.
    efes = [f(x, y) for x, y in solucion]

    for i in range(3, n):
        x_i, y_i = solucion[i]
        x_sig = x_i + h
        # Predictor (Adams-Bashforth 4 pasos).
        y_pred = y_i + h / 24.0 * (
            55 * efes[i] - 59 * efes[i - 1] + 37 * efes[i - 2] - 9 * efes[i - 3]
        )
        # Corrector (Adams-Moulton 3 pasos), iterado hasta convergencia.
        y_corr = y_pred
        for _ in range(max_correcciones):
            f_sig = f(x_sig, y_corr)
            nuevo = y_i + h / 24.0 * (
                9 * f_sig + 19 * efes[i] - 5 * efes[i - 1] + efes[i - 2]
            )
            if abs(nuevo - y_corr) < tolerancia:
                y_corr = nuevo
                break
            y_corr = nuevo

        solucion.append((x_sig, y_corr))
        efes.append(f(x_sig, y_corr))

    return {"solucion": solucion, "h": h, "n": n}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.adams import adams
#
# # dy/dx = x - y, y(0)=1 ; solución exacta y = x - 1 + 2 e^{-x}
# r = adams(lambda x, y: x - y, 0, 1, 2, n=20)
# r["solucion"][-1]
