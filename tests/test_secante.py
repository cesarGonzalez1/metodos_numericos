"""Pruebas unitarias del método de la secante."""

from __future__ import annotations

import math

import pytest

from metodos.raices.secante import secante
from utils.errores import EntradaInvalidaError


def test_secante_raiz_cuadrada_de_dos() -> None:
    """Debe converger a sqrt(2) para f(x) = x^2 - 2."""
    resultado = secante(lambda x: x**2 - 2, x0=1, x1=2)
    assert resultado["raiz"] == pytest.approx(math.sqrt(2), abs=1e-6)
    assert resultado["convergio"] is True


def test_secante_estructura() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = secante(lambda x: x**3 - x - 2, x0=1, x1=2)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado


def test_secante_iniciales_iguales_lanza_error() -> None:
    """Debe rechazar x0 == x1."""
    with pytest.raises(EntradaInvalidaError):
        secante(lambda x: x - 1, x0=1, x1=1)


def test_secante_funcion_invalida() -> None:
    """Debe rechazar una f no invocable."""
    with pytest.raises(EntradaInvalidaError):
        secante(None, x0=0, x1=1)  # type: ignore[arg-type]
