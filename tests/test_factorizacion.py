"""Pruebas de inversa y factorizaciones de matrices (U-IV 4.2-4.3)."""

from __future__ import annotations

import pytest

from metodos.matrices.cholesky import cholesky, resolver_cholesky
from metodos.matrices.crout import crout, resolver_crout
from metodos.matrices.factorizacion_ldl import factorizacion_ldl, resolver_ldl
from metodos.matrices.factorizacion_lu import factorizacion_lu, resolver_lu
from metodos.matrices.inversa import inversa
from utils.errores import EntradaInvalidaError


def _producto(a, b):
    """Producto matricial simple para verificar reconstrucciones."""
    n = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)
    ]


def _aprox_matriz(a, b, tol=1e-9):
    return all(
        a[i][j] == pytest.approx(b[i][j], abs=tol)
        for i in range(len(a))
        for j in range(len(a))
    )


# --- Inversa ------------------------------------------------------------
def test_inversa_2x2() -> None:
    r = inversa([[4, 7], [2, 6]])
    assert _aprox_matriz(r["inversa"], [[0.6, -0.7], [-0.2, 0.4]])


def test_inversa_por_identidad() -> None:
    A = [[2, 1, 1], [1, 3, 2], [1, 0, 0]]
    inv = inversa(A)["inversa"]
    producto = _producto(A, inv)
    identidad = [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    assert _aprox_matriz(producto, identidad, tol=1e-9)


def test_inversa_singular() -> None:
    with pytest.raises(EntradaInvalidaError):
        inversa([[1, 2], [2, 4]])


# --- LU (Doolittle) -----------------------------------------------------
def test_lu_reconstruccion() -> None:
    A = [[4, 3], [6, 3]]
    f = factorizacion_lu(A)
    assert _aprox_matriz(_producto(f["L"], f["U"]), A)
    # L es triangular inferior con diagonal unitaria.
    assert f["L"][0][0] == 1.0 and f["L"][1][1] == 1.0


def test_lu_resolver() -> None:
    assert resolver_lu([[2, 1], [1, 3]], [3, 4])["solucion"] == pytest.approx(
        [1.0, 1.0]
    )


def test_lu_pivote_nulo() -> None:
    with pytest.raises(EntradaInvalidaError):
        factorizacion_lu([[0, 1], [1, 1]])


# --- Crout --------------------------------------------------------------
def test_crout_reconstruccion() -> None:
    A = [[2, 1, 1], [4, 3, 3], [8, 7, 9]]
    f = crout(A)
    assert _aprox_matriz(_producto(f["L"], f["U"]), A)
    # U tiene diagonal unitaria.
    assert all(f["U"][i][i] == 1.0 for i in range(3))


def test_crout_resolver() -> None:
    assert resolver_crout([[2, 1], [1, 3]], [3, 4])["solucion"] == pytest.approx(
        [1.0, 1.0]
    )


# --- Cholesky -----------------------------------------------------------
def test_cholesky_reconstruccion() -> None:
    A = [[25, 15, -5], [15, 18, 0], [-5, 0, 11]]
    L = cholesky(A)["L"]
    Lt = [[L[j][i] for j in range(3)] for i in range(3)]
    assert _aprox_matriz(_producto(L, Lt), A)


def test_cholesky_resolver() -> None:
    assert resolver_cholesky([[4, 2], [2, 2]], [6, 4])["solucion"] == pytest.approx(
        [1.0, 1.0]
    )


def test_cholesky_no_definida_positiva() -> None:
    with pytest.raises(EntradaInvalidaError):
        cholesky([[1, 2], [2, 1]])


def test_cholesky_no_simetrica() -> None:
    with pytest.raises(EntradaInvalidaError):
        cholesky([[4, 2], [1, 3]])


# --- LDL^T --------------------------------------------------------------
def test_ldl_reconstruccion() -> None:
    A = [[4, 12, -16], [12, 37, -43], [-16, -43, 98]]
    f = factorizacion_ldl(A)
    L, D = f["L"], f["D"]
    Lt = [[L[j][i] for j in range(3)] for i in range(3)]
    LD = [[L[i][k] * D[k] for k in range(3)] for i in range(3)]
    assert _aprox_matriz(_producto(LD, Lt), A)


def test_ldl_resolver() -> None:
    assert resolver_ldl([[4, 2], [2, 2]], [6, 4])["solucion"] == pytest.approx(
        [1.0, 1.0]
    )


def test_ldl_no_simetrica() -> None:
    with pytest.raises(EntradaInvalidaError):
        factorizacion_ldl([[4, 2], [1, 3]])
