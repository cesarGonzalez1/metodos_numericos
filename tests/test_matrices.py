"""Pruebas unitarias de los métodos de álgebra lineal numérica."""

from __future__ import annotations

import pytest

from metodos.matrices.eliminacion_aritmetica import eliminacion_aritmetica
from metodos.matrices.eliminacion_gaussiana import eliminacion_gaussiana
from metodos.matrices.pivoteo_escalado import pivoteo_escalado
from metodos.matrices.pivoteo_parcial import pivoteo_parcial
from utils.errores import EntradaInvalidaError

# Matrices de prueba reutilizables.
A_2X2 = [[2, 1], [1, 3]]
B_2X2 = [3, 4]
SOL_2X2 = [1.0, 1.0]

A_3X3 = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
B_3X3 = [8, -11, -3]
SOL_3X3 = [2.0, 3.0, -1.0]

# Todos los solucionadores deben coincidir en su firma y resultado.
SOLUCIONADORES = [
    eliminacion_gaussiana,
    eliminacion_aritmetica,
    pivoteo_parcial,
    pivoteo_escalado,
]


@pytest.mark.parametrize("resolver", SOLUCIONADORES)
def test_sistema_2x2(resolver) -> None:
    assert resolver(A_2X2, B_2X2) == pytest.approx(SOL_2X2)


@pytest.mark.parametrize("resolver", SOLUCIONADORES)
def test_sistema_3x3(resolver) -> None:
    assert resolver(A_3X3, B_3X3) == pytest.approx(SOL_3X3)


@pytest.mark.parametrize("resolver", SOLUCIONADORES)
def test_dimensiones_incompatibles(resolver) -> None:
    with pytest.raises(EntradaInvalidaError):
        resolver([[1, 2], [3, 4]], [1, 2, 3])


@pytest.mark.parametrize("resolver", SOLUCIONADORES)
def test_no_cuadrada(resolver) -> None:
    with pytest.raises(EntradaInvalidaError):
        resolver([[1, 2, 3], [4, 5, 6]], [1, 2])


def test_pivote_nulo_sin_pivoteo_falla() -> None:
    # Primer pivote 0: la eliminación simple no puede continuar.
    with pytest.raises(EntradaInvalidaError):
        eliminacion_gaussiana([[0, 2], [1, 1]], [4, 3])


def test_pivoteo_parcial_resuelve_pivote_nulo() -> None:
    # El mismo sistema sí lo resuelve el pivoteo parcial.
    assert pivoteo_parcial([[0, 2], [1, 1]], [4, 3]) == pytest.approx([1.0, 2.0])


def test_matriz_singular_detectada() -> None:
    with pytest.raises(EntradaInvalidaError):
        pivoteo_parcial([[1, 2], [2, 4]], [3, 6])
