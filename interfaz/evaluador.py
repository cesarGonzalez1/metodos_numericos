"""Evaluador seguro de expresiones para la interfaz.

Convierte el texto que el usuario escribe (p. ej. ``x**2 + sin(x)``) en
funciones de Python invocables. Pertenece a la capa de presentación: su
única responsabilidad es traducir entrada de texto a `Callable`, sin
contener lógica numérica.

Por seguridad, las expresiones se evalúan con los ``__builtins__``
deshabilitados y un espacio de nombres restringido a funciones de `math`.
"""

from __future__ import annotations

import math
from collections.abc import Callable

# Espacio de nombres permitido: funciones y constantes de `math` + utilidades.
_NOMBRES_PERMITIDOS: dict[str, object] = {
    nombre: getattr(math, nombre) for nombre in dir(math) if not nombre.startswith("_")
}
_NOMBRES_PERMITIDOS.update({"abs": abs, "min": min, "max": max, "pow": pow})


class ExpresionInvalidaError(ValueError):
    """Se lanza cuando una expresión no puede compilarse o evaluarse."""


def _compilar(expresion: str) -> object:
    """Compila la expresión, validando que sea sintácticamente correcta."""
    if not isinstance(expresion, str) or not expresion.strip():
        raise ExpresionInvalidaError("La expresión no puede estar vacía.")
    try:
        # Se recorta para evitar errores de "unexpected indent" por espacios.
        return compile(expresion.strip(), "<expresion>", "eval")
    except SyntaxError as exc:
        raise ExpresionInvalidaError(f"Expresión inválida: {exc.msg}.") from exc


def _evaluar(codigo: object, entorno: dict[str, object]) -> object:
    """Evalúa código solo si todos sus nombres aparecen en el entorno seguro.

    Deshabilitar ``__builtins__`` no basta por sí solo: el acceso a atributos
    de objetos puede reconstruir clases internas de Python. ``co_names``
    incluye tanto nombres globales como atributos, así que rechazar cualquier
    nombre que no esté expresamente autorizado cierra también esa vía.
    """
    usados = set(getattr(codigo, "co_names", ()))
    desconocidos = usados - set(entorno)
    if desconocidos:
        lista = ", ".join(sorted(desconocidos))
        raise ExpresionInvalidaError(f"Nombre o atributo no permitido: {lista}.")
    return eval(codigo, {"__builtins__": {}}, entorno)


def crear_funcion_x(expresion: str) -> Callable[[float], float]:
    """Crea una función de una variable f(x) a partir de texto.

    Args:
        expresion: Cadena con la expresión en términos de ``x``.

    Returns:
        Función ``f(x) -> float``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def f(x: float) -> float:
        return _evaluar(codigo, {**_NOMBRES_PERMITIDOS, "x": x})

    return f


def crear_funcion_xy(expresion: str) -> Callable[[float, float], float]:
    """Crea una función de dos variables f(x, y) a partir de texto.

    Args:
        expresion: Cadena con la expresión en términos de ``x`` e ``y``.

    Returns:
        Función ``f(x, y) -> float``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def f(x: float, y: float) -> float:
        return _evaluar(codigo, {**_NOMBRES_PERMITIDOS, "x": x, "y": y})

    return f


def crear_funcion_xyz(expresion: str) -> Callable[[float, float, float], float]:
    """Crea una función de tres variables f(x, y, z) a partir de texto.

    Útil para integrales triples.

    Args:
        expresion: Cadena en términos de ``x``, ``y`` y ``z``.

    Returns:
        Función ``f(x, y, z) -> float``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def f(x: float, y: float, z: float) -> float:
        return _evaluar(codigo, {**_NOMBRES_PERMITIDOS, "x": x, "y": y, "z": z})

    return f


def crear_sistema_edo(texto: str) -> Callable[[float, object], list[float]]:
    """Crea la función de un sistema de EDO a partir de varias expresiones.

    Cada ecuación se separa con ``;`` y se escribe en términos de ``x`` y de
    las componentes del estado ``y1, y2, ...`` (1-indexadas). El número de
    ecuaciones determina el tamaño del sistema.

    Ejemplo: ``"y2; -y1"`` representa  y1' = y2,  y2' = -y1.

    Returns:
        Función ``f(x, y) -> list[float]`` donde ``y`` es el vector de estado.

    Raises:
        ExpresionInvalidaError: Si no hay expresiones o alguna no compila.
    """
    partes = [parte for parte in texto.split(";") if parte.strip()]
    if not partes:
        raise ExpresionInvalidaError("Debe ingresar al menos una ecuación.")
    codigos = [_compilar(parte) for parte in partes]
    m = len(codigos)

    def f(x: float, y: object) -> list[float]:
        nombres = {f"y{i + 1}": y[i] for i in range(m)}
        entorno = {**_NOMBRES_PERMITIDOS, "x": x, **nombres}
        return [_evaluar(codigo, entorno) for codigo in codigos]

    return f


def crear_funcion_estado(expresion: str) -> Callable[..., float]:
    """Crea la función de la derivada de mayor orden de una EDO de orden m.

    Para  y^{(m)} = g(x, y, y', ..., y^{(m-1)})  la expresión se escribe en
    términos de ``x`` y del estado ``y0 = y, y1 = y', y2 = y'', ...``.

    Ejemplo: ``"-y0"`` representa  y'' = −y  (con estado y0=y, y1=y').

    Returns:
        Función ``g(x, *u) -> float`` con ``u = (y, y', ..., y^{(m-1)})``.

    Raises:
        ExpresionInvalidaError: Si la expresión no compila.
    """
    codigo = _compilar(expresion)

    def g(x: float, *u: float) -> float:
        nombres = {f"y{i}": u[i] for i in range(len(u))}
        return _evaluar(codigo, {**_NOMBRES_PERMITIDOS, "x": x, **nombres})

    return g


def parsear_lista(texto: str) -> list[float]:
    """Convierte ``"1, 2, 3"`` o ``"1 2 3"`` en ``[1.0, 2.0, 3.0]``.

    Raises:
        ExpresionInvalidaError: Si algún elemento no es numérico.
    """
    crudo = texto.replace(",", " ").split()
    if not crudo:
        raise ExpresionInvalidaError("La lista de valores está vacía.")
    try:
        return [float(valor) for valor in crudo]
    except ValueError as exc:
        raise ExpresionInvalidaError(
            "La lista debe contener solo números separados por comas o espacios."
        ) from exc


def parsear_matriz(texto: str) -> list[list[float]]:
    """Convierte filas (una por línea o separadas por ``;``) en una matriz.

    Ejemplo: ``"2 1; 1 3"`` -> ``[[2.0, 1.0], [1.0, 3.0]]``.

    Raises:
        ExpresionInvalidaError: Si hay valores no numéricos o filas vacías.
    """
    filas_texto = [
        fila for fila in texto.replace(";", "\n").splitlines() if fila.strip()
    ]
    if not filas_texto:
        raise ExpresionInvalidaError("La matriz está vacía.")
    return [parsear_lista(fila) for fila in filas_texto]


def parsear_lista_funciones_xy(texto: str) -> list[Callable[[float, float], float]]:
    """Convierte expresiones separadas por ``;`` en funciones f(x, y).

    Útil para el método de Taylor de orden superior, que recibe la lista de
    derivadas totales como funciones.
    """
    partes = [parte for parte in texto.split(";") if parte.strip()]
    if not partes:
        raise ExpresionInvalidaError("Debe ingresar al menos una función.")
    return [crear_funcion_xy(parte) for parte in partes]
