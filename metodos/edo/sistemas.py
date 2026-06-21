"""Runge-Kutta 4 para sistemas de EDO de primer orden (U-III 3.5).

Resuelve un sistema de m ecuaciones diferenciales de primer orden

    y'_k = f_k(x, y_1, ..., y_m),   k = 1..m,   y(x0) = y0

con el método clásico RK4 aplicado vectorialmente. Cada etapa k1..k4 es
ahora un vector de longitud m.

Este mismo solucionador resuelve **ecuaciones de orden superior**
transformándolas en un sistema de primer orden. Para

    y^{(m)} = g(x, y, y', ..., y^{(m-1)})

se define el vector de estado u = (y, y', ..., y^{(m-1)}) y entonces

    u'_1 = u_2,  u'_2 = u_3,  ...,  u'_m = g(x, u_1, ..., u_m).

La función `orden_superior` construye esa f automáticamente a partir de g.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_entero_positivo, validar_funcion

# Tipo de la función del sistema: (x, vector_y) -> vector_derivadas.
FuncionSistema = Callable[[float, Sequence[float]], Sequence[float]]


def _suma_escalada(
    base: Sequence[float], factor: float, incremento: Sequence[float]
) -> list[float]:
    """Devuelve ``base + factor·incremento`` componente a componente."""
    return [b + factor * d for b, d in zip(base, incremento)]


def resolver_sistema(
    f: FuncionSistema,
    x0: float,
    y0: Sequence[float],
    x_final: float,
    n: int = 100,
) -> dict:
    """Resuelve un sistema de EDO de primer orden con RK4 vectorial.

    Args:
        f: Función f(x, y) que recibe el vector de estado y devuelve el
            vector de derivadas (ambos de longitud m).
        x0: Valor inicial de x.
        y0: Vector de condiciones iniciales (longitud m).
        x_final: Valor final de x (distinto de x0).
        n: Número de pasos (n >= 1).

    Returns:
        Diccionario con:
            - ``x`` (list[float]): Malla de x (longitud n + 1).
            - ``columnas`` (list[list[float]]): Una lista por componente
              y_k, cada una de longitud n + 1.
            - ``solucion`` (list[tuple]): Lista de (x_i, (y1_i, ..., ym_i)).
            - ``h`` (float): Tamaño de paso.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, `y0` está vacío,
            n <= 0, x_final == x0 o las dimensiones no son consistentes.

    Example:
        >>> # y1' = y2, y2' = -y1 (oscilador), y(0)=(0,1) -> y1=sin(x)
        >>> import math
        >>> f = lambda x, y: [y[1], -y[0]]
        >>> r = resolver_sistema(f, 0, [0.0, 1.0], math.pi / 2, n=200)
        >>> round(r["columnas"][0][-1], 4)
        1.0
    """
    validar_funcion(f)
    validar_entero_positivo(n, "n")
    if not isinstance(y0, (list, tuple)) or len(y0) == 0:
        raise EntradaInvalidaError("'y0' debe ser un vector no vacío.")
    if x_final == x0:
        raise EntradaInvalidaError("x_final debe ser distinto de x0.")

    m = len(y0)
    h = (x_final - x0) / n
    x = x0
    y = [float(v) for v in y0]

    malla_x = [x]
    columnas: list[list[float]] = [[y[k]] for k in range(m)]
    solucion = [(x, tuple(y))]

    for _ in range(n):
        k1 = list(f(x, y))
        _verificar_dim(k1, m)
        k2 = list(f(x + h / 2, _suma_escalada(y, h / 2, k1)))
        k3 = list(f(x + h / 2, _suma_escalada(y, h / 2, k2)))
        k4 = list(f(x + h, _suma_escalada(y, h, k3)))

        y = [y[i] + h / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(m)]
        x = x + h

        malla_x.append(x)
        for k in range(m):
            columnas[k].append(y[k])
        solucion.append((x, tuple(y)))

    return {"x": malla_x, "columnas": columnas, "solucion": solucion, "h": h}


def _verificar_dim(vector: list[float], m: int) -> None:
    """Valida que la función del sistema devolvió un vector de tamaño m."""
    if len(vector) != m:
        raise EntradaInvalidaError(
            f"La función del sistema debe devolver {m} valores "
            f"(uno por ecuación); devolvió {len(vector)}."
        )


def orden_superior(
    g: Callable[..., float],
    x0: float,
    condiciones_iniciales: Sequence[float],
    x_final: float,
    n: int = 100,
) -> dict:
    """Resuelve y^{(m)} = g(x, y, y', ..., y^{(m-1)}) reduciéndola a sistema.

    Args:
        g: Función que define la derivada de mayor orden. Se invoca como
            ``g(x, y, y', ..., y^{(m-1)})`` con ``m`` argumentos de estado.
        x0: Valor inicial de x.
        condiciones_iniciales: Vector (y(x0), y'(x0), ..., y^{(m-1)}(x0)).
        x_final: Valor final de x.
        n: Número de pasos.

    Returns:
        El mismo diccionario que `resolver_sistema`. La componente 0
        (``columnas[0]``) es la solución y(x); las demás son sus derivadas.

    Raises:
        EntradaInvalidaError: Si `g` no es invocable o no hay condiciones.

    Example:
        >>> # y'' = -y, y(0)=0, y'(0)=1 -> y = sin(x)
        >>> import math
        >>> r = orden_superior(lambda x, y, dy: -y, 0, [0, 1], math.pi / 2, n=200)
        >>> round(r["columnas"][0][-1], 4)
        1.0
    """
    validar_funcion(g, "g")
    if (
        not isinstance(condiciones_iniciales, (list, tuple))
        or not condiciones_iniciales
    ):
        raise EntradaInvalidaError(
            "'condiciones_iniciales' debe contener al menos un valor."
        )

    def f(x: float, u: Sequence[float]) -> list[float]:
        # u = (y, y', ..., y^{(m-1)}); las primeras derivadas son corrimientos.
        derivadas = list(u[1:])
        derivadas.append(g(x, *u))
        return derivadas

    return resolver_sistema(f, x0, condiciones_iniciales, x_final, n)


# --- Ejemplos comentados ------------------------------------------------
# from metodos.edo.sistemas import resolver_sistema, orden_superior
#
# # Sistema depredador-presa linealizado, o un oscilador:
# f = lambda x, y: [y[1], -y[0]]
# resolver_sistema(f, 0, [0.0, 1.0], 6.283185, n=500)["columnas"][0][-1]
#
# # Ecuación de orden 2:  y'' - y' - 2y = 0,  y(0)=1, y'(0)=0
# g = lambda x, y, dy: dy + 2 * y
# orden_superior(g, 0, [1, 0], 1, n=100)
