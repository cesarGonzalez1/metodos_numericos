"""Formateo de los resultados de los métodos para mostrarlos en la GUI.

Traduce los distintos contratos de retorno del proyecto (escalares, listas,
listas de tuplas, diccionarios con tablas o historiales) a texto plano apto
para un widget `Text`. No depende de Tkinter, por lo que puede probarse en
entornos sin display.
"""

from __future__ import annotations

from utils.formato import formatear_numero, tabla_iteraciones


def formatear_resultado(valor: object) -> str:
    """Convierte el valor devuelto por un método en texto legible.

    Soporta escalares, listas (vectores solución), listas de tuplas
    (soluciones de EDO) y diccionarios con campos escalares, tablas o
    historiales.
    """
    if isinstance(valor, dict):
        return _formatear_dict(valor)
    if isinstance(valor, list):
        return _formatear_lista(valor)
    if isinstance(valor, float):
        return f"Resultado: {formatear_numero(valor)}"
    return f"Resultado: {valor}"


def _formatear_escalar(valor: object) -> str:
    """Formatea un escalar (float con decimales fijos; otros tal cual)."""
    if isinstance(valor, float):
        return formatear_numero(valor)
    return str(valor)


def _es_matriz(valor: object) -> bool:
    """Indica si `valor` es una lista de listas (matriz numérica)."""
    return (
        isinstance(valor, list)
        and len(valor) > 0
        and all(isinstance(fila, (list, tuple)) for fila in valor)
    )


def _formatear_matriz(matriz: list) -> str:
    """Formatea una matriz (lista de listas) como tabla alineada."""
    filas = [[_formatear_escalar(v) for v in fila] for fila in matriz]
    encabezados = [f"c{j}" for j in range(len(filas[0]))]
    return tabla_iteraciones(encabezados, filas)


def _formatear_solucion_edo(valor: list) -> str:
    """Formatea una lista de pasos (x, y) o (x, (y1, ..., ym)) de una EDO."""
    primero = valor[0]
    # Sistema: (x, (y1, ..., ym)) -> una columna por componente.
    if isinstance(primero[1], (tuple, list)):
        m = len(primero[1])
        encabezados = ["x"] + [f"y{k + 1}" for k in range(m)]
        filas = [
            [_formatear_escalar(x)] + [_formatear_escalar(c) for c in comps]
            for x, comps in valor
        ]
        return "Solución del sistema:\n" + tabla_iteraciones(encabezados, filas)
    # EDO escalar: (x, y).
    encabezados = ["x", "y"]
    filas = [[_formatear_escalar(x), _formatear_escalar(y)] for x, y in valor]
    return "Solución (x, y):\n" + tabla_iteraciones(encabezados, filas)


def _formatear_lista(valor: list) -> str:
    """Formatea listas: vector solución o lista de tuplas (x, y) de EDO."""
    if valor and isinstance(valor[0], tuple):
        return _formatear_solucion_edo(valor)
    return "Solución: [" + ", ".join(_formatear_escalar(v) for v in valor) + "]"


def _formatear_dict(valor: dict) -> str:
    """Formatea diccionarios: escalares + tablas/historiales si los hay."""
    lineas: list[str] = []
    for clave, contenido in valor.items():
        if clave == "historial" and contenido:
            encabezados = list(contenido[0].keys())
            filas = [
                [_formatear_escalar(fila[col]) for col in encabezados]
                for fila in contenido
            ]
            lineas.append("Historial:\n" + tabla_iteraciones(encabezados, filas))
        elif clave == "tabla" and contenido:
            filas = [[_formatear_escalar(v) for v in fila] for fila in contenido]
            encabezados = [str(i) for i in range(len(filas[0]))]
            lineas.append("Tabla:\n" + tabla_iteraciones(encabezados, filas))
        elif (
            clave == "solucion"
            and isinstance(contenido, list)
            and contenido
            and (isinstance(contenido[0], tuple))
        ):
            lineas.append(_formatear_solucion_edo(contenido))
        elif _es_matriz(contenido):
            lineas.append(f"{clave}:\n" + _formatear_matriz(contenido))
        elif isinstance(contenido, list):
            elementos = ", ".join(_formatear_escalar(v) for v in contenido)
            lineas.append(f"{clave}: [{elementos}]")
        else:
            lineas.append(f"{clave}: {_formatear_escalar(contenido)}")
    return "\n".join(lineas)
