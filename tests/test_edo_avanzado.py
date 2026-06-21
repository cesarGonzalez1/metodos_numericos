"""Pruebas de métodos multipaso y sistemas de EDO (U-III 3.4-3.5)."""

from __future__ import annotations

import math

import pytest

from metodos.edo.adams import adams
from metodos.edo.sistemas import orden_superior, resolver_sistema
from utils.errores import EntradaInvalidaError

E = math.e


# --- Adams-Bashforth-Moulton --------------------------------------------
def test_adams_exponencial() -> None:
    r = adams(lambda x, y: y, 0, 1, 1, n=20)
    assert r["solucion"][-1][1] == pytest.approx(E, abs=1e-4)
    assert len(r["solucion"]) == 21


def test_adams_lineal() -> None:
    # dy/dx = x - y, y(0)=1 -> y = x - 1 + 2 e^{-x}
    r = adams(lambda x, y: x - y, 0, 1, 2, n=40)
    exacto = 2 - 1 + 2 * math.exp(-2)
    assert r["solucion"][-1][1] == pytest.approx(exacto, abs=1e-5)


def test_adams_n_insuficiente() -> None:
    with pytest.raises(EntradaInvalidaError):
        adams(lambda x, y: y, 0, 1, 1, n=3)


def test_adams_x_final_igual_x0() -> None:
    with pytest.raises(EntradaInvalidaError):
        adams(lambda x, y: y, 0, 1, 0)


# --- Sistemas de EDO (RK4 vectorial) ------------------------------------
def test_sistema_oscilador() -> None:
    # y1' = y2, y2' = -y1, y(0)=(0,1) -> y1 = sin x, y2 = cos x
    f = lambda x, y: [y[1], -y[0]]  # noqa: E731
    r = resolver_sistema(f, 0, [0.0, 1.0], math.pi / 2, n=400)
    assert r["columnas"][0][-1] == pytest.approx(1.0, abs=1e-4)
    assert r["columnas"][1][-1] == pytest.approx(0.0, abs=1e-4)


def test_sistema_dimension_incorrecta() -> None:
    # La función devuelve menos componentes de las esperadas.
    with pytest.raises(EntradaInvalidaError):
        resolver_sistema(lambda x, y: [y[0]], 0, [1.0, 2.0], 1, n=10)


def test_sistema_y0_vacio() -> None:
    with pytest.raises(EntradaInvalidaError):
        resolver_sistema(lambda x, y: [], 0, [], 1)


# --- Ecuaciones de orden superior ---------------------------------------
def test_orden_superior_armonico() -> None:
    # y'' = -y, y(0)=0, y'(0)=1 -> y = sin x
    r = orden_superior(lambda x, y, dy: -y, 0, [0, 1], math.pi / 2, n=400)
    assert r["columnas"][0][-1] == pytest.approx(1.0, abs=1e-4)


def test_orden_superior_lineal() -> None:
    # y'' - y' - 2y = 0, y(0)=1, y'(0)=0 -> y = (2 e^{-x} + e^{2x}) / 3
    r = orden_superior(lambda x, y, dy: dy + 2 * y, 0, [1, 0], 1, n=200)
    exacto = (2 * math.exp(-1) + math.exp(2)) / 3
    assert r["columnas"][0][-1] == pytest.approx(exacto, abs=1e-3)


def test_orden_superior_sin_condiciones() -> None:
    with pytest.raises(EntradaInvalidaError):
        orden_superior(lambda x, y: -y, 0, [], 1)
