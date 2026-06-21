"""Pruebas de la integración múltiple (U-II 2.4)."""

from __future__ import annotations

import pytest

from metodos.integracion.cuadratura_gaussiana_doble import cuadratura_gaussiana_doble
from metodos.integracion.cuadratura_gaussiana_triple import (
    cuadratura_gaussiana_triple,
)
from metodos.integracion.integral_doble_simpson import integral_doble_simpson
from utils.errores import EntradaInvalidaError


# --- Integral doble de Simpson ------------------------------------------
def test_doble_simpson_lineal() -> None:
    # ∫_0^1 ∫_0^1 (x + y) dy dx = 1
    r = integral_doble_simpson(lambda x, y: x + y, 0, 1, 0, 1)
    assert r["integral"] == pytest.approx(1.0, abs=1e-9)


def test_doble_simpson_producto() -> None:
    # ∫_0^2 ∫_0^1 x·y dy dx = 1
    r = integral_doble_simpson(lambda x, y: x * y, 0, 2, 0, 1, n=4, m=4)
    assert r["integral"] == pytest.approx(1.0, abs=1e-9)


def test_doble_simpson_cuadratico_exacto() -> None:
    # Simpson integra cúbicas de forma exacta: ∫_0^1∫_0^1 x^2·y^2 = 1/9
    r = integral_doble_simpson(lambda x, y: x**2 * y**2, 0, 1, 0, 1, n=2, m=2)
    assert r["integral"] == pytest.approx(1 / 9, abs=1e-12)


def test_doble_simpson_n_impar() -> None:
    with pytest.raises(EntradaInvalidaError):
        integral_doble_simpson(lambda x, y: x, 0, 1, 0, 1, n=3, m=4)


def test_doble_simpson_intervalo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        integral_doble_simpson(lambda x, y: x, 1, 0, 0, 1)


# --- Cuadratura gaussiana doble -----------------------------------------
def test_gauss_doble_suma_cuadrados() -> None:
    r = cuadratura_gaussiana_doble(lambda x, y: x**2 + y**2, 0, 1, 0, 1)
    assert r["integral"] == pytest.approx(2 / 3, abs=1e-10)


def test_gauss_doble_producto() -> None:
    r = cuadratura_gaussiana_doble(lambda x, y: x * y, 0, 2, 0, 3)
    assert r["integral"] == pytest.approx(9.0, abs=1e-10)


def test_gauss_doble_puntos_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        cuadratura_gaussiana_doble(lambda x, y: x, 0, 1, 0, 1, puntos=9)


# --- Cuadratura gaussiana triple ----------------------------------------
def test_gauss_triple_suma() -> None:
    r = cuadratura_gaussiana_triple(lambda x, y, z: x + y + z, 0, 1, 0, 1, 0, 1)
    assert r["integral"] == pytest.approx(1.5, abs=1e-10)


def test_gauss_triple_producto() -> None:
    r = cuadratura_gaussiana_triple(lambda x, y, z: x * y * z, 0, 1, 0, 1, 0, 1)
    assert r["integral"] == pytest.approx(0.125, abs=1e-10)
    assert r["evaluaciones"] == 27


def test_gauss_triple_intervalo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        cuadratura_gaussiana_triple(lambda x, y, z: x, 0, 1, 0, 1, 1, 0)
