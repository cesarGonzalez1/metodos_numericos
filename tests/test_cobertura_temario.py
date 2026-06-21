"""Pruebas de los apartados del temario añadidos durante la auditoría."""

from __future__ import annotations

import math

import pytest

from metodos.conversion.analisis_errores import (
    analisis_errores,
    redondeo_y_truncamiento,
)
from metodos.derivacion.n_mas_un_puntos import n_mas_un_puntos
from metodos.edo.adams_variable import adams_variable
from metodos.integracion.punto_medio_compuesto import punto_medio_compuesto
from utils.errores import EntradaInvalidaError


def test_analisis_errores() -> None:
    r = analisis_errores(10.0, 9.8)
    assert r["error absoluto"] == pytest.approx(0.2)
    assert r["error relativo"] == pytest.approx(0.02)
    assert r["error porcentual"] == pytest.approx(2.0)


def test_error_relativo_indefinido_en_cero() -> None:
    assert analisis_errores(0.0, 0.1)["error relativo"] is None


def test_redondeo_y_truncamiento() -> None:
    r = redondeo_y_truncamiento(1.2396, 3)
    assert r["redondeado (empates al par)"] == pytest.approx(1.24)
    assert r["truncado (hacia cero)"] == pytest.approx(1.239)


def test_n_mas_un_puntos_centrada() -> None:
    r = n_mas_un_puntos(math.sin, 0.3, h=0.01, puntos=7)
    assert r["derivada"] == pytest.approx(math.cos(0.3), abs=1e-10)
    assert sum(r["pesos"]) == pytest.approx(0.0, abs=1e-12)


def test_n_mas_un_puntos_centrada_requiere_impar() -> None:
    with pytest.raises(EntradaInvalidaError):
        n_mas_un_puntos(math.sin, 0.0, puntos=4)


def test_punto_medio_compuesto() -> None:
    r = punto_medio_compuesto(lambda x: x**2, 0.0, 1.0, n=1000)
    assert r["integral"] == pytest.approx(1 / 3, abs=1e-7)
    assert r["evaluaciones"] == 1000


def test_adams_variable_exponencial() -> None:
    r = adams_variable(
        lambda x, y: y,
        0.0,
        1.0,
        1.0,
        tolerancia=1e-7,
        h_inicial=0.08,
        h_max=0.2,
    )
    assert r["solucion"][-1][0] == pytest.approx(1.0)
    assert r["solucion"][-1][1] == pytest.approx(math.e, abs=2e-5)
    assert r["pasos aceptados"] > 3
