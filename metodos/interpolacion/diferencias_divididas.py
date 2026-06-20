"""Interpolación de Newton por diferencias divididas.

Construye la forma de Newton del polinomio interpolante calculando la tabla
de diferencias divididas. Los coeficientes son la diagonal superior de la
tabla y permiten evaluar el polinomio con el esquema anidado de Horner.

Complejidad: O(n^2) para construir la tabla; O(n) por evaluación posterior.
"""

from __future__ import annotations

from utils.validaciones import (
    validar_misma_longitud,
    validar_no_vacia,
    validar_sin_duplicados,
)


def diferencias_divididas(
    x_datos: list[float],
    y_datos: list[float],
    x_evaluar: float | None = None,
) -> dict:
    """Calcula coeficientes de Newton y opcionalmente evalúa el polinomio.

    Args:
        x_datos: Coordenadas x conocidas (sin repetidos).
        y_datos: Coordenadas y conocidas, misma longitud que `x_datos`.
        x_evaluar: Si se proporciona, punto donde evaluar el polinomio; si
            es None solo se devuelven coeficientes y tabla.

    Returns:
        Diccionario con:
            - ``coeficientes`` (list[float]): Coeficientes de Newton
              (diagonal superior de la tabla).
            - ``tabla`` (list[list[float]]): Tabla completa de diferencias
              divididas.
            - ``valor`` (float | None): Evaluación en `x_evaluar`, o None.

    Raises:
        EntradaInvalidaError: Si las listas están vacías, difieren en
            longitud o `x_datos` tiene repetidos.

    Example:
        >>> r = diferencias_divididas([0, 1, 2], [1, 3, 7], x_evaluar=1.5)
        >>> r["coeficientes"]
        [1.0, 2.0, 1.0]
        >>> round(r["valor"], 4)
        4.75
    """
    validar_no_vacia(x_datos, "x_datos")
    validar_no_vacia(y_datos, "y_datos")
    validar_misma_longitud(x_datos, y_datos)
    validar_sin_duplicados(list(x_datos), "x_datos")

    n = len(x_datos)
    tabla = [[0.0] * n for _ in range(n)]
    for i in range(n):
        tabla[i][0] = float(y_datos[i])

    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = (tabla[i + 1][j - 1] - tabla[i][j - 1]) / (
                x_datos[i + j] - x_datos[i]
            )

    coeficientes = [tabla[0][j] for j in range(n)]

    valor = None
    if x_evaluar is not None:
        valor = evaluar_newton(coeficientes, x_datos, x_evaluar)

    return {"coeficientes": coeficientes, "tabla": tabla, "valor": valor}


def evaluar_newton(
    coeficientes: list[float], x_datos: list[float], x_evaluar: float
) -> float:
    """Evalúa el polinomio de Newton (Horner) dados sus coeficientes.

    Args:
        coeficientes: Coeficientes de Newton (de ``diferencias_divididas``).
        x_datos: Nodos x usados para construir los coeficientes.
        x_evaluar: Punto de evaluación.

    Returns:
        Valor del polinomio en `x_evaluar`.
    """
    n = len(coeficientes)
    resultado = coeficientes[n - 1]
    for i in range(n - 2, -1, -1):
        resultado = resultado * (x_evaluar - x_datos[i]) + coeficientes[i]
    return resultado


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.diferencias_divididas import diferencias_divididas
#
# # Entrada: nodos (0,1), (1,3), (2,7)
# r = diferencias_divididas([0, 1, 2], [1, 3, 7], x_evaluar=1.5)
# r["coeficientes"]   # Salida: [1.0, 2.0, 1.0]  -> 1 + 2(x) + 1·x(x-1)
# r["valor"]          # Salida: 4.75
