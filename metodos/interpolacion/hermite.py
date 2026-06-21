"""Interpolación de Hermite (U-V 5.2.3).

Construye el polinomio osculador que coincide con la función **y con su
primera derivada** en cada nodo. Con ``n+1`` nodos y sus derivadas, el
polinomio tiene grado a lo más ``2n+1``.

Se implementa con el esquema de diferencias divididas sobre nodos
duplicados: cada nodo x_i se repite dos veces (z_{2i} = z_{2i+1} = x_i) y la
diferencia dividida de orden 1 entre las dos copias se sustituye por la
derivada f'(x_i), evitando la división por cero.
"""

from __future__ import annotations

from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def hermite(
    x_datos: list[float],
    y_datos: list[float],
    derivadas: list[float],
    x_evaluar: float,
) -> dict:
    """Interpola con el polinomio de Hermite y lo evalúa en ``x_evaluar``.

    Args:
        x_datos: Nodos x distintos (longitud n).
        y_datos: Valores f(x_i) (longitud n).
        derivadas: Valores f'(x_i) (longitud n).
        x_evaluar: Punto donde se evalúa el polinomio de Hermite.

    Returns:
        Diccionario con:
            - ``valor`` (float): H(x_evaluar).
            - ``coeficientes`` (list[float]): Coeficientes de Newton (la
              diagonal de la tabla de diferencias divididas).
            - ``grado`` (int): Grado del polinomio (a lo más 2n-1).

    Raises:
        EntradaInvalidaError: Si las listas están vacías, difieren en
            longitud o hay nodos repetidos.

    Example:
        >>> # f(x)=x^2: f(1)=1,f'(1)=2 ; f(2)=4,f'(2)=4 -> H(1.5)=2.25
        >>> r = hermite([1, 2], [1, 4], [2, 4], 1.5)
        >>> round(r["valor"], 6)
        2.25
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_no_vacia(derivadas, "derivadas")
    validar_misma_longitud(x_datos, y_datos, derivadas)
    validar_sin_duplicados(x_datos, "x_datos")

    n = len(x_datos)
    m = 2 * n
    # Nodos duplicados z y tabla de diferencias divididas Q.
    z = [0.0] * m
    Q = [[0.0] * m for _ in range(m)]

    for i in range(n):
        z[2 * i] = x_datos[i]
        z[2 * i + 1] = x_datos[i]
        Q[2 * i][0] = y_datos[i]
        Q[2 * i + 1][0] = y_datos[i]
        # Diferencia de orden 1 entre copias del mismo nodo = derivada.
        Q[2 * i + 1][1] = derivadas[i]
        if i != 0:
            Q[2 * i][1] = (Q[2 * i][0] - Q[2 * i - 1][0]) / (z[2 * i] - z[2 * i - 1])

    for j in range(2, m):
        for i in range(j, m):
            Q[i][j] = (Q[i][j - 1] - Q[i - 1][j - 1]) / (z[i] - z[i - j])

    coeficientes = [Q[i][i] for i in range(m)]

    # Evaluación con la forma anidada de Newton.
    valor = coeficientes[-1]
    for k in range(m - 2, -1, -1):
        valor = valor * (x_evaluar - z[k]) + coeficientes[k]

    return {"valor": valor, "coeficientes": coeficientes, "grado": m - 1}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.hermite import hermite
#
# # Datos clásicos de Burden (ln x): x=8.3,8.6 con f y f'
# hermite([8.3, 8.6], [17.56492, 18.50515], [3.116256, 3.151762], 8.4)
