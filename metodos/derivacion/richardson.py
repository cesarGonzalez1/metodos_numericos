"""Extrapolación de Richardson para derivación numérica.

Combina aproximaciones de la derivada con pasos cada vez más pequeños
(h, h/2, h/4, ...) para cancelar sistemáticamente los términos de error y
obtener una estimación de orden muy superior. Partiendo de la diferencia
centrada (error O(h^2)), cada columna de la tabla elimina el siguiente
término par del error:

    T[i][j] = (4^j · T[i][j-1] - T[i-1][j-1]) / (4^j - 1)

Complejidad: O(niveles^2) evaluaciones de la fórmula base.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_paso,
)


def richardson(
    f: Callable[[float], float],
    x: float,
    h: float = 0.1,
    niveles: int = 4,
) -> dict:
    """Aproxima f'(x) por extrapolación de Richardson.

    Args:
        f: Función a derivar.
        x: Punto donde se evalúa la derivada.
        h: Tamaño de paso inicial (> 0); se refina dividiéndolo a la mitad.
        niveles: Número de filas de la tabla (>= 1). A mayor número, mayor
            precisión teórica (hasta el límite de la aritmética flotante).

    Returns:
        Diccionario con:
            - ``valor`` (float): Mejor aproximación de f'(x).
            - ``tabla`` (list[list[float]]): Tabla de Richardson, lista para
              mostrarse en la GUI.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable, h <= 0 o niveles <= 0.

    Example:
        >>> r = richardson(lambda x: x**3, 2.0, h=0.1, niveles=4)
        >>> round(r["valor"], 6)
        12.0
    """
    validar_funcion(f)
    validar_paso(h)
    validar_entero_positivo(niveles, "niveles")

    tabla = [[0.0] * niveles for _ in range(niveles)]
    for i in range(niveles):
        paso = h / (2**i)
        tabla[i][0] = (f(x + paso) - f(x - paso)) / (2 * paso)
        for j in range(1, i + 1):
            potencia = 4**j
            tabla[i][j] = (potencia * tabla[i][j - 1] - tabla[i - 1][j - 1]) / (
                potencia - 1
            )

    return {"valor": tabla[niveles - 1][niveles - 1], "tabla": tabla}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.derivacion.richardson import richardson
#
# # f(x)=x^3, f'(2)=12 con alta precisión
# r = richardson(lambda x: x**3, 2.0, h=0.1, niveles=4)
# r["valor"]   # ~12.0
