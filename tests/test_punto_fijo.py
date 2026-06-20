"""Pruebas unitarias del método de iteración de punto fijo."""

from __future__ import annotations

import math

import pytest

from metodos.raices.punto_fijo import punto_fijo
from utils.errores import EntradaInvalidaError


def test_punto_fijo_coseno() -> None:
    """x = cos(x) debe converger al punto fijo de Dottie (~0.739085)."""
    resultado = punto_fijo(math.cos, x0=0.5)
    assert resultado["raiz"] == pytest.approx(0.7390851, abs=1e-4)
    assert resultado["convergio"] is True


def test_punto_fijo_estructura() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = punto_fijo(lambda x: (x + 2 / x) / 2, x0=1.0)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado
    # g(x) = (x + 2/x)/2 converge a sqrt(2).
    assert resultado["raiz"] == pytest.approx(math.sqrt(2), abs=1e-6)


def test_punto_fijo_funcion_invalida() -> None:
    """Debe rechazar un argumento no invocable."""
    with pytest.raises(EntradaInvalidaError):
        punto_fijo(42, x0=0.5)  # type: ignore[arg-type]


def test_punto_fijo_tolerancia_invalida() -> None:
    """Debe rechazar tolerancia no positiva."""
    with pytest.raises(EntradaInvalidaError):
        punto_fijo(math.cos, x0=0.5, tolerancia=-1)
