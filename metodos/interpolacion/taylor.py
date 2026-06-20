"""Polinomio de Taylor.

Aproxima una función alrededor de un punto x0 usando sus derivadas
sucesivas evaluadas en x0:

    T(x) = Σ_{k=0}^{n} f^(k)(x0) / k! · (x - x0)^k

La función recibe la lista de derivadas ``[f(x0), f'(x0), f''(x0), ...]``
(la lógica numérica de obtener esas derivadas corresponde al módulo de
derivación, manteniendo separadas las responsabilidades).

Complejidad: O(n) para construir coeficientes y O(n) por evaluación.
"""

from __future__ import annotations

from math import factorial

from utils.validaciones import validar_no_vacia


def taylor(derivadas: list[float], x0: float, x_evaluar: float | None = None) -> dict:
    """Construye el polinomio de Taylor y opcionalmente lo evalúa.

    Args:
        derivadas: Lista ``[f(x0), f'(x0), ..., f^(n)(x0)]``. Su longitud
            determina el grado del polinomio (grado = len - 1).
        x0: Punto alrededor del cual se centra la aproximación.
        x_evaluar: Punto donde evaluar el polinomio; si es None solo se
            devuelven los coeficientes.

    Returns:
        Diccionario con:
            - ``coeficientes`` (list[float]): Coeficientes de Taylor
              ``f^(k)(x0)/k!`` para k = 0..n (potencias de (x - x0)).
            - ``grado`` (int): Grado del polinomio.
            - ``valor`` (float | None): Evaluación en `x_evaluar`, o None.

    Raises:
        EntradaInvalidaError: Si `derivadas` está vacía o no es secuencia.

    Example:
        >>> # e^x en x0=0: derivadas todas 1 -> T(x)=1+x+x^2/2+x^3/6
        >>> r = taylor([1, 1, 1, 1], x0=0, x_evaluar=1)
        >>> round(r["valor"], 6)
        2.666667
    """
    validar_no_vacia(derivadas, "derivadas")

    coeficientes = [derivadas[k] / factorial(k) for k in range(len(derivadas))]

    valor = None
    if x_evaluar is not None:
        valor = evaluar_taylor(coeficientes, x0, x_evaluar)

    return {
        "coeficientes": coeficientes,
        "grado": len(derivadas) - 1,
        "valor": valor,
    }


def evaluar_taylor(coeficientes: list[float], x0: float, x_evaluar: float) -> float:
    """Evalúa el polinomio de Taylor por Horner en potencias de (x - x0).

    Args:
        coeficientes: Coeficientes de Taylor (de ``taylor``).
        x0: Centro de la expansión.
        x_evaluar: Punto de evaluación.

    Returns:
        Valor del polinomio en `x_evaluar`.
    """
    desplazado = x_evaluar - x0
    resultado = 0.0
    for coef in reversed(coeficientes):
        resultado = resultado * desplazado + coef
    return resultado


# --- Ejemplos de entrada y salida (comentados) --------------------------
# from metodos.interpolacion.taylor import taylor
#
# # Aproximar e^x con grado 3 alrededor de 0 (derivadas de e^x = 1):
# r = taylor([1, 1, 1, 1], x0=0, x_evaluar=1)
# r["valor"]         # Salida: 2.6666... (aprox. de e ≈ 2.71828)
# r["coeficientes"]  # Salida: [1.0, 1.0, 0.5, 0.16666...]
