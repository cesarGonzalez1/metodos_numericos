"""Fórmula general de derivación con n+1 puntos (U-II 2.1.2).

Los pesos se obtienen imponiendo exactitud sobre la base monomial. Para
desplazamientos adimensionales ``t_j`` se resuelve

    sum_j w_j t_j^k = delta_{k,1},    k = 0, ..., p-1,

y entonces ``f'(x) ~= (1/h) sum_j w_j f(x + h t_j)``. El procedimiento
produce, en vez de memorizarla, la fórmula de diferencias finitas de
``p = n+1`` puntos solicitada.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_funcion, validar_paso


def _resolver_sistema(a: list[list[float]], b: list[float]) -> list[float]:
    """Resuelve un sistema pequeño con Gauss y pivoteo parcial."""
    n = len(b)
    m = [fila[:] + [b[i]] for i, fila in enumerate(a)]
    for k in range(n):
        pivote = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[pivote][k]) < 1e-15:
            raise EntradaInvalidaError("No fue posible construir los pesos.")
        m[k], m[pivote] = m[pivote], m[k]
        for i in range(k + 1, n):
            factor = m[i][k] / m[k][k]
            for j in range(k, n + 1):
                m[i][j] -= factor * m[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))) / m[i][i]
    return x


def n_mas_un_puntos(
    f: Callable[[float], float],
    x: float,
    h: float = 0.01,
    puntos: int = 5,
    alineacion: str = "centrada",
) -> dict:
    """Aproxima ``f'(x)`` mediante una fórmula generada de ``puntos`` nodos.

    ``alineacion`` puede ser ``centrada``, ``adelante`` o ``atras``. Una
    plantilla centrada exige un número impar de puntos para ser simétrica.
    La fórmula es exacta para polinomios hasta grado ``puntos - 1``.
    """
    validar_funcion(f)
    validar_paso(h)
    if not isinstance(puntos, int) or isinstance(puntos, bool) or puntos < 2:
        raise EntradaInvalidaError("'puntos' debe ser un entero mayor o igual a 2.")
    if puntos > 15:
        raise EntradaInvalidaError(
            "Use como máximo 15 puntos para evitar mal condicionamiento."
        )
    if alineacion not in {"centrada", "adelante", "atras"}:
        raise EntradaInvalidaError("'alineacion' debe ser centrada, adelante o atras.")
    if alineacion == "centrada":
        if puntos % 2 == 0:
            raise EntradaInvalidaError(
                "Una plantilla centrada requiere un número impar de puntos."
            )
        mitad = puntos // 2
        desplazamientos = list(range(-mitad, mitad + 1))
    elif alineacion == "adelante":
        desplazamientos = list(range(puntos))
    else:
        desplazamientos = list(range(-(puntos - 1), 1))

    matriz = [[float(t) ** k for t in desplazamientos] for k in range(puntos)]
    termino = [0.0] * puntos
    termino[1] = 1.0
    pesos = _resolver_sistema(matriz, termino)
    nodos = [x + h * t for t in desplazamientos]
    valores = [f(nodo) for nodo in nodos]
    aproximacion = sum(w * valor for w, valor in zip(pesos, valores)) / h
    return {
        "derivada": aproximacion,
        "puntos": puntos,
        "alineacion": alineacion,
        "orden de truncamiento": f"O(h^{puntos - 1})",
        "nodos": nodos,
        "pesos": pesos,
        "evaluaciones": valores,
    }
