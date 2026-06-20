"""Pruebas unitarias del método de Müller."""

from __future__ import annotations

import pytest

from metodos.raices.muller import muller
from utils.errores import EntradaInvalidaError


def test_muller_raiz_real() -> None:
    """Debe encontrar la raíz real de x^3 - x^2 + x - 1  ->  1.0."""
    resultado = muller(lambda x: x**3 - x**2 + x - 1, 0, 0.5, 1.5)
    assert resultado["raiz"].real == pytest.approx(1.0, abs=1e-5)
    assert abs(resultado["raiz"].imag) < 1e-5
    assert resultado["convergio"] is True


def test_muller_raiz_compleja() -> None:
    """Debe encontrar una raíz compleja de x^2 + 1  ->  +/- i."""
    resultado = muller(lambda x: x**2 + 1, 0j, 0.5j, 1j)
    assert abs(resultado["raiz"] - 1j) == pytest.approx(0.0, abs=1e-4)


def test_muller_estructura() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = muller(lambda x: x**2 - 2, 0, 1, 2)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado


def test_muller_iniciales_repetidos_lanza_error() -> None:
    """Debe rechazar aproximaciones iniciales no distintas."""
    with pytest.raises(EntradaInvalidaError):
        muller(lambda x: x**2 - 2, 1, 1, 2)
