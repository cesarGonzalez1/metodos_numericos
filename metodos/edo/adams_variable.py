"""Adams predictor-corrector con tamaño de paso variable (U-III 3.4).

En una malla no uniforme los coeficientes constantes 55, -59, ... dejan de
ser válidos. Este módulo calcula en cada paso los pesos integrando los
polinomios cardinales de Lagrange que interpolan ``f(x, y)``:

    y_{n+1} = y_n + sum_j w_j f_j,
    w_j = integral_{x_n}^{x_{n+1}} L_j(x) dx.

Se usa Adams-Bashforth de cuatro datos como predictor y Adams-Moulton de
cuatro datos como corrector. La diferencia predictor-corrector estima el
error local y controla el siguiente paso. Los tres puntos de arranque se
obtienen con RK4 y extrapolación por dos medios pasos.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError
from utils.validaciones import (
    validar_entero_positivo,
    validar_funcion,
    validar_paso,
    validar_tolerancia,
)


def _multiplicar_lineal(coef: list[float], raiz: float) -> list[float]:
    """Multiplica un polinomio ascendente por ``(x - raiz)``."""
    salida = [0.0] * (len(coef) + 1)
    for k, valor in enumerate(coef):
        salida[k] -= raiz * valor
        salida[k + 1] += valor
    return salida


def _pesos_integrados(nodos: list[float], a: float, b: float) -> list[float]:
    """Integra las bases cardinales de Lagrange sobre ``[a, b]``."""
    ancho = b - a
    if ancho <= 0:
        raise EntradaInvalidaError("El paso de integración debe ser positivo.")
    # Coordenada local t=(x-a)/(b-a): evita cancelar potencias grandes cuando
    # x está lejos del origen. Al final dx = ancho·dt.
    nodos_locales = [(x - a) / ancho for x in nodos]
    pesos: list[float] = []
    for j, xj in enumerate(nodos_locales):
        polinomio = [1.0]
        denominador = 1.0
        for m, xm in enumerate(nodos_locales):
            if m == j:
                continue
            diferencia = xj - xm
            if abs(diferencia) < 1e-15:
                raise EntradaInvalidaError(
                    "La historia de Adams contiene nodos repetidos."
                )
            polinomio = _multiplicar_lineal(polinomio, xm)
            denominador *= diferencia
        integral_local = sum(c / (k + 1) for k, c in enumerate(polinomio))
        pesos.append(ancho * integral_local / denominador)
    return pesos


def _rk4_paso(
    f: Callable[[float, float], float], x: float, y: float, h: float
) -> float:
    k1 = f(x, y)
    k2 = f(x + h / 2.0, y + h * k1 / 2.0)
    k3 = f(x + h / 2.0, y + h * k2 / 2.0)
    k4 = f(x + h, y + h * k3)
    return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0


def adams_variable(
    f: Callable[[float, float], float],
    x0: float,
    y0: float,
    x_final: float,
    tolerancia: float = 1e-6,
    h_inicial: float = 0.1,
    h_min: float = 1e-8,
    h_max: float = 0.5,
    max_pasos: int = 100000,
) -> dict:
    """Resuelve ``y'=f(x,y)`` con Adams de cuarto orden y paso adaptativo.

    La integración es hacia adelante. ``tolerancia`` controla el error local
    absoluto estimado; los pasos rechazados se conservan en ``historial``
    para que el usuario pueda auditar el proceso.
    """
    validar_funcion(f)
    validar_tolerancia(tolerancia)
    validar_paso(h_inicial, "h_inicial")
    validar_paso(h_min, "h_min")
    validar_paso(h_max, "h_max")
    validar_entero_positivo(max_pasos, "max_pasos")
    if x_final <= x0:
        raise EntradaInvalidaError("x_final debe ser mayor que x0.")
    if h_min > h_inicial or h_inicial > h_max:
        raise EntradaInvalidaError("Se requiere h_min <= h_inicial <= h_max.")

    solucion: list[tuple[float, float]] = [(float(x0), float(y0))]
    efes = [f(float(x0), float(y0))]
    historial: list[dict] = []
    h = min(h_inicial, x_final - x0)
    intentos = 0
    rechazados = 0

    while solucion[-1][0] < x_final and intentos < max_pasos:
        intentos += 1
        x, y = solucion[-1]
        h = min(h, x_final - x)
        x_sig = x + h

        if len(solucion) < 4:
            y_completo = _rk4_paso(f, x, y, h)
            y_medio = _rk4_paso(f, x, y, h / 2.0)
            y_dos_medios = _rk4_paso(f, x + h / 2.0, y_medio, h / 2.0)
            error = abs(y_dos_medios - y_completo) / 15.0
            y_nuevo = y_dos_medios + (y_dos_medios - y_completo) / 15.0
            metodo = "arranque RK4"
        else:
            xs_pred = [p[0] for p in solucion[-4:]][::-1]
            fs_pred = efes[-4:][::-1]
            pesos_pred = _pesos_integrados(xs_pred, x, x_sig)
            y_pred = y + sum(w * fj for w, fj in zip(pesos_pred, fs_pred))

            xs_corr = [x_sig] + xs_pred[:3]
            pesos_corr = _pesos_integrados(xs_corr, x, x_sig)
            y_corr = y_pred
            for _ in range(8):
                fs_corr = [f(x_sig, y_corr)] + fs_pred[:3]
                siguiente = y + sum(w * fj for w, fj in zip(pesos_corr, fs_corr))
                if abs(siguiente - y_corr) <= max(tolerancia * 0.1, 1e-14):
                    y_corr = siguiente
                    break
                y_corr = siguiente
            error = abs(y_corr - y_pred) / 15.0
            y_nuevo = y_corr
            metodo = "Adams ABM4 variable"

        aceptado = error <= tolerancia
        historial.append(
            {
                "intento": intentos,
                "x": x_sig,
                "h": h,
                "y": y_nuevo,
                "error": error,
                "aceptado": aceptado,
                "metodo": metodo,
            }
        )
        if aceptado:
            solucion.append((x_sig, y_nuevo))
            efes.append(f(x_sig, y_nuevo))
        else:
            rechazados += 1

        if error == 0.0:
            factor = 2.0
        else:
            factor = 0.9 * (tolerancia / error) ** 0.2
            factor = min(2.0, max(0.2, factor))
        h_nuevo = min(h_max, h * factor)
        if h_nuevo < h_min:
            if not aceptado:
                raise EntradaInvalidaError(
                    "No se alcanza la tolerancia sin reducir el paso por "
                    "debajo de h_min."
                )
            h_nuevo = h_min
        h = h_nuevo

    if solucion[-1][0] < x_final:
        raise EntradaInvalidaError("Se alcanzó max_pasos antes de llegar a x_final.")
    return {
        "solucion": solucion,
        "pasos aceptados": len(solucion) - 1,
        "pasos rechazados": rechazados,
        "error local máximo aceptado": max(
            (fila["error"] for fila in historial if fila["aceptado"]), default=0.0
        ),
        "historial": historial,
    }
