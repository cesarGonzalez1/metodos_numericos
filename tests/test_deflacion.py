"""Pruebas unitarias de la deflación polinomial."""

from __future__ import annotations

import pytest

from metodos.raices.deflacion import deflacion
from utils.errores import EntradaInvalidaError


def test_deflacion_division_exacta() -> None:
    """x^2 - 3x + 2 entre (x - 1)  ->  cociente x - 2, residuo 0."""
    resultado = deflacion([1, -3, 2], raiz=1)
    assert resultado["cociente"] == pytest.approx([1, -2])
    assert resultado["residuo"] == pytest.approx(0)


def test_deflacion_grado_tres() -> None:
    """x^3 - 6x^2 + 11x - 6 entre (x - 1)  ->  x^2 - 5x + 6."""
    resultado = deflacion([1, -6, 11, -6], raiz=1)
    assert resultado["cociente"] == pytest.approx([1, -5, 6])
    assert resultado["residuo"] == pytest.approx(0)


def test_deflacion_residuo_es_p_de_raiz() -> None:
    """El residuo debe coincidir con P(valor) cuando no es raíz."""
    # P(x) = x^2 + 1, P(2) = 5.
    resultado = deflacion([1, 0, 1], raiz=2)
    assert resultado["residuo"] == pytest.approx(5)


def test_deflacion_coeficiente_principal_cero() -> None:
    """Debe rechazar coeficiente principal nulo."""
    with pytest.raises(EntradaInvalidaError):
        deflacion([0, 1, 2], raiz=1)


def test_deflacion_pocos_coeficientes() -> None:
    """Debe rechazar polinomios de grado 0."""
    with pytest.raises(EntradaInvalidaError):
        deflacion([3], raiz=1)
