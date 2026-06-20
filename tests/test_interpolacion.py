"""Pruebas unitarias de los métodos de interpolación."""

from __future__ import annotations

import pytest

from metodos.interpolacion.aproximacion_polinomial import aproximacion_polinomial
from metodos.interpolacion.diferencias_divididas import diferencias_divididas
from metodos.interpolacion.interpolacion_basica import interpolacion_basica
from metodos.interpolacion.lagrange import lagrange
from metodos.interpolacion.minimos_cuadrados import minimos_cuadrados
from metodos.interpolacion.neville import neville
from metodos.interpolacion.taylor import taylor
from utils.errores import EntradaInvalidaError


# --- Interpolación básica -----------------------------------------------
def test_interpolacion_basica_punto_medio() -> None:
    assert interpolacion_basica([0, 1, 2], [0, 10, 20], 0.5) == pytest.approx(5.0)


def test_interpolacion_basica_nodos_desordenados() -> None:
    assert interpolacion_basica([2, 0, 1], [20, 0, 10], 1.5) == pytest.approx(15.0)


def test_interpolacion_basica_pocos_puntos() -> None:
    with pytest.raises(EntradaInvalidaError):
        interpolacion_basica([1], [1], 0.5)


# --- Lagrange ------------------------------------------------------------
def test_lagrange_reproduce_nodos() -> None:
    x, y = [0, 1, 2], [1, 3, 7]
    for xi, yi in zip(x, y):
        assert lagrange(x, y, xi) == pytest.approx(yi)


def test_lagrange_valor_intermedio() -> None:
    assert lagrange([0, 1, 2], [1, 3, 7], 1.5) == pytest.approx(4.75)


def test_lagrange_x_repetidos() -> None:
    with pytest.raises(EntradaInvalidaError):
        lagrange([0, 0, 2], [1, 3, 7], 1.0)


def test_lagrange_longitudes_distintas() -> None:
    with pytest.raises(EntradaInvalidaError):
        lagrange([0, 1, 2], [1, 3], 1.0)


# --- Neville -------------------------------------------------------------
def test_neville_cuadratica_exacta() -> None:
    r = neville([1, 2, 3], [1, 4, 9], 2.5)
    assert r["valor"] == pytest.approx(6.25)
    assert "tabla" in r


def test_neville_coincide_con_lagrange() -> None:
    x, y = [0, 1, 2, 3], [1, 2, 0, 5]
    assert neville(x, y, 1.5)["valor"] == pytest.approx(lagrange(x, y, 1.5))


# --- Diferencias divididas ----------------------------------------------
def test_diferencias_divididas_coeficientes() -> None:
    r = diferencias_divididas([0, 1, 2], [1, 3, 7], x_evaluar=1.5)
    assert r["coeficientes"] == pytest.approx([1.0, 2.0, 1.0])
    assert r["valor"] == pytest.approx(4.75)


def test_diferencias_divididas_coincide_con_lagrange() -> None:
    x, y = [1, 2, 4, 5], [0, 3, 1, 8]
    r = diferencias_divididas(x, y, x_evaluar=3.0)
    assert r["valor"] == pytest.approx(lagrange(x, y, 3.0))


# --- Taylor --------------------------------------------------------------
def test_taylor_exponencial() -> None:
    # e^x en x0=0, grado 3, evaluar en 1.
    r = taylor([1, 1, 1, 1], x0=0, x_evaluar=1)
    assert r["valor"] == pytest.approx(1 + 1 + 0.5 + 1 / 6)
    assert r["grado"] == 3


def test_taylor_vacio() -> None:
    with pytest.raises(EntradaInvalidaError):
        taylor([], x0=0, x_evaluar=1)


# --- Mínimos cuadrados (lineal) -----------------------------------------
def test_minimos_cuadrados_recta_exacta() -> None:
    r = minimos_cuadrados([0, 1, 2, 3], [1, 3, 5, 7])
    assert r["pendiente"] == pytest.approx(2.0)
    assert r["interseccion"] == pytest.approx(1.0)
    assert r["r2"] == pytest.approx(1.0)


def test_minimos_cuadrados_x_constantes() -> None:
    with pytest.raises(EntradaInvalidaError):
        minimos_cuadrados([1, 1, 1], [2, 3, 4])


# --- Aproximación polinómica --------------------------------------------
def test_aproximacion_polinomial_cuadratica() -> None:
    r = aproximacion_polinomial([0, 1, 2, 3], [0, 1, 4, 9], grado=2)
    assert r["coeficientes"] == pytest.approx([0.0, 0.0, 1.0], abs=1e-9)
    assert r["r2"] == pytest.approx(1.0)


def test_aproximacion_polinomial_grado_excesivo() -> None:
    with pytest.raises(EntradaInvalidaError):
        aproximacion_polinomial([0, 1], [0, 1], grado=5)
