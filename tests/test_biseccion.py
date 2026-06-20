"""Pruebas unitarias del método de bisección."""

from __future__ import annotations

import pytest

from metodos.raices.biseccion import biseccion
from utils.errores import EntradaInvalidaError


def test_biseccion_encuentra_raiz_simple() -> None:
    """biseccion() debe encontrar la raíz de f(x) = x^2 - 4 en [0, 5]."""
    resultado = biseccion(lambda x: x**2 - 4, a=0, b=5, tolerancia=1e-8)
    assert resultado["raiz"] == pytest.approx(2.0, abs=1e-4)
    assert resultado["convergio"] is True


def test_biseccion_devuelve_estructura_esperada() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = biseccion(lambda x: x - 1, a=0, b=2)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado
    assert resultado["iteraciones"] == len(resultado["historial"])


def test_biseccion_intervalo_sin_cambio_signo_lanza_error() -> None:
    """Debe rechazar intervalos donde f(a) y f(b) tienen igual signo."""
    with pytest.raises(EntradaInvalidaError):
        biseccion(lambda x: x**2 + 4, a=0, b=5)


def test_biseccion_intervalo_invalido_lanza_error() -> None:
    """Debe rechazar a >= b."""
    with pytest.raises(EntradaInvalidaError):
        biseccion(lambda x: x - 1, a=5, b=0)


def test_biseccion_tolerancia_invalida_lanza_error() -> None:
    """Debe rechazar tolerancia no positiva."""
    with pytest.raises(EntradaInvalidaError):
        biseccion(lambda x: x - 1, a=0, b=2, tolerancia=0)
