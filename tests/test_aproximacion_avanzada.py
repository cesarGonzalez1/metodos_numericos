"""Pruebas de regresión, Hermite, splines y Fourier (U-V)."""

from __future__ import annotations

import math

import pytest

from metodos.interpolacion.fourier import fourier
from metodos.interpolacion.hermite import hermite
from metodos.interpolacion.regresion_multiple import regresion_multiple
from metodos.interpolacion.regresion_no_lineal import regresion_no_lineal
from metodos.interpolacion.splines_cubicos import splines_cubicos
from utils.errores import EntradaInvalidaError


# --- Regresión lineal múltiple ------------------------------------------
def test_regresion_multiple_exacta() -> None:
    # y = 1 + 2 x1 + 3 x2 (datos exactos)
    X = [[1, 1], [2, 1], [1, 2], [3, 2], [2, 3]]
    y = [1 + 2 * a + 3 * b for a, b in X]
    r = regresion_multiple(X, y)
    assert r["coeficientes"] == pytest.approx([1.0, 2.0, 3.0], abs=1e-6)
    assert r["r2"] == pytest.approx(1.0, abs=1e-9)


def test_regresion_multiple_pocas_observaciones() -> None:
    with pytest.raises(EntradaInvalidaError):
        regresion_multiple([[1, 1], [2, 2]], [1, 2])


def test_regresion_multiple_colineal() -> None:
    # x2 = 2·x1 -> sistema normal singular.
    X = [[1, 2], [2, 4], [3, 6], [4, 8]]
    with pytest.raises(EntradaInvalidaError):
        regresion_multiple(X, [1, 2, 3, 4])


# --- Regresión no lineal ------------------------------------------------
def test_regresion_exponencial() -> None:
    xs = [0, 1, 2, 3]
    ys = [2 * math.exp(0.5 * x) for x in xs]
    r = regresion_no_lineal(xs, ys, "exponencial")
    assert r["a"] == pytest.approx(2.0, abs=1e-6)
    assert r["b"] == pytest.approx(0.5, abs=1e-6)
    assert r["r2"] == pytest.approx(1.0, abs=1e-9)


def test_regresion_potencia() -> None:
    r = regresion_no_lineal([1, 2, 3, 4], [3, 12, 27, 48], "potencia")
    assert r["a"] == pytest.approx(3.0, abs=1e-6)
    assert r["b"] == pytest.approx(2.0, abs=1e-6)


def test_regresion_no_lineal_y_no_positiva() -> None:
    with pytest.raises(EntradaInvalidaError):
        regresion_no_lineal([1, 2, 3], [1, -2, 3], "exponencial")


def test_regresion_modelo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        regresion_no_lineal([1, 2], [1, 2], "logaritmica")


# --- Hermite ------------------------------------------------------------
def test_hermite_cuadratica() -> None:
    # f(x)=x^2: f(1)=1,f'(1)=2 ; f(2)=4,f'(2)=4 -> H(1.5)=2.25
    r = hermite([1, 2], [1, 4], [2, 4], 1.5)
    assert r["valor"] == pytest.approx(2.25, abs=1e-9)


def test_hermite_reproduce_nodos() -> None:
    # En los nodos, H coincide con f.
    r = hermite([1, 2], [1, 4], [2, 4], 2.0)
    assert r["valor"] == pytest.approx(4.0, abs=1e-9)


def test_hermite_nodos_repetidos() -> None:
    with pytest.raises(EntradaInvalidaError):
        hermite([1, 1], [1, 1], [2, 2], 1.5)


# --- Splines cúbicos ----------------------------------------------------
def test_spline_reproduce_nodos() -> None:
    r = splines_cubicos([0, 1, 2, 3], [0, 1, 4, 9], 2.0)
    assert r["valor"] == pytest.approx(4.0, abs=1e-9)


def test_spline_interpola() -> None:
    r = splines_cubicos([0, 1, 2, 3], [0, 1, 4, 9], 1.5)
    assert 1.0 < r["valor"] < 4.0


def test_spline_pocos_puntos() -> None:
    with pytest.raises(EntradaInvalidaError):
        splines_cubicos([0, 1], [0, 1], 0.5)


def test_spline_fuera_de_rango() -> None:
    with pytest.raises(EntradaInvalidaError):
        splines_cubicos([0, 1, 2], [0, 1, 4], 5.0)


def test_spline_no_creciente() -> None:
    with pytest.raises(EntradaInvalidaError):
        splines_cubicos([0, 2, 1], [0, 4, 1], 1.5)


# --- Fourier ------------------------------------------------------------
def test_fourier_coseno() -> None:
    # f(x)=cos(x) en [-π, π]: a_1 ≈ 1, resto ≈ 0
    r = fourier(math.cos, -math.pi, math.pi, m=8, n=3)
    assert r["a"][1] == pytest.approx(1.0, abs=1e-6)
    assert r["a"][0] == pytest.approx(0.0, abs=1e-6)


def test_fourier_n_mayor_igual_m() -> None:
    with pytest.raises(EntradaInvalidaError):
        fourier(math.cos, -math.pi, math.pi, m=4, n=4)


def test_fourier_evalua_punto() -> None:
    r = fourier(math.cos, -math.pi, math.pi, m=16, n=5, x_evaluar=0.0)
    assert "valor" in r
    assert r["valor"] == pytest.approx(1.0, abs=1e-2)
