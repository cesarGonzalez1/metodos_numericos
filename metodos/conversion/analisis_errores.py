"""Errores de representación, redondeo y truncamiento (U-I 1.1.2).

Las rutinas de este módulo distinguen el valor de referencia ``x`` de una
aproximación ``x_a`` y reportan los errores absoluto, relativo y porcentual:

    E_a = |x - x_a|,    E_r = E_a / |x|,    E_% = 100 E_r.

Para ``x = 0`` el error relativo no está definido; se devuelve ``None`` en
lugar de ocultar la indeterminación con una división artificial.
"""

from __future__ import annotations

import math

from utils.errores import EntradaInvalidaError


def analisis_errores(valor_verdadero: float, valor_aproximado: float) -> dict:
    """Calcula errores absoluto, relativo y porcentual de una aproximación."""
    try:
        verdadero = float(valor_verdadero)
        aproximado = float(valor_aproximado)
    except (TypeError, ValueError) as exc:
        raise EntradaInvalidaError("Los valores deben ser números reales.") from exc
    if not math.isfinite(verdadero) or not math.isfinite(aproximado):
        raise EntradaInvalidaError("Los valores deben ser finitos.")

    error_absoluto = abs(verdadero - aproximado)
    if verdadero == 0.0:
        error_relativo = None
        error_porcentual = None
        cifras = None
    else:
        error_relativo = error_absoluto / abs(verdadero)
        error_porcentual = 100.0 * error_relativo
        if error_relativo == 0.0:
            cifras = "todas las representables"
        else:
            # Criterio usual: E_r <= 0.5 * 10^{-n} garantiza n cifras.
            cifras = max(0, math.floor(-math.log10(2.0 * error_relativo)))

    return {
        "valor verdadero": verdadero,
        "valor aproximado": aproximado,
        "error absoluto": error_absoluto,
        "error relativo": error_relativo,
        "error porcentual": error_porcentual,
        "cifras significativas garantizadas": cifras,
    }


def redondeo_y_truncamiento(numero: float, decimales: int = 3) -> dict:
    """Compara redondeo y truncamiento decimal de ``numero``.

    El truncamiento se realiza hacia cero, que es la convención numérica
    habitual. El redondeo usa ``round`` de Python (empates al par), coherente
    con IEEE 754 y con la reducción del sesgo acumulado.
    """
    try:
        valor = float(numero)
    except (TypeError, ValueError) as exc:
        raise EntradaInvalidaError("'numero' debe ser un real.") from exc
    if not math.isfinite(valor):
        raise EntradaInvalidaError("'numero' debe ser finito.")
    if not isinstance(decimales, int) or isinstance(decimales, bool) or decimales < 0:
        raise EntradaInvalidaError("'decimales' debe ser un entero mayor o igual a 0.")
    if decimales > 15:
        raise EntradaInvalidaError(
            "Use como máximo 15 decimales para un float de 64 bits."
        )

    factor = 10**decimales
    truncado = math.trunc(valor * factor) / factor
    redondeado = round(valor, decimales)
    return {
        "numero original": valor,
        "decimales": decimales,
        "redondeado (empates al par)": redondeado,
        "error absoluto de redondeo": abs(valor - redondeado),
        "truncado (hacia cero)": truncado,
        "error absoluto de truncamiento": abs(valor - truncado),
    }
