"""Pruebas unitarias de los métodos de integración numérica."""

from __future__ import annotations

import math

import pytest

from metodos.integracion.cuadratura_adaptativa import cuadratura_adaptativa
from metodos.integracion.cuadratura_gaussiana import cuadratura_gaussiana
from metodos.integracion.punto_medio import punto_medio
from metodos.integracion.romberg import romberg
from metodos.integracion.simpson_tres_octavos import simpson_tres_octavos
from metodos.integracion.simpson_tres_octavos_compuesto import (
    simpson_tres_octavos_compuesto,
)
from metodos.integracion.simpson_un_tercio import simpson_un_tercio
from metodos.integracion.simpson_un_tercio_compuesto import (
    simpson_un_tercio_compuesto,
)
from metodos.integracion.trapecio import trapecio
from metodos.integracion.trapecio_compuesto import trapecio_compuesto
from utils.errores import EntradaInvalidaError


# --- Reglas simples ------------------------------------------------------
def test_trapecio_lineal_exacto() -> None:
    assert trapecio(lambda x: x, 0, 2) == pytest.approx(2.0)


def test_punto_medio_lineal_exacto() -> None:
    assert punto_medio(lambda x: x, 0, 2) == pytest.approx(2.0)


def test_simpson_un_tercio_cubica_exacta() -> None:
    # Simpson 1/3 integra exacto hasta grado 3.
    assert simpson_un_tercio(lambda x: x**3, 0, 2) == pytest.approx(4.0)


def test_simpson_tres_octavos_cubica_exacta() -> None:
    assert simpson_tres_octavos(lambda x: x**3, 0, 2) == pytest.approx(4.0)


def test_trapecio_intervalo_invalido() -> None:
    with pytest.raises(EntradaInvalidaError):
        trapecio(lambda x: x, 2, 0)


# --- Reglas compuestas ---------------------------------------------------
def test_trapecio_compuesto_converge() -> None:
    assert trapecio_compuesto(lambda x: x**2, 0, 2, 1000) == pytest.approx(
        8 / 3, abs=1e-4
    )


def test_simpson_un_tercio_compuesto() -> None:
    val = simpson_un_tercio_compuesto(math.sin, 0, math.pi, 100)
    assert val == pytest.approx(2.0, abs=1e-6)


def test_simpson_un_tercio_compuesto_impar() -> None:
    with pytest.raises(EntradaInvalidaError):
        simpson_un_tercio_compuesto(lambda x: x, 0, 1, n=3)


def test_simpson_tres_octavos_compuesto() -> None:
    val = simpson_tres_octavos_compuesto(lambda x: x**3, 0, 2, 9)
    assert val == pytest.approx(4.0, abs=1e-9)


def test_simpson_tres_octavos_compuesto_no_multiplo_3() -> None:
    with pytest.raises(EntradaInvalidaError):
        simpson_tres_octavos_compuesto(lambda x: x, 0, 1, n=10)


# --- Romberg, adaptativa, gaussiana -------------------------------------
def test_romberg_cubica() -> None:
    r = romberg(lambda x: x**3, 0, 2, niveles=4)
    assert r["valor"] == pytest.approx(4.0, abs=1e-9)
    assert len(r["tabla"]) == 4


def test_cuadratura_adaptativa_seno() -> None:
    assert cuadratura_adaptativa(math.sin, 0, math.pi) == pytest.approx(2.0, abs=1e-7)


def test_cuadratura_gaussiana_exacta() -> None:
    # 2 puntos integran exacto polinomios de grado <= 3.
    assert cuadratura_gaussiana(lambda x: x**3, 0, 2, puntos=2) == pytest.approx(4.0)


def test_cuadratura_gaussiana_suave() -> None:
    assert cuadratura_gaussiana(math.sin, 0, math.pi, puntos=5) == pytest.approx(
        2.0, abs=1e-4
    )


def test_cuadratura_gaussiana_puntos_invalidos() -> None:
    with pytest.raises(EntradaInvalidaError):
        cuadratura_gaussiana(lambda x: x, 0, 1, puntos=7)
