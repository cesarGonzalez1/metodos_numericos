"""Pruebas de la capa de interfaz (sin abrir ventanas Tkinter).

Verifican el evaluador de expresiones, el registro de métodos y el
formateo de resultados. No instancian widgets Tk para poder ejecutarse en
entornos sin display (CI headless).
"""

from __future__ import annotations

import pytest

from interfaz import evaluador
from interfaz.formato_resultado import formatear_resultado
from interfaz.registro import CATEGORIAS


# --- Evaluador -----------------------------------------------------------
def test_crear_funcion_x() -> None:
    f = evaluador.crear_funcion_x("x**2 + 1")
    assert f(3) == pytest.approx(10.0)


def test_crear_funcion_xy() -> None:
    f = evaluador.crear_funcion_xy("x + y")
    assert f(2, 5) == pytest.approx(7.0)


def test_funcion_usa_math() -> None:
    f = evaluador.crear_funcion_x("sin(x)")
    assert f(0) == pytest.approx(0.0)


def test_funcion_sin_builtins() -> None:
    # No debe poder usar funciones peligrosas: `open` no está disponible.
    f = evaluador.crear_funcion_x("open('x')")
    with pytest.raises(Exception):
        f(0)


def test_expresion_invalida() -> None:
    with pytest.raises(evaluador.ExpresionInvalidaError):
        evaluador.crear_funcion_x("x +")


def test_parsear_lista() -> None:
    assert evaluador.parsear_lista("1, 2, 3") == [1.0, 2.0, 3.0]
    assert evaluador.parsear_lista("1 2 3") == [1.0, 2.0, 3.0]


def test_parsear_lista_invalida() -> None:
    with pytest.raises(evaluador.ExpresionInvalidaError):
        evaluador.parsear_lista("1, a, 3")


def test_parsear_matriz() -> None:
    assert evaluador.parsear_matriz("2 1; 1 3") == [[2.0, 1.0], [1.0, 3.0]]


def test_parsear_lista_funciones_xy() -> None:
    funcs = evaluador.parsear_lista_funciones_xy("y; x + y")
    assert len(funcs) == 2
    assert funcs[0](1, 2) == pytest.approx(2.0)
    assert funcs[1](1, 2) == pytest.approx(3.0)


# --- Registro ------------------------------------------------------------
def test_categorias_esperadas() -> None:
    nombres = [categoria for categoria, _ in CATEGORIAS]
    assert nombres == [
        "Conversión",
        "Raíces",
        "Interpolación",
        "Derivación",
        "Integración",
        "EDO",
        "Sistemas lineales",
    ]


def test_cada_metodo_es_invocable() -> None:
    for _categoria, metodos in CATEGORIAS:
        for metodo in metodos:
            assert callable(metodo["funcion"])
            assert isinstance(metodo["campos"], list) and metodo["campos"]


def test_claves_de_campos_unicas_por_metodo() -> None:
    for _categoria, metodos in CATEGORIAS:
        for metodo in metodos:
            claves = [c["clave"] for c in metodo["campos"]]
            assert len(claves) == len(set(claves))


# --- Formateo de resultados ---------------------------------------------
def test_formatear_float() -> None:
    assert "Resultado" in formatear_resultado(3.14159)


def test_formatear_vector() -> None:
    texto = formatear_resultado([1.0, 2.0, 3.0])
    assert "Solución" in texto


def test_formatear_lista_tuplas() -> None:
    texto = formatear_resultado([(0.0, 1.0), (0.5, 1.5)])
    assert "x" in texto and "y" in texto


def test_formatear_dict_con_historial() -> None:
    valor = {
        "raiz": 2.0,
        "convergio": True,
        "historial": [{"i": 1, "c": 2.0, "error": 0.1}],
    }
    texto = formatear_resultado(valor)
    assert "raiz" in texto and "Historial" in texto
