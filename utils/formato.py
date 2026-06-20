"""Utilidades de formateo de resultados para mostrar en la interfaz.

Centraliza cómo se presentan tablas de iteraciones, números, etc., para
mantener consistencia visual entre los distintos módulos de `interfaz`.
"""

from __future__ import annotations


def formatear_numero(valor: float, decimales: int = 6) -> str:
    """Formatea un número flotante con un número fijo de decimales.

    Args:
        valor: Número a formatear.
        decimales: Cantidad de decimales a mostrar.

    Returns:
        Representación en cadena de `valor` con `decimales` decimales.
    """
    return f"{valor:.{decimales}f}"


def tabla_iteraciones(encabezados: list[str], filas: list[list]) -> str:
    """Genera una tabla de texto simple a partir de encabezados y filas.

    Pensada para mostrarse en un widget `Text` de Tkinter (fuente
    monoespaciada recomendada).

    Args:
        encabezados: Nombres de columna.
        filas: Lista de filas, cada una con un valor por columna.

    Returns:
        Tabla formateada como texto plano.

    TODO(equipo): mejorar alineación/anchos dinámicos si se requiere.
    """
    lineas = ["\t".join(str(encabezado) for encabezado in encabezados)]
    for fila in filas:
        lineas.append("\t".join(str(valor) for valor in fila))
    return "\n".join(lineas)
