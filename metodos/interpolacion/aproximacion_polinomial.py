"""Aproximación polinómica por mínimos cuadrados.

Generaliza la regresión lineal a un polinomio de grado m:

    p(x) = c0 + c1·x + c2·x^2 + ... + cm·x^m

Los coeficientes se obtienen resolviendo el sistema de ecuaciones normales
(de tamaño (m+1)×(m+1)) mediante eliminación gaussiana con pivoteo parcial.
El solver se incluye localmente para que el módulo de interpolación sea
autocontenido y no dependa del módulo de matrices.

Complejidad: O(n·m) para armar las ecuaciones normales + O(m^3) para
resolver el sistema.
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_misma_longitud,
    validar_no_vacia,
)


def _resolver_sistema(matriz: list[list[float]], vector: list[float]) -> list[float]:
    """Resuelve A·c = b por eliminación gaussiana con pivoteo parcial.

    Helper privado para las ecuaciones normales; A es cuadrada y pequeña.

    Raises:
        EntradaInvalidaError: Si el sistema es singular (mal condicionado).
    """
    n = len(vector)
    # Matriz aumentada [A | b] con copias para no mutar la entrada.
    a = [list(fila) + [vector[i]] for i, fila in enumerate(matriz)]

    for col in range(n):
        # Pivoteo parcial: fila con mayor |valor| en la columna actual.
        pivote = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivote][col]) < 1e-15:
            raise EntradaInvalidaError(
                "Sistema de ecuaciones normales singular: revise los datos "
                "o reduzca el grado del polinomio."
            )
        a[col], a[pivote] = a[pivote], a[col]

        for fila in range(col + 1, n):
            factor = a[fila][col] / a[col][col]
            for k in range(col, n + 1):
                a[fila][k] -= factor * a[col][k]

    # Sustitución hacia atrás.
    solucion = [0.0] * n
    for fila in range(n - 1, -1, -1):
        acumulado = a[fila][n] - sum(
            a[fila][k] * solucion[k] for k in range(fila + 1, n)
        )
        solucion[fila] = acumulado / a[fila][fila]
    return solucion


def aproximacion_polinomial(
    x_datos: list[float], y_datos: list[float], grado: int
) -> dict:
    """Ajusta un polinomio de grado `grado` por mínimos cuadrados.

    Args:
        x_datos: Coordenadas x observadas.
        y_datos: Coordenadas y observadas, misma longitud que `x_datos`.
        grado: Grado del polinomio (>= 1). Debe cumplirse
            ``grado + 1 <= número de puntos``.

    Returns:
        Diccionario con:
            - ``coeficientes`` (list[float]): ``[c0, c1, ..., cm]`` en orden
              ascendente de potencias de x.
            - ``grado`` (int): Grado ajustado.
            - ``r2`` (float): Coeficiente de determinación R².

    Raises:
        EntradaInvalidaError: Si las entradas son inválidas, hay puntos
            insuficientes para el grado pedido o el sistema es singular.

    Example:
        >>> # Datos exactos de y = x^2 -> ajuste cuadrático perfecto
        >>> r = aproximacion_polinomial([0, 1, 2, 3], [0, 1, 4, 9], grado=2)
        >>> [round(c, 4) + 0.0 for c in r["coeficientes"]]
        [0.0, 0.0, 1.0]
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_entero_positivo(grado, "grado")

    n = len(x_datos)
    if grado + 1 > n:
        raise EntradaInvalidaError(
            f"Para grado {grado} se requieren al menos {grado + 1} puntos, "
            f"se recibieron {n}."
        )

    # Sumas de potencias de x: S_k = Σ x_i^k para k = 0..2·grado.
    potencias = [sum(x**k for x in x_datos) for k in range(2 * grado + 1)]
    # Lado derecho: T_k = Σ y_i · x_i^k para k = 0..grado.
    derecho = [
        sum(y * (x**k) for x, y in zip(x_datos, y_datos)) for k in range(grado + 1)
    ]
    # Matriz normal (grado+1)×(grado+1): A[i][j] = S_{i+j}.
    matriz = [[potencias[i + j] for j in range(grado + 1)] for i in range(grado + 1)]

    coeficientes = _resolver_sistema(matriz, derecho)

    media_y = sum(y_datos) / n
    ss_total = sum((y - media_y) ** 2 for y in y_datos)
    ss_residual = sum(
        (y - _evaluar(coeficientes, x)) ** 2 for x, y in zip(x_datos, y_datos)
    )
    r2 = 1.0 if ss_total == 0 else 1 - ss_residual / ss_total

    return {"coeficientes": coeficientes, "grado": grado, "r2": r2}


def _evaluar(coeficientes: list[float], x: float) -> float:
    """Evalúa un polinomio dado en orden ascendente de potencias (Horner)."""
    resultado = 0.0
    for coef in reversed(coeficientes):
        resultado = resultado * x + coef
    return resultado


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.aproximacion_polinomial import aproximacion_polinomial
#
# # Entrada: datos de y = x^2; ajuste de grado 2
# r = aproximacion_polinomial([0, 1, 2, 3], [0, 1, 4, 9], grado=2)
# r["coeficientes"]   # Salida: [0.0, 0.0, 1.0]  -> p(x) = x^2
# r["r2"]             # Salida: 1.0
