"""Pruebas unitarias del método de Newton-Raphson."""

from __future__ import annotations

import math

import pytest

from metodos.raices.newton_raphson import newton_raphson
from utils.errores import EntradaInvalidaError


def test_newton_raiz_cuadrada_de_dos() -> None:
    """Debe converger a sqrt(2) para f(x) = x^2 - 2."""
    resultado = newton_raphson(lambda x: x**2 - 2, lambda x: 2 * x, x0=1.5)
    assert resultado["raiz"] == pytest.approx(math.sqrt(2), abs=1e-8)
    assert resultado["convergio"] is True


def test_newton_estructura() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = newton_raphson(lambda x: x - 3, lambda x: 1, x0=0.0)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado


def test_newton_derivada_nula_lanza_error() -> None:
    """Debe lanzar error si la derivada se anula (división por cero)."""
    with pytest.raises(EntradaInvalidaError):
        newton_raphson(lambda x: x**2 + 1, lambda x: 2 * x, x0=0.0)


def test_newton_derivada_no_invocable() -> None:
    """Debe rechazar una derivada no invocable."""
    with pytest.raises(EntradaInvalidaError):
        newton_raphson(lambda x: x, 5, x0=1.0)  # type: ignore[arg-type]
