"""Pruebas de las extensiones de la capa de interfaz (sin Tkinter).

Cubre los nuevos tipos del evaluador (f(x,y,z), sistemas de EDO, función de
estado) y el formateo de matrices y soluciones de sistemas, todo sin
requerir un entorno gráfico.
"""

from __future__ import annotations

import pytest

from interfaz import evaluador
from interfaz.formato_resultado import formatear_resultado


# --- Evaluador: nuevos tipos --------------------------------------------
def test_crear_funcion_xyz() -> None:
    f = evaluador.crear_funcion_xyz("x + y + z")
    assert f(1, 2, 3) == pytest.approx(6.0)


def test_crear_sistema_edo() -> None:
    f = evaluador.crear_sistema_edo("y2; -y1")
    assert f(0.0, [3.0, 5.0]) == [5.0, -3.0]


def test_crear_sistema_edo_vacio() -> None:
    with pytest.raises(evaluador.ExpresionInvalidaError):
        evaluador.crear_sistema_edo("   ")


def test_crear_funcion_estado() -> None:
    # g(x, y0, y1) = y1 + 2 y0
    g = evaluador.crear_funcion_estado("y1 + 2*y0")
    assert g(0.0, 1.0, 3.0) == pytest.approx(5.0)


def test_evaluador_sin_builtins() -> None:
    # El espacio de nombres restringido no expone builtins peligrosos.
    f = evaluador.crear_funcion_x("__import__('os')")
    with pytest.raises(Exception):
        f(0)


# --- Formateo de resultados ---------------------------------------------
def test_formatear_matriz() -> None:
    salida = formatear_resultado({"inversa": [[0.5, 0.0], [0.0, 0.25]], "n": 2})
    assert "inversa:" in salida
    assert "0.500000" in salida
    assert "n: 2" in salida


def test_formatear_solucion_sistema() -> None:
    resultado = {
        "solucion": [(0.0, (0.0, 1.0)), (0.5, (0.48, 0.88))],
        "h": 0.5,
    }
    salida = formatear_resultado(resultado)
    assert "y1" in salida and "y2" in salida


def test_formatear_lista_simple() -> None:
    assert "Solución" in formatear_resultado([1.0, 2.0, 3.0]) or "Solucion" in (
        formatear_resultado([1.0, 2.0, 3.0])
    )


def test_formatear_escalar() -> None:
    assert "2.000000" in formatear_resultado(2.0)
