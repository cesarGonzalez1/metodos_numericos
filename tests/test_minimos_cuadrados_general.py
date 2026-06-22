"""Pruebas del ajuste por mínimos cuadrados con funciones base arbitrarias."""

from __future__ import annotations

import math

import pytest

from metodos.interpolacion.minimos_cuadrados_general import (
    minimos_cuadrados_general,
)
from utils.errores import EntradaInvalidaError


def test_recta_recupera_minimos_cuadrados_lineal() -> None:
    # Base [1, x] equivale al ajuste lineal ordinario.
    base = [lambda x: 1.0, lambda x: x]
    r = minimos_cuadrados_general(base, [0, 1, 2, 3], [1, 3, 5, 7])
    assert r["coeficientes"][0] == pytest.approx(1.0)
    assert r["coeficientes"][1] == pytest.approx(2.0)
    assert r["r2"] == pytest.approx(1.0)


def test_ajuste_polinomial_con_base_de_potencias() -> None:
    base = [lambda x: 1.0, lambda x: x, lambda x: x**2]
    xs = [0, 1, 2, 3, 4]
    ys = [x**2 for x in xs]
    r = minimos_cuadrados_general(base, xs, ys)
    assert r["coeficientes"][0] == pytest.approx(0.0, abs=1e-9)
    assert r["coeficientes"][1] == pytest.approx(0.0, abs=1e-9)
    assert r["coeficientes"][2] == pytest.approx(1.0)


def test_base_trigonometrica() -> None:
    base = [lambda x: 1.0, math.sin]
    xs = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [2 + 3 * math.sin(x) for x in xs]
    r = minimos_cuadrados_general(base, xs, ys)
    assert r["coeficientes"][0] == pytest.approx(2.0)
    assert r["coeficientes"][1] == pytest.approx(3.0)
    assert r["r2"] == pytest.approx(1.0)


def test_predichos_coinciden_con_modelo() -> None:
    base = [lambda x: 1.0, lambda x: x]
    r = minimos_cuadrados_general(base, [0, 1, 2], [1, 2, 3])
    assert r["predichos"] == pytest.approx([1.0, 2.0, 3.0])


def test_sin_funciones_es_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        minimos_cuadrados_general([], [0, 1], [0, 1])


def test_menos_puntos_que_funciones() -> None:
    base = [lambda x: 1.0, lambda x: x, lambda x: x**2]
    with pytest.raises(EntradaInvalidaError):
        minimos_cuadrados_general(base, [0, 1], [0, 1])


def test_funciones_base_dependientes_dan_sistema_singular() -> None:
    # g1 = x y g2 = 2x son linealmente dependientes -> AᵀA singular.
    base = [lambda x: x, lambda x: 2 * x]
    with pytest.raises(EntradaInvalidaError):
        minimos_cuadrados_general(base, [1, 2, 3], [1, 2, 3])


def test_longitudes_distintas() -> None:
    base = [lambda x: 1.0, lambda x: x]
    with pytest.raises(EntradaInvalidaError):
        minimos_cuadrados_general(base, [0, 1, 2], [0, 1])
