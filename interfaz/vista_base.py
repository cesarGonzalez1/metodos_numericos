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

from interfaz.tema import AZUL_NOCHE, BLANCO, BORDE, centrar, configurar_tema


class VistaBase(tk.Toplevel):
    """Ventana secundaria base con estructura formulario + resultado."""

    def __init__(self, master: tk.Misc, titulo: str) -> None:
        super().__init__(master)
        self.title(titulo)
        configurar_tema(self)
        self.minsize(820, 600)
        centrar(self, 1040, 760)

        cabecera = tk.Frame(self, background=AZUL_NOCHE, padx=22, pady=13)
        cabecera.pack(fill="x")
        tk.Label(
            cabecera,
            text=titulo,
            background=AZUL_NOCHE,
            foreground=BLANCO,
            font=("Segoe UI Semibold", 16),
        ).pack(anchor="w")

        cuerpo = ttk.Panedwindow(self, orient="horizontal")
        cuerpo.pack(fill="both", expand=True, padx=16, pady=16)
        panel_formulario = ttk.Frame(cuerpo, style="Card.TFrame")
        self.panel_salida = ttk.Frame(cuerpo)
        cuerpo.add(panel_formulario, weight=2)
        cuerpo.add(self.panel_salida, weight=3)

        # El formulario puede tener hasta ocho campos (integrales triples).
        # Un lienzo desplazable evita recortes en pantallas pequeñas.
        lienzo = tk.Canvas(
            panel_formulario,
            background=BLANCO,
            highlightthickness=0,
            borderwidth=0,
        )
        barra_formulario = ttk.Scrollbar(
            panel_formulario, orient="vertical", command=lienzo.yview
        )
        lienzo.configure(yscrollcommand=barra_formulario.set)
        lienzo.pack(side="left", fill="both", expand=True)
        barra_formulario.pack(side="right", fill="y")
        self.frame_formulario = ttk.Frame(lienzo, padding=16, style="Card.TFrame")
        ventana_formulario = lienzo.create_window(
            (0, 0), window=self.frame_formulario, anchor="nw"
        )
        self.frame_formulario.bind(
            "<Configure>",
            lambda _e: lienzo.configure(scrollregion=lienzo.bbox("all")),
        )
        lienzo.bind(
            "<Configure>",
            lambda e: lienzo.itemconfigure(ventana_formulario, width=e.width),
        )

        def desplazar(evento: tk.Event) -> None:
            lienzo.yview_scroll(int(-evento.delta / 120), "units")

        lienzo.bind("<Enter>", lambda _e: lienzo.bind_all("<MouseWheel>", desplazar))
        lienzo.bind("<Leave>", lambda _e: lienzo.unbind_all("<MouseWheel>"))

        self.notebook = ttk.Notebook(self.panel_salida)
        self.notebook.pack(fill="both", expand=True)
        self.frame_resultado = ttk.Frame(self.notebook, padding=8, style="Card.TFrame")
        self.notebook.add(self.frame_resultado, text="Resultado")

        self.texto_resultado = tk.Text(
            self.frame_resultado,
            height=10,
            state="disabled",
            wrap="none",
            font=("Cascadia Mono", 9),
            background=BLANCO,
            foreground="#172B4D",
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDE,
            padx=10,
            pady=10,
        )
        scroll_y = ttk.Scrollbar(
            self.frame_resultado, orient="vertical", command=self.texto_resultado.yview
        )
        scroll_x = ttk.Scrollbar(
            self.frame_resultado,
            orient="horizontal",
            command=self.texto_resultado.xview,
        )
        self.texto_resultado.configure(
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.texto_resultado.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.frame_resultado.rowconfigure(0, weight=1)
        self.frame_resultado.columnconfigure(0, weight=1)

    def mostrar_resultado(self, texto: str) -> None:
        """Escribe `texto` en el área de resultado, reemplazando lo previo."""
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, texto)
        self.texto_resultado.configure(state="disabled")
