"""Deflación polinomial mediante división sintética.

Una vez conocida una raíz r de un polinomio P(x), la deflación reduce su
grado dividiéndolo entre (x - r). El polinomio cociente Q(x) contiene las
raíces restantes, lo que permite buscarlas sobre un problema más pequeño y
evita reconverger a una raíz ya encontrada.

Convención de coeficientes: lista en orden de grado descendente, es decir
``[a_n, ..., a_1, a_0]`` representa a_n*x^n + ... + a_1*x + a_0 (misma
convención que ``numpy.poly1d`` y ``numpy.roots``).
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError


def _validar_coeficientes(coeficientes: list[float]) -> None:
    """Valida que `coeficientes` represente un polinomio de grado >= 1.

    Args:
        coeficientes: Coeficientes en orden de grado descendente.

    Raises:
        EntradaInvalidaError: Si la lista está vacía, tiene menos de 2
            elementos o su coeficiente principal es 0.
    """
    if not isinstance(coeficientes, (list, tuple)):
        raise EntradaInvalidaError("Los coeficientes deben darse como lista o tupla.")
    if len(coeficientes) < 2:
        raise EntradaInvalidaError(
            "Se requieren al menos 2 coeficientes (polinomio de grado >= 1)."
        )
    if coeficientes[0] == 0:
        raise EntradaInvalidaError(
            "El coeficiente principal (primer elemento) no puede ser 0."
        )


def deflacion(coeficientes: list[float], raiz: complex) -> dict:
    """Deflaciona un polinomio dividiéndolo entre (x - raiz).

    Aplica división sintética (regla de Ruffini) para obtener el polinomio
    cociente de grado n-1 y el residuo. Si `raiz` es una raíz exacta, el
    residuo es 0; en la práctica el residuo indica el error de la raíz.

    Args:
        coeficientes: Coeficientes del polinomio en orden de grado
            descendente.
        raiz: Raíz conocida por la que se divide el polinomio.

    Returns:
        Diccionario con las claves:
            - ``cociente`` (list): Coeficientes del polinomio reducido
              (grado n-1), en orden descendente.
            - ``residuo`` (complex/float): Residuo de la división, igual a
              ``P(raiz)``.
            - ``raiz`` (complex/float): La raíz utilizada (eco de entrada).

    Raises:
        EntradaInvalidaError: Si `coeficientes` no es un polinomio válido.

    Example:
        >>> # x^2 - 3x + 2 = (x - 1)(x - 2); deflactar por x = 1
        >>> resultado = deflacion([1, -3, 2], raiz=1)
        >>> resultado["cociente"]
        [1, -2]
        >>> resultado["residuo"]
        0
    """
    _validar_coeficientes(coeficientes)

    cociente: list = [coeficientes[0]]
    for coef in coeficientes[1:]:
        cociente.append(coef + cociente[-1] * raiz)

    residuo = cociente.pop()  # el último valor es el residuo, no del cociente

    return {"cociente": cociente, "residuo": residuo, "raiz": raiz}


# --- Ejemplos de uso (comentados) ---------------------------------------
# from metodos.raices.deflacion import deflacion
#
# # x^3 - 6x^2 + 11x - 6 = (x-1)(x-2)(x-3); deflactar por x = 1
# resultado = deflacion([1, -6, 11, -6], raiz=1)
# resultado["cociente"]   # [1, -5, 6]  ->  x^2 - 5x + 6
# resultado["residuo"]    # 0
#
# # Encadenar deflaciones para reducir el grado paso a paso:
# q1 = deflacion([1, -6, 11, -6], raiz=1)["cociente"]   # [1, -5, 6]
# q2 = deflacion(q1, raiz=2)["cociente"]                # [1, -3]
