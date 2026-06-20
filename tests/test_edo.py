"""Pruebas unitarias de los métodos para EDO."""

from __future__ import annotations

import math

import pytest

from metodos.edo.euler import euler
from metodos.edo.runge_kutta import runge_kutta
from metodos.edo.runge_kutta_fehlberg import runge_kutta_fehlberg
from metodos.edo.taylor_superior import taylor_superior
from utils.errores import EntradaInvalidaError

E = math.e


# --- Euler ---------------------------------------------------------------
def test_euler_exponencial() -> None:
    sol = euler(lambda x, y: y, 0, 1, 1, n=1000)
    assert sol[0] == (0, 1)
    assert sol[-1][1] == pytest.approx(E, abs=1e-2)
    assert len(sol) == 1001


def test_euler_x_final_igual_x0() -> None:
    with pytest.raises(EntradaInvalidaError):
        euler(lambda x, y: y, 0, 1, 0)


def test_euler_n_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        euler(lambda x, y: y, 0, 1, 1, n=0)


# --- Taylor de orden superior -------------------------------------------
def test_taylor_superior_orden2() -> None:
    # dy/dx = y: f y f' coinciden con y.
    sol = taylor_superior([lambda x, y: y, lambda x, y: y], 0, 1, 1, n=100)
    assert sol[-1][1] == pytest.approx(E, abs=1e-3)


def test_taylor_superior_derivadas_vacias() -> None:
    with pytest.raises(EntradaInvalidaError):
        taylor_superior([], 0, 1, 1)


# --- Runge-Kutta 4 -------------------------------------------------------
def test_runge_kutta_preciso() -> None:
    sol = runge_kutta(lambda x, y: y, 0, 1, 1, n=10)
    assert sol[-1][1] == pytest.approx(E, abs=1e-5)


def test_runge_kutta_logistica() -> None:
    # dy/dx = x - y, y(0)=1; solución exacta y = x - 1 + 2 e^{-x}.
    sol = runge_kutta(lambda x, y: x - y, 0, 1, 2, n=200)
    exacto = 2 - 1 + 2 * math.exp(-2)
    assert sol[-1][1] == pytest.approx(exacto, abs=1e-6)


# --- Runge-Kutta-Fehlberg -----------------------------------------------
def test_rkf_exponencial() -> None:
    sol = runge_kutta_fehlberg(lambda x, y: y, 0, 1, 1, tolerancia=1e-8)
    assert sol[-1][0] == pytest.approx(1.0)
    assert sol[-1][1] == pytest.approx(E, abs=1e-6)


def test_rkf_x_final_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        runge_kutta_fehlberg(lambda x, y: y, 0, 1, -1)
