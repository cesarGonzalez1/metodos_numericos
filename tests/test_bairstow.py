"""Pruebas unitarias del método de Bairstow."""

from __future__ import annotations

import pytest

from metodos.raices.bairstow import bairstow
from utils.errores import EntradaInvalidaError


def test_bairstow_raices_reales() -> None:
    """x^3 - 6x^2 + 11x - 6  ->  raíces 1, 2, 3."""
    resultado = bairstow([1, -6, 11, -6])
    reales = sorted(z.real for z in resultado["raices"])
    assert reales == pytest.approx([1.0, 2.0, 3.0], abs=1e-4)
    assert resultado["convergio"] is True


def test_bairstow_raices_complejas() -> None:
    """x^2 + 1  ->  raíces +i y -i."""
    resultado = bairstow([1, 0, 1])
    imaginarias = sorted(z.imag for z in resultado["raices"])
    assert imaginarias == pytest.approx([-1.0, 1.0], abs=1e-6)


def test_bairstow_grado_cuatro() -> None:
    """x^4 - 1  ->  raíces 1, -1, +i, -i."""
    resultado = bairstow([1, 0, 0, 0, -1])
    assert len(resultado["raices"]) == 4


def test_bairstow_coeficiente_principal_cero() -> None:
    """Debe rechazar un coeficiente principal nulo."""
    with pytest.raises(EntradaInvalidaError):
        bairstow([0, 1, 2])


def test_bairstow_pocos_coeficientes() -> None:
    """Debe rechazar listas con menos de 2 coeficientes."""
    with pytest.raises(EntradaInvalidaError):
        bairstow([5])
