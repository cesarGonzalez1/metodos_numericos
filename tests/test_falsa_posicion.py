"""Pruebas unitarias del método de falsa posición."""

from __future__ import annotations

import pytest

from metodos.raices.falsa_posicion import falsa_posicion
from utils.errores import EntradaInvalidaError


def test_falsa_posicion_encuentra_raiz() -> None:
    """Debe encontrar la raíz de x^3 - x - 2 en [1, 2]."""
    resultado = falsa_posicion(lambda x: x**3 - x - 2, a=1, b=2)
    assert resultado["raiz"] == pytest.approx(1.5213797, abs=1e-4)
    assert resultado["convergio"] is True


def test_falsa_posicion_estructura() -> None:
    """El resultado debe contener las claves del contrato público."""
    resultado = falsa_posicion(lambda x: x**2 - 4, a=0, b=5)
    for clave in ("raiz", "iteraciones", "convergio", "error", "historial"):
        assert clave in resultado


def test_falsa_posicion_sin_cambio_signo_lanza_error() -> None:
    """Debe rechazar intervalos sin cambio de signo."""
    with pytest.raises(EntradaInvalidaError):
        falsa_posicion(lambda x: x**2 + 1, a=0, b=5)


def test_falsa_posicion_max_iteraciones_invalido() -> None:
    """Debe rechazar max_iteraciones <= 0."""
    with pytest.raises(EntradaInvalidaError):
        falsa_posicion(lambda x: x - 1, a=0, b=2, max_iteraciones=0)
