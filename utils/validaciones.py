"""Validaciones de entrada reutilizables por todos los métodos numéricos.

Mantener aquí cualquier validación que se repita en más de un método para
evitar duplicación (DRY). Cada función debe lanzar
`utils.errores.EntradaInvalidaError` cuando la validación falle.
"""

from __future__ import annotations

from collections.abc import Callable

from utils.errores import EntradaInvalidaError


def validar_no_vacia(lista: object, nombre: str = "datos") -> None:
    """Valida que `lista` sea una secuencia no vacía.

    Args:
        lista: Secuencia (list/tuple) a validar.
        nombre: Nombre del parámetro, usado en el mensaje de error.

    Raises:
        EntradaInvalidaError: Si no es lista/tupla o está vacía.
    """
    if not isinstance(lista, (list, tuple)):
        raise EntradaInvalidaError(f"'{nombre}' debe ser una lista o tupla.")
    if len(lista) == 0:
        raise EntradaInvalidaError(f"'{nombre}' no puede estar vacía.")


def validar_sin_duplicados(valores: list, nombre: str = "x_datos") -> None:
    """Valida que `valores` no contenga elementos repetidos.

    Args:
        valores: Secuencia de valores (típicamente nodos x).
        nombre: Nombre del parámetro, usado en el mensaje de error.

    Raises:
        EntradaInvalidaError: Si hay valores repetidos.
    """
    if len(set(valores)) != len(valores):
        raise EntradaInvalidaError(f"'{nombre}' no debe contener valores repetidos.")


def validar_entero_positivo(valor: int, nombre: str) -> None:
    """Valida que `valor` sea un entero estrictamente positivo.

    Args:
        valor: Valor a validar.
        nombre: Nombre del parámetro, usado en el mensaje de error.

    Raises:
        EntradaInvalidaError: Si no es entero o es <= 0.
    """
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise EntradaInvalidaError(f"'{nombre}' debe ser un entero.")
    if valor <= 0:
        raise EntradaInvalidaError(
            f"'{nombre}' debe ser mayor a 0, se recibió: {valor}."
        )


def validar_funcion(f: object, nombre: str = "f") -> None:
    """Valida que `f` sea invocable (una función o callable).

    Args:
        f: Objeto que debería ser una función de una variable.
        nombre: Nombre del parámetro, usado en el mensaje de error.

    Raises:
        EntradaInvalidaError: Si `f` no es invocable.
    """
    if not callable(f):
        raise EntradaInvalidaError(
            f"El parámetro '{nombre}' debe ser una función invocable."
        )


def validar_tolerancia(tolerancia: float) -> None:
    """Valida que la tolerancia sea un número estrictamente positivo.

    Args:
        tolerancia: Error absoluto máximo aceptado por un método iterativo.

    Raises:
        EntradaInvalidaError: Si tolerancia <= 0.
    """
    if tolerancia <= 0:
        raise EntradaInvalidaError(
            f"La tolerancia debe ser mayor a 0, se recibió: {tolerancia}."
        )


def validar_cambio_signo(f: Callable[[float], float], a: float, b: float) -> None:
    """Valida que `f(a)` y `f(b)` tengan signos opuestos.

    Es la condición necesaria para los métodos cerrados (bisección y regla
    falsa): garantiza —por el teorema de Bolzano— que existe al menos una
    raíz en el intervalo [a, b].

    Args:
        f: Función continua evaluada en los extremos.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.

    Raises:
        EntradaInvalidaError: Si f(a) y f(b) no tienen signos opuestos.
    """
    if f(a) * f(b) > 0:
        raise EntradaInvalidaError(
            "No se garantiza una raíz en el intervalo: f(a) y f(b) deben "
            f"tener signos opuestos (f({a})={f(a)}, f({b})={f(b)})."
        )


def validar_intervalo(a: float, b: float) -> None:
    """Valida que `a` sea estrictamente menor que `b`.

    Args:
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.

    Raises:
        EntradaInvalidaError: Si a >= b.
    """
    if a >= b:
        raise EntradaInvalidaError(
            f"El intervalo es inválido: a ({a}) debe ser menor que b ({b})."
        )


def validar_misma_longitud(*listas: list) -> None:
    """Valida que todas las listas recibidas tengan la misma longitud.

    Args:
        *listas: Listas a comparar.

    Raises:
        EntradaInvalidaError: Si las longitudes difieren.
    """
    longitudes = {len(lista) for lista in listas}
    if len(longitudes) > 1:
        raise EntradaInvalidaError(
            f"Las listas deben tener la misma longitud, se recibieron: "
            f"{[len(lista) for lista in listas]}."
        )


def validar_max_iteraciones(max_iteraciones: int) -> None:
    """Valida que el número máximo de iteraciones sea positivo.

    Args:
        max_iteraciones: Límite de iteraciones de un método iterativo.

    Raises:
        EntradaInvalidaError: Si max_iteraciones <= 0.
    """
    if max_iteraciones <= 0:
        raise EntradaInvalidaError(
            f"max_iteraciones debe ser mayor a 0, se recibió: {max_iteraciones}."
        )
