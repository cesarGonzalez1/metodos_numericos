"""Tests de conversión entre bases: decimal <-> binario (IEEE 754)."""

from __future__ import annotations

import math

import pytest

from metodos.conversion.binario_a_decimal import binario_a_decimal
from metodos.conversion.decimal_a_binario import decimal_a_binario
from utils.errores import EntradaInvalidaError


def test_decimal_a_binario_directo():
    r = decimal_a_binario(12.625, "simple")
    assert r["binario directo"] == "1100.101"
    assert r["signo"].startswith("0")
    assert r["exponente real (sin sesgo)"] == 3


def test_decimal_a_binario_negativo_signo():
    r = decimal_a_binario(-5.0, "doble")
    assert r["signo"].startswith("1")
    assert r["binario directo"] == "-101"


@pytest.mark.parametrize("valor", [12.625, -3.14159, 0.1, 1.0, -256.0])
def test_round_trip_doble_exacto(valor):
    # En doble precisión el viaje de ida y vuelta es exacto bit a bit.
    bits = decimal_a_binario(valor, "doble")["binario IEEE 754 completo"]
    assert binario_a_decimal(bits, "doble")["valor decimal"] == valor


@pytest.mark.parametrize("valor", [12.625, -3.14159, 0.1, 1.0, -256.0])
def test_round_trip_simple_aproximado(valor):
    # En simple precisión hay redondeo float64 -> float32 (esperado).
    bits = decimal_a_binario(valor, "simple")["binario IEEE 754 completo"]
    reconstruido = binario_a_decimal(bits, "simple")["valor decimal"]
    assert math.isclose(reconstruido, valor, rel_tol=1e-6)


def test_binario_posicional_con_punto():
    r = binario_a_decimal("1010.101")
    assert r["valor decimal"] == 10.625
    assert r["modo"].startswith("binario posicional")


def test_binario_posicional_negativo():
    assert binario_a_decimal("-11.1")["valor decimal"] == -3.5


def test_ieee_desglose_campos():
    # 1.0 en doble: signo 0, caracteristica 1023, mantisa 0.
    bits = "0" + format(1023, "011b") + "0" * 52
    r = binario_a_decimal(bits, "doble")
    assert r["valor decimal"] == 1.0
    assert r["exponente real (sin sesgo)"] == 0
    assert r["tipo"].startswith("normalizado")


def test_ieee_cero_e_infinito():
    assert binario_a_decimal("0" * 64, "doble")["valor decimal"] == 0.0
    inf_bits = "0" + "1" * 8 + "0" * 23
    assert binario_a_decimal(inf_bits, "simple")["valor decimal"] == math.inf


def test_ieee_nan():
    nan_bits = "0" + "1" * 8 + "1" + "0" * 22
    assert math.isnan(binario_a_decimal(nan_bits, "simple")["valor decimal"])


def test_separadores_ignorados():
    r = decimal_a_binario(1.0, "simple")
    agrupado = r["IEEE 754 (signo | caracteristica | mantisa)"]
    assert binario_a_decimal(agrupado, "simple")["valor decimal"] == 1.0


def test_precision_invalida():
    with pytest.raises(EntradaInvalidaError):
        decimal_a_binario(1.0, "cuadruple")
    with pytest.raises(EntradaInvalidaError):
        binario_a_decimal("0" * 32, "cuadruple")


def test_longitud_ieee_incorrecta():
    with pytest.raises(EntradaInvalidaError):
        binario_a_decimal("0101", "simple")


def test_caracteres_no_binarios():
    with pytest.raises(EntradaInvalidaError):
        binario_a_decimal("10201")
    with pytest.raises(EntradaInvalidaError):
        binario_a_decimal("")
