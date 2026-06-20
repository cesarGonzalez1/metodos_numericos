"""Pruebas unitarias de los métodos de derivación numérica."""

from __future__ import annotations

import math

import pytest

from metodos.derivacion.cinco_puntos import cinco_puntos
from metodos.derivacion.cuatro_puntos import cuatro_puntos
from metodos.derivacion.diferencias_finitas import (
    derivada,
    diferencia_adelante,
    diferencia_atras,
    diferencia_centrada,
)
from metodos.derivacion.richardson import richardson
from metodos.derivacion.tres_puntos import tres_puntos
from utils.errores import EntradaInvalidaError


# --- Diferencias finitas (general) --------------------------------------
def test_diferencia_centrada_polinomio() -> None:
    assert diferencia_centrada(lambda x: x**2, 3.0, 1e-5) == pytest.approx(
        6.0, abs=1e-4
    )


def test_diferencia_adelante_y_atras() -> None:
    assert diferencia_adelante(lambda x: x**2, 3.0, 1e-6) == pytest.approx(
        6.0, abs=1e-3
    )
    assert diferencia_atras(lambda x: x**2, 3.0, 1e-6) == pytest.approx(6.0, abs=1e-3)


def test_derivada_seno() -> None:
    # d/dx sin(x) en 0 = cos(0) = 1.
    assert derivada(math.sin, 0.0, 1e-5, "centrada") == pytest.approx(1.0, abs=1e-6)


def test_derivada_tipo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        derivada(math.sin, 0.0, tipo="oblicua")


def test_diferencia_paso_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        diferencia_centrada(lambda x: x, 1.0, h=0)


def test_diferencia_funcion_invalida() -> None:
    with pytest.raises(EntradaInvalidaError):
        diferencia_centrada(42, 1.0)


# --- 3 puntos ------------------------------------------------------------
def test_tres_puntos_variantes() -> None:
    f = lambda x: x**2  # noqa: E731
    for tipo in ("medio", "adelante", "atras"):
        assert tres_puntos(f, 3.0, 1e-4, tipo) == pytest.approx(6.0, abs=1e-3)


def test_tres_puntos_tipo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        tres_puntos(lambda x: x, 1.0, tipo="centrada")


# --- 4 puntos ------------------------------------------------------------
def test_cuatro_puntos_cubica() -> None:
    f = lambda x: x**3  # noqa: E731
    assert cuatro_puntos(f, 2.0, 1e-3, "adelante") == pytest.approx(12.0, abs=1e-2)
    assert cuatro_puntos(f, 2.0, 1e-3, "atras") == pytest.approx(12.0, abs=1e-2)


# --- 5 puntos ------------------------------------------------------------
def test_cinco_puntos_cuartica() -> None:
    f = lambda x: x**4  # noqa: E731
    assert cinco_puntos(f, 2.0, 1e-2, "medio") == pytest.approx(32.0, abs=1e-4)
    assert cinco_puntos(f, 2.0, 1e-2, "adelante") == pytest.approx(32.0, abs=1e-2)


# --- Richardson ----------------------------------------------------------
def test_richardson_cubica() -> None:
    r = richardson(lambda x: x**3, 2.0, h=0.1, niveles=4)
    assert r["valor"] == pytest.approx(12.0, abs=1e-8)
    assert len(r["tabla"]) == 4


def test_richardson_niveles_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        richardson(lambda x: x, 1.0, niveles=0)
