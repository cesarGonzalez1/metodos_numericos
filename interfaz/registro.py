"""Registro declarativo de categorías y métodos para la interfaz.

Esta es la capa de *conexión* entre la GUI y la lógica de `metodos/`. No
contiene algoritmos: solo describe, de forma declarativa, qué métodos hay en
cada categoría y qué parámetros necesita cada uno. La vista genérica
(`interfaz/vista_categoria.py`) lee este registro para construir los
formularios y llamar a la función correspondiente.

Cada campo declara un ``tipo`` que indica a la vista cómo convertir el texto
del formulario en un valor de Python:

* ``funcion_x``            -> Callable f(x)        (evaluador.crear_funcion_x)
* ``funcion_xy``           -> Callable f(x, y)     (evaluador.crear_funcion_xy)
* ``funcion_xyz``          -> Callable f(x, y, z)  (evaluador.crear_funcion_xyz)
* ``sistema_edo``          -> Callable f(x, y_vec) (evaluador.crear_sistema_edo)
* ``funcion_estado``       -> Callable g(x, *u)    (evaluador.crear_funcion_estado)
* ``lista``                -> list[float]          (evaluador.parsear_lista)
* ``matriz``               -> list[list[float]]    (evaluador.parsear_matriz)
* ``lista_funciones_xy``   -> list[Callable]       (Taylor superior)
* ``float`` / ``int``      -> número
* ``complejo``             -> complex
* ``texto``                -> str (Entry, sin conversión)
* ``opcion``               -> str (Combobox con ``opciones``)
"""

from __future__ import annotations

# Registro de métodos por categoría (sincronizado con el plan de estudios LCD).
from metodos.conversion.analisis_errores import (
    analisis_errores,
    redondeo_y_truncamiento,
)
from metodos.conversion.binario_a_decimal import binario_a_decimal
from metodos.conversion.decimal_a_binario import decimal_a_binario
from metodos.derivacion.cinco_puntos import cinco_puntos
from metodos.derivacion.cuatro_puntos import cuatro_puntos
from metodos.derivacion.diferencias_finitas import derivada
from metodos.derivacion.n_mas_un_puntos import n_mas_un_puntos
from metodos.derivacion.richardson import richardson
from metodos.derivacion.tres_puntos import tres_puntos
from metodos.edo.adams import adams
from metodos.edo.adams_variable import adams_variable
from metodos.edo.euler import euler
from metodos.edo.runge_kutta import runge_kutta
from metodos.edo.runge_kutta_fehlberg import runge_kutta_fehlberg
from metodos.edo.sistemas import orden_superior, resolver_sistema
from metodos.edo.taylor_superior import taylor_superior
from metodos.integracion.cuadratura_adaptativa import cuadratura_adaptativa
from metodos.integracion.cuadratura_gaussiana import cuadratura_gaussiana
from metodos.integracion.cuadratura_gaussiana_doble import cuadratura_gaussiana_doble
from metodos.integracion.cuadratura_gaussiana_triple import (
    cuadratura_gaussiana_triple,
)
from metodos.integracion.integral_doble_simpson import integral_doble_simpson
from metodos.integracion.punto_medio import punto_medio
from metodos.integracion.punto_medio_compuesto import punto_medio_compuesto
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
from metodos.interpolacion.aproximacion_polinomial import aproximacion_polinomial
from metodos.interpolacion.diferencias_divididas import diferencias_divididas
from metodos.interpolacion.fourier import fourier
from metodos.interpolacion.hermite import hermite
from metodos.interpolacion.interpolacion_basica import interpolacion_basica
from metodos.interpolacion.lagrange import lagrange
from metodos.interpolacion.minimos_cuadrados import minimos_cuadrados
from metodos.interpolacion.neville import neville
from metodos.interpolacion.regresion_multiple import regresion_multiple
from metodos.interpolacion.regresion_no_lineal import regresion_no_lineal
from metodos.interpolacion.splines_cubicos import splines_cubicos
from metodos.interpolacion.taylor import taylor
from metodos.matrices.cholesky import cholesky, resolver_cholesky
from metodos.matrices.crout import crout, resolver_crout
from metodos.matrices.eliminacion_aritmetica import eliminacion_aritmetica
from metodos.matrices.eliminacion_gaussiana import eliminacion_gaussiana
from metodos.matrices.factorizacion_ldl import factorizacion_ldl, resolver_ldl
from metodos.matrices.factorizacion_lu import factorizacion_lu, resolver_lu
from metodos.matrices.inversa import inversa
from metodos.matrices.pivoteo_escalado import pivoteo_escalado
from metodos.matrices.pivoteo_parcial import pivoteo_parcial
from metodos.raices.bairstow import bairstow
from metodos.raices.biseccion import biseccion
from metodos.raices.deflacion import deflacion
from metodos.raices.falsa_posicion import falsa_posicion
from metodos.raices.muller import muller
from metodos.raices.newton_raphson import newton_raphson
from metodos.raices.punto_fijo import punto_fijo
from metodos.raices.secante import secante


