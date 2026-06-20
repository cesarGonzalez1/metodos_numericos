"""Validaciones de entrada reutilizables por todos los métodos numéricos.

Mantener aquí cualquier validación que se repita en más de un método para
evitar duplicación (DRY). Cada función debe lanzar
`utils.errores.EntradaInvalidaError` cuando la validación falle.
"""

from __future__ import annotations

from utils.errores import EntradaInvalidaError


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
