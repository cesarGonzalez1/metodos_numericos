"""Regresión lineal múltiple por mínimos cuadrados (U-V 5.1.3).

Ajusta un modelo lineal en varias variables independientes

    y = b_0 + b_1·x_1 + b_2·x_2 + ... + b_p·x_p

minimizando la suma de cuadrados de los residuos. Resuelve las ecuaciones
normales Xᵀ·X·b = Xᵀ·y, donde X es la matriz de diseño con una primera
columna de unos (para el término independiente b_0).

Complejidad: O(n·p² + p³).
"""

from __future__ import annotations

from metodos.matrices.inversa import inversa
from utils.errores import EntradaInvalidaError
from utils.validaciones import validar_misma_longitud, validar_no_vacia


def _transpuesta(m: list[list[float]]) -> list[list[float]]:
    """Transpone una matriz rectangular."""
    return [list(col) for col in zip(*m)]


def _producto(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    """Producto matricial A·B."""
    bt = _transpuesta(b)
    return [[sum(x * y for x, y in zip(fila, col)) for col in bt] for fila in a]


def _matvec(a: list[list[float]], v: list[float]) -> list[float]:
    """Producto matriz-vector A·v."""
    return [sum(x * y for x, y in zip(fila, v)) for fila in a]


def regresion_multiple(x_datos: list[list[float]], y_datos: list[float]) -> dict:
    """Ajusta y = b0 + b1·x1 + ... + bp·xp por mínimos cuadrados.

    Args:
        x_datos: Lista de observaciones; cada observación es una lista con
            los ``p`` valores de las variables independientes
            (``x_datos[i] = [x1_i, x2_i, ..., xp_i]``).
        y_datos: Valores observados de la respuesta (longitud n).

    Returns:
        Diccionario con:
            - ``coeficientes`` (list[float]): ``[b0, b1, ..., bp]``.
            - ``r2`` (float): Coeficiente de determinación R².
            - ``predichos`` (list[float]): Valores ajustados ŷ_i.

    Raises:
        EntradaInvalidaError: Si las entradas son inválidas, hay menos
            observaciones que parámetros o el sistema normal es singular
            (colinealidad).

    Example:
        >>> # y = 1 + 2·x1 + 3·x2 (datos exactos)
        >>> X = [[1, 1], [2, 1], [1, 2], [3, 2]]
        >>> y = [1 + 2 * a + 3 * b for a, b in X]
        >>> r = regresion_multiple(X, y)
        >>> [round(c, 4) for c in r["coeficientes"]]
        [1.0, 2.0, 3.0]
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    n = len(x_datos)
    p = len(x_datos[0])
    for fila in x_datos:
        if len(fila) != p:
            raise EntradaInvalidaError(
                "Todas las observaciones deben tener el mismo número de "
                "variables independientes."
            )
    if n < p + 1:
        raise EntradaInvalidaError(
            f"Se requieren al menos {p + 1} observaciones para ajustar "
            f"{p} variables más el término independiente; se recibieron {n}."
        )

    # Matriz de diseño X con columna de unos al frente.
    X = [[1.0] + [float(v) for v in fila] for fila in x_datos]
    y = [float(v) for v in y_datos]

    Xt = _transpuesta(X)
    XtX = _producto(Xt, X)
    Xty = _matvec(Xt, y)

    try:
        inv = inversa(XtX)["inversa"]
    except EntradaInvalidaError as exc:
        raise EntradaInvalidaError(
            "El sistema de ecuaciones normales es singular: las variables "
            "independientes podrían ser colineales."
        ) from exc

    coeficientes = _matvec(inv, Xty)

    predichos = [
        coeficientes[0] + sum(coeficientes[j + 1] * fila[j] for j in range(p))
        for fila in x_datos
    ]
    media_y = sum(y) / n
    ss_total = sum((yi - media_y) ** 2 for yi in y)
    ss_residual = sum((yi - pi) ** 2 for yi, pi in zip(y, predichos))
    r2 = 1.0 if ss_total == 0 else 1 - ss_residual / ss_total

    return {"coeficientes": coeficientes, "r2": r2, "predichos": predichos}


# --- Ejemplos comentados ------------------------------------------------
# from metodos.interpolacion.regresion_multiple import regresion_multiple
#
# X = [[1, 1], [1, 2], [2, 2], [2, 3], [3, 3]]
# y = [6, 9, 11, 14, 16]
# regresion_multiple(X, y)["coeficientes"]