def _campo(clave, etiqueta, tipo, default="", opciones=None):
    """Crea la descripción de un campo de formulario."""
    campo = {"clave": clave, "etiqueta": etiqueta, "tipo": tipo, "default": default}
    if opciones is not None:
        campo["opciones"] = opciones
    return campo


# Campos comunes reutilizables.
_TOL = _campo("tolerancia", "Tolerancia", "float", "1e-6")
_MAXIT = _campo("max_iteraciones", "Máx. iteraciones", "int", "100")


def _campos_integral_simple(f_default: str) -> list[dict]:
    """Campos para una regla de integración simple: f(x), a, b."""
    return [
        _campo("f", "f(x)", "funcion_x", f_default),
        _campo("a", "a", "float", "0"),
        _campo("b", "b", "float", "2"),
    ]


def _campos_integral_n(f_default: str, n_default: str) -> list[dict]:
    """Campos para una regla compuesta: f(x), a, b, n."""
    return _campos_integral_simple(f_default) + [
        _campo("n", "n subintervalos", "int", n_default)
    ]


def _campos_edo_n(f_default: str) -> list[dict]:
    """Campos para un método de EDO de paso fijo: f(x, y), x0, y0, x_final, n."""
    return [
        _campo("f", "f(x, y)", "funcion_xy", f_default),
        _campo("x0", "x0", "float", "0"),
        _campo("y0", "y0", "float", "1"),
        _campo("x_final", "x final", "float", "1"),
        _campo("n", "n pasos", "int", "100"),
    ]


def _campos_sistema() -> list[dict]:
    """Campos para un solucionador de sistemas lineales: matriz A y vector b."""
    return [
        _campo("matriz_a", "Matriz A (filas con ; )", "matriz", "2 1; 1 3"),
        _campo("vector_b", "Vector b", "lista", "3, 4"),
    ]


