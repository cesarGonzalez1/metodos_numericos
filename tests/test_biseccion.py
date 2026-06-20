"""Pruebas de ejemplo para el método de bisección.

Plantilla: este archivo muestra la estructura esperada de un test. Está
marcado con `xfail` porque `biseccion()` aún no está implementado
(lanza `NotImplementedError`). Quien implemente el método debe quitar el
marcador `xfail` y completar/ajustar los casos de prueba reales.
"""

from __future__ import annotations

import pytest

from metodos.raices.biseccion import biseccion


@pytest.mark.xfail(
    reason="Pendiente de implementar por el equipo.", raises=NotImplementedError
)
def test_biseccion_encuentra_raiz_simple() -> None:
    """biseccion() debe encontrar la raíz de f(x) = x^2 - 4 en [0, 5]."""
    resultado = biseccion(lambda x: x**2 - 4, a=0, b=5, tolerancia=1e-6)
    assert resultado["raiz"] == pytest.approx(2.0, abs=1e-4)


@pytest.mark.xfail(
    reason="Pendiente de implementar por el equipo.", raises=NotImplementedError
)
def test_biseccion_intervalo_sin_cambio_signo_lanza_error() -> None:
    """biseccion() debe rechazar intervalos donde f(a) y f(b) tienen igual signo."""
    with pytest.raises(ValueError):
        biseccion(lambda x: x**2 + 4, a=0, b=5)
