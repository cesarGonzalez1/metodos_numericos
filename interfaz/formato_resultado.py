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


def _formatear_lista(valor: list) -> str:
    """Formatea listas: vector solución o lista de tuplas (x, y) de EDO."""
    if valor and isinstance(valor[0], tuple):
        encabezados = ["x", "y"]
        filas = [[_formatear_escalar(x), _formatear_escalar(y)] for x, y in valor]
        return "Solución (x, y):\n" + tabla_iteraciones(encabezados, filas)
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
        elif isinstance(contenido, list):
            elementos = ", ".join(_formatear_escalar(v) for v in contenido)
            lineas.append(f"{clave}: [{elementos}]")
        else:
            lineas.append(f"{clave}: {_formatear_escalar(contenido)}")
    return "\n".join(lineas)
