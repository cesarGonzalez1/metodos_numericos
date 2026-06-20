"""Método de mínimos cuadrados (regresión lineal).

Ajusta la recta y = a + b·x que minimiza la suma de los cuadrados de los
residuos para un conjunto de puntos (x_i, y_i). A diferencia de la
interpolación, la recta no pasa necesariamente por los puntos: busca la
mejor aproximación global.

Complejidad: O(n).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
)


def minimos_cuadrados(x_datos: list[float], y_datos: list[float]) -> dict:
    """Ajusta una recta y = a + b·x por mínimos cuadrados.

    Args:
        x_datos: Coordenadas x observadas.
        y_datos: Coordenadas y observadas, misma longitud que `x_datos`.

    Returns:
        Diccionario con:
            - ``interseccion`` (float): Coeficiente a (ordenada al origen).
            - ``pendiente`` (float): Coeficiente b.
            - ``r2`` (float): Coeficiente de determinación R².
            - ``coeficientes`` (list[float]): ``[a, b]`` (orden ascendente
              en potencias de x), consistente con la aproximación polinómica.

    Raises:
        EntradaInvalidaError: Si las listas están vacías, difieren en
            longitud, hay menos de 2 puntos o todas las x son iguales
            (recta vertical, pendiente indefinida).

    Example:
        >>> r = minimos_cuadrados([0, 1, 2, 3], [1, 3, 5, 7])
        >>> round(r["pendiente"], 4), round(r["interseccion"], 4)
        (2.0, 1.0)
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    n = len(x_datos)
    if n < 2:
        raise EntradaInvalidaError(
            "Se requieren al menos 2 puntos para el ajuste lineal."
        )

    suma_x = sum(x_datos)
    suma_y = sum(y_datos)
    suma_xy = sum(x * y for x, y in zip(x_datos, y_datos))
    suma_xx = sum(x * x for x in x_datos)

    denominador = n * suma_xx - suma_x * suma_x
    if denominador == 0:
        raise EntradaInvalidaError(
            "Todas las abscisas son iguales: la pendiente es indefinida."
        )

    pendiente = (n * suma_xy - suma_x * suma_y) / denominador
    interseccion = (suma_y - pendiente * suma_x) / n

    media_y = suma_y / n
    ss_total = sum((y - media_y) ** 2 for y in y_datos)
    ss_residual = sum(
        (y - (interseccion + pendiente * x)) ** 2 for x, y in zip(x_datos, y_datos)
    )
    r2 = 1.0 if ss_total == 0 else 1 - ss_residual / ss_total

    return {
        "interseccion": interseccion,
        "pendiente": pendiente,
        "r2": r2,
        "coeficientes": [interseccion, pendiente],
    }


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.minimos_cuadrados import minimos_cuadrados
#
# # Entrada: puntos sobre la recta y = 1 + 2x
# r = minimos_cuadrados([0, 1, 2, 3], [1, 3, 5, 7])
# r["pendiente"], r["interseccion"], r["r2"]   # Salida: 2.0, 1.0, 1.0
