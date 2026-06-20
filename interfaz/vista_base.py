"""Vista base para las sub-ventanas de cada categoría de método.

Cada categoría (raices, interpolacion, etc.) puede heredar de
`VistaBase` para mantener un look-and-feel consistente: un Toplevel con
área de formulario, botón de calcular y área de resultado.

Ejemplo de uso (en interfaz/raices_vista.py, a futuro):

    from interfaz.vista_base import VistaBase

    class VistaBiseccion(VistaBase):
        def __init__(self, master):
            super().__init__(master, titulo="Método de Bisección")
            # agregar campos de formulario propios aquí
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class VistaBase(tk.Toplevel):
    """Ventana secundaria base con estructura formulario + resultado."""

    def __init__(self, master: tk.Misc, titulo: str) -> None:
        super().__init__(master)
        self.title(titulo)
        self.geometry("500x400")

        self.frame_formulario = ttk.Frame(self, padding=15)
        self.frame_formulario.pack(fill="x")

        self.frame_resultado = ttk.LabelFrame(self, text="Resultado", padding=15)
        self.frame_resultado.pack(fill="both", expand=True, padx=15, pady=15)

        self.texto_resultado = tk.Text(
            self.frame_resultado, height=10, state="disabled"
        )
        self.texto_resultado.pack(fill="both", expand=True)

    def mostrar_resultado(self, texto: str) -> None:
        """Escribe `texto` en el área de resultado, reemplazando lo previo."""
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, texto)
        self.texto_resultado.configure(state="disabled")
