"""Regresión no lineal por linealización (U-V 5.1.5).

Ajusta modelos no lineales que pueden transformarse en lineales aplicando
logaritmos, y luego se resuelven con mínimos cuadrados ordinarios:

* Exponencial:  y = a·e^{b·x}   ⇒   ln y = ln a + b·x
* Potencia:     y = a·x^b       ⇒   ln y = ln a + b·ln x

Tras ajustar la recta sobre los datos transformados se recuperan los
parámetros originales (a = e^{intercepto}). El R² se reporta sobre la
escala **original** (no la transformada), que es lo relevante para evaluar
el ajuste del modelo no lineal.
"""

from __future__ import annotations

import math

from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_misma_longitud, validar_no_vacia

MODELOS = ("exponencial", "potencia")


def regresion_no_lineal(
    x_datos: list[float], y_datos: list[float], modelo: str = "exponencial"
) -> dict:
    """Ajusta un modelo exponencial o potencia por linealización.

    Args:
        x_datos: Coordenadas x observadas.
        y_datos: Coordenadas y observadas (deben ser > 0 para tomar ln).
        modelo: ``"exponencial"`` (y = a·e^{b·x}) o ``"potencia"``
            (y = a·x^b; requiere además x > 0).

    Returns:
        Diccionario con:
            - ``modelo`` (str): Modelo ajustado.
            - ``a`` (float), ``b`` (float): Parámetros del modelo.
            - ``ecuacion`` (str): Forma legible del modelo ajustado.
            - ``r2`` (float): Coeficiente de determinación en escala original.

    Raises:
        EntradaInvalidaError: Si las entradas son inválidas, el modelo no es
            reconocido o los datos no permiten aplicar el logaritmo
            (y <= 0, o x <= 0 en el modelo potencia).

    Example:
        >>> # y = 2·e^{0.5 x} (datos exactos)
        >>> import math
        >>> xs = [0, 1, 2, 3]
        >>> ys = [2 * math.exp(0.5 * x) for x in xs]
        >>> r = regresion_no_lineal(xs, ys, "exponencial")
        >>> round(r["a"], 4), round(r["b"], 4)
        (2.0, 0.5)
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    if modelo not in MODELOS:
        raise EntradaInvalidaError(
            f"Modelo no reconocido: '{modelo}'. Use {' o '.join(MODELOS)}."
        )
    if len(x_datos) < 2:
        raise EntradaInvalidaError("Se requieren al menos 2 puntos.")
    if any(y <= 0 for y in y_datos):
        raise EntradaInvalidaError(
            "La regresión por linealización requiere y > 0 (se aplica ln y)."
        )
    if modelo == "potencia" and any(x <= 0 for x in x_datos):
        raise EntradaInvalidaError(
            "El modelo potencia requiere x > 0 (se aplica ln x)."
        )

    # Variables transformadas (X, Y) según el modelo.
    if modelo == "exponencial":
        xs = list(x_datos)
    else:  # potencia
        xs = [math.log(x) for x in x_datos]
    ys = [math.log(y) for y in y_datos]

    n = len(xs)
    suma_x = sum(xs)
    suma_y = sum(ys)
    suma_xy = sum(x * y for x, y in zip(xs, ys))
    suma_xx = sum(x * x for x in xs)
    denom = n * suma_xx - suma_x**2
    if denom == 0:
        raise EntradaInvalidaError(
            "No se puede ajustar: todos los valores de x transformados son iguales."
        )

    b = (n * suma_xy - suma_x * suma_y) / denom
    intercepto = (suma_y - b * suma_x) / n
    a = math.exp(intercepto)

    # R² en escala original.
    if modelo == "exponencial":

        def modelo_eval(x: float) -> float:
            return a * math.exp(b * x)

        ecuacion = f"y = {a:.6g}·e^({b:.6g}·x)"
    else:

        def modelo_eval(x: float) -> float:
            return a * x**b

        ecuacion = f"y = {a:.6g}·x^({b:.6g})"

    media_y = sum(y_datos) / len(y_datos)
    ss_total = sum((y - media_y) ** 2 for y in y_datos)
    ss_residual = sum((y - modelo_eval(x)) ** 2 for x, y in zip(x_datos, y_datos))
    r2 = 1.0 if ss_total == 0 else 1 - ss_residual / ss_total

    return {"modelo": modelo, "a": a, "b": b, "ecuacion": ecuacion, "r2": r2}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.regresion_no_lineal import regresion_no_lineal
#
# # Modelo potencia y = 3·x^2
# regresion_no_lineal([1, 2, 3, 4], [3, 12, 27, 48], "potencia")