# Estructura: lista ordenada de (categoria, lista de métodos).
# Cada método: {"nombre", "funcion", "campos"}.
CATEGORIAS: list[tuple[str, list[dict]]] = [
    (
        "Conversión",
        [
            {
                "nombre": "Análisis de errores",
                "funcion": analisis_errores,
                "campos": [
                    _campo("valor_verdadero", "Valor verdadero", "float", "3.14159265"),
                    _campo("valor_aproximado", "Valor aproximado", "float", "3.14"),
                ],
            },
            {
                "nombre": "Redondeo y truncamiento",
                "funcion": redondeo_y_truncamiento,
                "campos": [
                    _campo("numero", "Número", "float", "3.14159265"),
                    _campo("decimales", "Decimales", "int", "4"),
                ],
            },
            {
                "nombre": "Decimal a binario",
                "funcion": decimal_a_binario,
                "campos": [
                    _campo("numero", "Número decimal", "float", "12.625"),
                    _campo(
                        "precision",
                        "Precisión IEEE 754",
                        "opcion",
                        "doble",
                        ["doble", "simple"],
                    ),
                ],
            },
            {
                "nombre": "Binario a decimal",
                "funcion": binario_a_decimal,
                "campos": [
                    _campo(
                        "bits",
                        "Binario (bits o entera.fracc.)",
                        "texto",
                        "1010.101",
                    ),
                    _campo(
                        "precision",
                        "Precisión IEEE 754",
                        "opcion",
                        "doble",
                        ["doble", "simple"],
                    ),
                ],
            },
        ],
    ),
    (
        "Raíces",
        [
            {
                "nombre": "Bisección",
                "funcion": biseccion,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2 - 2"),
                    _campo("a", "a", "float", "0"),
                    _campo("b", "b", "float", "2"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Falsa posición",
                "funcion": falsa_posicion,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**3 - x - 2"),
                    _campo("a", "a", "float", "1"),
                    _campo("b", "b", "float", "2"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Punto fijo",
                "funcion": punto_fijo,
                "campos": [
                    _campo("g", "g(x)", "funcion_x", "cos(x)"),
                    _campo("x0", "x0", "float", "0.5"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Newton-Raphson",
                "funcion": newton_raphson,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2 - 2"),
                    _campo("df", "f'(x)", "funcion_x", "2*x"),
                    _campo("x0", "x0", "float", "1.5"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Secante",
                "funcion": secante,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2 - 2"),
                    _campo("x0", "x0", "float", "1"),
                    _campo("x1", "x1", "float", "2"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Müller",
                "funcion": muller,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2 + 1"),
                    _campo("x0", "x0", "complejo", "0"),
                    _campo("x1", "x1", "complejo", "0.5j"),
                    _campo("x2", "x2", "complejo", "1j"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Bairstow",
                "funcion": bairstow,
                "campos": [
                    _campo("coeficientes", "Coeficientes (desc.)", "lista", "1, 0, 1"),
                    _campo("r", "r inicial", "float", "1"),
                    _campo("s", "s inicial", "float", "1"),
                    _TOL,
                    _MAXIT,
                ],
            },
            {
                "nombre": "Deflación",
                "funcion": deflacion,
                "campos": [
                    _campo("coeficientes", "Coeficientes (desc.)", "lista", "1, -3, 2"),
                    _campo("raiz", "Raíz", "complejo", "1"),
                ],
            },
        ],
    ),
    (
        "Interpolación",
        [
            {
                "nombre": "Interpolación básica",
                "funcion": interpolacion_basica,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "0, 1, 2"),
                    _campo("y_datos", "y (valores)", "lista", "0, 10, 20"),
                    _campo("x_evaluar", "x a evaluar", "float", "0.5"),
                ],
            },
            {
                "nombre": "Polinomio de Lagrange",
                "funcion": lagrange,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "0, 1, 2"),
                    _campo("y_datos", "y (valores)", "lista", "1, 3, 7"),
                    _campo("x_evaluar", "x a evaluar", "float", "1.5"),
                ],
            },
            {
                "nombre": "Interpolación de Neville",
                "funcion": neville,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "1, 2, 3"),
                    _campo("y_datos", "y (valores)", "lista", "1, 4, 9"),
                    _campo("x_evaluar", "x a evaluar", "float", "2.5"),
                ],
            },
            {
                "nombre": "Diferencias divididas",
                "funcion": diferencias_divididas,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "0, 1, 2"),
                    _campo("y_datos", "y (valores)", "lista", "1, 3, 7"),
                    _campo("x_evaluar", "x a evaluar", "float", "1.5"),
                ],
            },
            {
                "nombre": "Polinomio de Taylor",
                "funcion": taylor,
                "campos": [
                    _campo("derivadas", "Derivadas en x0", "lista", "1, 1, 1, 1"),
                    _campo("x0", "x0 (centro)", "float", "0"),
                    _campo("x_evaluar", "x a evaluar", "float", "1"),
                ],
            },
            {
                "nombre": "Mínimos cuadrados (lineal)",
                "funcion": minimos_cuadrados,
                "campos": [
                    _campo("x_datos", "x", "lista", "0, 1, 2, 3"),
                    _campo("y_datos", "y", "lista", "1, 3, 5, 7"),
                ],
            },
            {
                "nombre": "Aproximación polinómica",
                "funcion": aproximacion_polinomial,
                "campos": [
                    _campo("x_datos", "x", "lista", "0, 1, 2, 3"),
                    _campo("y_datos", "y", "lista", "0, 1, 4, 9"),
                    _campo("grado", "Grado", "int", "2"),
                ],
            },
            {
                "nombre": "Regresión lineal múltiple",
                "funcion": regresion_multiple,
                "campos": [
                    _campo(
                        "x_datos",
                        "Observaciones (filas con ; )",
                        "matriz",
                        "1 1; 2 1; 1 2; 3 2",
                    ),
                    _campo("y_datos", "y", "lista", "6, 8, 9, 11"),
                ],
            },
            {
                "nombre": "Regresión no lineal",
                "funcion": regresion_no_lineal,
                "campos": [
                    _campo("x_datos", "x", "lista", "0, 1, 2, 3"),
                    _campo("y_datos", "y (> 0)", "lista", "2, 3.3, 5.4, 9"),
                    _campo(
                        "modelo",
                        "Modelo",
                        "opcion",
                        "exponencial",
                        ["exponencial", "potencia"],
                    ),
                ],
            },
            {
                "nombre": "Interpolación de Hermite",
                "funcion": hermite,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "1, 2"),
                    _campo("y_datos", "f(x)", "lista", "1, 4"),
                    _campo("derivadas", "f'(x)", "lista", "2, 4"),
                    _campo("x_evaluar", "x a evaluar", "float", "1.5"),
                ],
            },
            {
                "nombre": "Trazadores cúbicos (splines)",
                "funcion": splines_cubicos,
                "campos": [
                    _campo("x_datos", "x (nodos)", "lista", "0, 1, 2, 3"),
                    _campo("y_datos", "y (valores)", "lista", "0, 1, 4, 9"),
                    _campo("x_evaluar", "x a evaluar", "float", "1.5"),
                ],
            },
            {
                "nombre": "Aproximación de Fourier",
                "funcion": fourier,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2"),
                    _campo("a", "a", "float", "-3.14159265"),
                    _campo("b", "b", "float", "3.14159265"),
                    _campo("m", "m (muestras = 2m)", "int", "16"),
                    _campo("n", "Grado n (< m)", "int", "4"),
                    _campo("x_evaluar", "x a evaluar", "float", "1.0"),
                ],
            },
        ],
    ),
    (
        "Derivación",
        [
            {
                "nombre": "Derivación general",
                "funcion": derivada,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2"),
                    _campo("x", "x", "float", "3"),
                    _campo("h", "h", "float", "1e-5"),
                    _campo(
                        "tipo",
                        "Tipo",
                        "opcion",
                        "centrada",
                        ["centrada", "adelante", "atras"],
                    ),
                ],
            },
            {
                "nombre": "Fórmula general de n+1 puntos",
                "funcion": n_mas_un_puntos,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "sin(x)"),
                    _campo("x", "x", "float", "0.3"),
                    _campo("h", "h", "float", "0.01"),
                    _campo("puntos", "n+1 puntos", "int", "7"),
                    _campo(
                        "alineacion",
                        "Plantilla",
                        "opcion",
                        "centrada",
                        ["centrada", "adelante", "atras"],
                    ),
                ],
            },
            {
                "nombre": "Fórmula de 3 puntos",
                "funcion": tres_puntos,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**2"),
                    _campo("x", "x", "float", "3"),
                    _campo("h", "h", "float", "1e-4"),
                    _campo(
                        "tipo",
                        "Tipo",
                        "opcion",
                        "medio",
                        ["medio", "adelante", "atras"],
                    ),
                ],
            },
            {
                "nombre": "Fórmula de 4 puntos",
                "funcion": cuatro_puntos,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**3"),
                    _campo("x", "x", "float", "2"),
                    _campo("h", "h", "float", "1e-3"),
                    _campo(
                        "tipo",
                        "Tipo",
                        "opcion",
                        "adelante",
                        ["adelante", "atras"],
                    ),
                ],
            },
            {
                "nombre": "Fórmula de 5 puntos",
                "funcion": cinco_puntos,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**4"),
                    _campo("x", "x", "float", "2"),
                    _campo("h", "h", "float", "1e-2"),
                    _campo("tipo", "Tipo", "opcion", "medio", ["medio", "adelante"]),
                ],
            },
            {
                "nombre": "Extrapolación de Richardson",
                "funcion": richardson,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**3"),
                    _campo("x", "x", "float", "2"),
                    _campo("h", "h inicial", "float", "0.1"),
                    _campo("niveles", "Niveles", "int", "4"),
                ],
            },
        ],
    ),
    (
        "Integración",
        [
            {
                "nombre": "Trapecio",
                "funcion": trapecio,
                "campos": _campos_integral_simple("x"),
            },
            {
                "nombre": "Punto medio",
                "funcion": punto_medio,
                "campos": _campos_integral_simple("x"),
            },
            {
                "nombre": "Punto medio compuesto",
                "funcion": punto_medio_compuesto,
                "campos": _campos_integral_n("x**2", "100"),
            },
            {
                "nombre": "Simpson 1/3",
                "funcion": simpson_un_tercio,
                "campos": _campos_integral_simple("x**2"),
            },
            {
                "nombre": "Simpson 3/8",
                "funcion": simpson_tres_octavos,
                "campos": _campos_integral_simple("x**2"),
            },
            {
                "nombre": "Trapecio compuesto",
                "funcion": trapecio_compuesto,
                "campos": _campos_integral_n("x**2", "100"),
            },
            {
                "nombre": "Simpson 1/3 compuesto",
                "funcion": simpson_un_tercio_compuesto,
                "campos": _campos_integral_n("sin(x)", "100"),
            },
            {
                "nombre": "Simpson 3/8 compuesto",
                "funcion": simpson_tres_octavos_compuesto,
                "campos": _campos_integral_n("x**3", "99"),
            },
            {
                "nombre": "Romberg",
                "funcion": romberg,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**3"),
                    _campo("a", "a", "float", "0"),
                    _campo("b", "b", "float", "2"),
                    _campo("niveles", "Niveles", "int", "5"),
                ],
            },
            {
                "nombre": "Cuadratura adaptativa",
                "funcion": cuadratura_adaptativa,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "sin(x)"),
                    _campo("a", "a", "float", "0"),
                    _campo("b", "b", "float", "3.14159265"),
                    _campo("tolerancia", "Tolerancia", "float", "1e-8"),
                ],
            },
            {
                "nombre": "Cuadratura gaussiana",
                "funcion": cuadratura_gaussiana,
                "campos": [
                    _campo("f", "f(x)", "funcion_x", "x**3"),
                    _campo("a", "a", "float", "0"),
                    _campo("b", "b", "float", "2"),
                    _campo("puntos", "Puntos (2-5)", "int", "3"),
                ],
            },
            {
                "nombre": "Integral doble de Simpson",
                "funcion": integral_doble_simpson,
                "campos": [
                    _campo("f", "f(x, y)", "funcion_xy", "x*y"),
                    _campo("a", "a (x inf.)", "float", "0"),
                    _campo("b", "b (x sup.)", "float", "2"),
                    _campo("c", "c (y inf.)", "float", "0"),
                    _campo("d", "d (y sup.)", "float", "1"),
                    _campo("n", "n subint. x (par)", "int", "4"),
                    _campo("m", "m subint. y (par)", "int", "4"),
                ],
            },
            {
                "nombre": "Cuadratura gaussiana doble",
                "funcion": cuadratura_gaussiana_doble,
                "campos": [
                    _campo("f", "f(x, y)", "funcion_xy", "x**2 + y**2"),
                    _campo("a", "a (x inf.)", "float", "0"),
                    _campo("b", "b (x sup.)", "float", "1"),
                    _campo("c", "c (y inf.)", "float", "0"),
                    _campo("d", "d (y sup.)", "float", "1"),
                    _campo("puntos", "Puntos por eje (2-5)", "int", "3"),
                ],
            },
            {
                "nombre": "Cuadratura gaussiana triple",
                "funcion": cuadratura_gaussiana_triple,
                "campos": [
                    _campo("f", "f(x, y, z)", "funcion_xyz", "x + y + z"),
                    _campo("a", "a (x inf.)", "float", "0"),
                    _campo("b", "b (x sup.)", "float", "1"),
                    _campo("c", "c (y inf.)", "float", "0"),
                    _campo("d", "d (y sup.)", "float", "1"),
                    _campo("e", "e (z inf.)", "float", "0"),
                    _campo("g", "g (z sup.)", "float", "1"),
                    _campo("puntos", "Puntos por eje (2-5)", "int", "3"),
                ],
            },
        ],
    ),
    (
        "EDO",
        [
            {
                "nombre": "Euler",
                "funcion": euler,
                "campos": _campos_edo_n("y"),
            },
            {
                "nombre": "Taylor de orden superior",
                "funcion": taylor_superior,
                "campos": [
                    _campo(
                        "derivadas",
                        "Derivadas f, f', ... (sep. ;)",
                        "lista_funciones_xy",
                        "y; y",
                    ),
                    _campo("x0", "x0", "float", "0"),
                    _campo("y0", "y0", "float", "1"),
                    _campo("x_final", "x final", "float", "1"),
                    _campo("n", "n pasos", "int", "100"),
                ],
            },
            {
                "nombre": "Runge-Kutta 4",
                "funcion": runge_kutta,
                "campos": _campos_edo_n("y"),
            },
            {
                "nombre": "Runge-Kutta-Fehlberg",
                "funcion": runge_kutta_fehlberg,
                "campos": [
                    _campo("f", "f(x, y)", "funcion_xy", "y"),
                    _campo("x0", "x0", "float", "0"),
                    _campo("y0", "y0", "float", "1"),
                    _campo("x_final", "x final", "float", "1"),
                    _campo("tolerancia", "Tolerancia", "float", "1e-6"),
                ],
            },
            {
                "nombre": "Adams (multipaso, predictor-corrector)",
                "funcion": adams,
                "campos": _campos_edo_n("y"),
            },
            {
                "nombre": "Adams con paso variable",
                "funcion": adams_variable,
                "campos": [
                    _campo("f", "f(x, y)", "funcion_xy", "y"),
                    _campo("x0", "x0", "float", "0"),
                    _campo("y0", "y0", "float", "1"),
                    _campo("x_final", "x final", "float", "1"),
                    _campo("tolerancia", "Tolerancia local", "float", "1e-6"),
                    _campo("h_inicial", "h inicial", "float", "0.08"),
                    _campo("h_min", "h mínimo", "float", "1e-8"),
                    _campo("h_max", "h máximo", "float", "0.2"),
                ],
            },
            {
                "nombre": "Sistema de EDO (RK4)",
                "funcion": resolver_sistema,
                "campos": [
                    _campo(
                        "f",
                        "Ecuaciones y1', y2', ... (sep. ;)",
                        "sistema_edo",
                        "y2; -y1",
                    ),
                    _campo("x0", "x0", "float", "0"),
                    _campo("y0", "y0 (vector)", "lista", "0, 1"),
                    _campo("x_final", "x final", "float", "6.283185"),
                    _campo("n", "n pasos", "int", "200"),
                ],
            },
            {
                "nombre": "Ecuación de orden superior (RK4)",
                "funcion": orden_superior,
                "campos": [
                    _campo(
                        "g",
                        "y^(m) = g(x, y0, y1, ...)",
                        "funcion_estado",
                        "-y0",
                    ),
                    _campo("x0", "x0", "float", "0"),
                    _campo(
                        "condiciones_iniciales",
                        "y(x0), y'(x0), ...",
                        "lista",
                        "0, 1",
                    ),
                    _campo("x_final", "x final", "float", "6.283185"),
                    _campo("n", "n pasos", "int", "200"),
                ],
            },
        ],
    ),
    (
        "Sistemas lineales",
        [
            {
                "nombre": "Eliminación gaussiana",
                "funcion": eliminacion_gaussiana,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Eliminación aritmética (Gauss-Jordan)",
                "funcion": eliminacion_aritmetica,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Pivoteo parcial",
                "funcion": pivoteo_parcial,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Pivoteo escalado",
                "funcion": pivoteo_escalado,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Solución por LU (Doolittle)",
                "funcion": resolver_lu,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Solución por Crout",
                "funcion": resolver_crout,
                "campos": _campos_sistema(),
            },
            {
                "nombre": "Solución por Cholesky (sim. def. pos.)",
                "funcion": resolver_cholesky,
                "campos": [
                    _campo("matriz_a", "Matriz A (filas con ; )", "matriz", "4 2; 2 2"),
                    _campo("vector_b", "Vector b", "lista", "6, 4"),
                ],
            },
            {
                "nombre": "Solución por LDLᵀ (simétrica)",
                "funcion": resolver_ldl,
                "campos": [
                    _campo("matriz_a", "Matriz A (filas con ; )", "matriz", "4 2; 2 2"),
                    _campo("vector_b", "Vector b", "lista", "6, 4"),
                ],
            },
            {
                "nombre": "Inversa de matriz",
                "funcion": inversa,
                "campos": [
                    _campo(
                        "matriz_a",
                        "Matriz A (filas con ; )",
                        "matriz",
                        "4 7; 2 6",
                    ),
                ],
            },
        ],
    ),
    (
        "Factorización",
        [
            {
                "nombre": "Factorización LU (Doolittle)",
                "funcion": factorizacion_lu,
                "campos": [
                    _campo(
                        "matriz_a",
                        "Matriz A (filas con ; )",
                        "matriz",
                        "4 3; 6 3",
                    ),
                ],
            },
            {
                "nombre": "Factorización de Crout",
                "funcion": crout,
                "campos": [
                    _campo(
                        "matriz_a",
                        "Matriz A (filas con ; )",
                        "matriz",
                        "2 1 1; 4 3 3; 8 7 9",
                    ),
                ],
            },
            {
                "nombre": "Factorización de Cholesky",
                "funcion": cholesky,
                "campos": [
                    _campo(
                        "matriz_a",
                        "Matriz A (sim. def. pos.)",
                        "matriz",
                        "25 15 -5; 15 18 0; -5 0 11",
                    ),
                ],
            },
            {
                "nombre": "Factorización LDLᵀ",
                "funcion": factorizacion_ldl,
                "campos": [
                    _campo(
                        "matriz_a",
                        "Matriz A (simétrica)",
                        "matriz",
                        "4 12 -16; 12 37 -43; -16 -43 98",
                    ),
                ],
            },
        ],
    ),
]
