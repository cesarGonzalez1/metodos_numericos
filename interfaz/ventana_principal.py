"""Ventana principal de la aplicación.

Ofrece la navegación por categorías de métodos numéricos. Cada botón abre
una `VistaCategoria` (Toplevel) con los métodos de esa categoría. La
ventana principal solo se ocupa de la navegación: la construcción de
formularios y la ejecución de los métodos viven en `interfaz.vista_categoria`,
y los algoritmos en `metodos/`.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from interfaz.registro import CATEGORIAS
from interfaz.vista_categoria import VistaCategoria

APP_TITLE = "Métodos Numéricos"
APP_MIN_WIDTH = 720
APP_MIN_HEIGHT = 480


class VentanaPrincipal(tk.Tk):
    """Ventana raíz de la aplicación.

    Responsable únicamente de la navegación general hacia cada categoría.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self._construir_layout()

    def _construir_layout(self) -> None:
        """Construye el encabezado y los botones de navegación."""
        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text=APP_TITLE, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=(0, 4))

        subtitulo = ttk.Label(
            contenedor,
            text="Selecciona una categoría de método",
        )
        subtitulo.pack(pady=(0, 16))

        # Rejilla de botones, uno por categoría del registro.
        rejilla = ttk.Frame(contenedor)
        rejilla.pack(fill="both", expand=True)
        for indice, (categoria, metodos) in enumerate(CATEGORIAS):
            boton = ttk.Button(
                rejilla,
                text=f"{categoria}  ({len(metodos)})",
                command=lambda c=categoria, m=metodos: self._abrir_categoria(c, m),
            )
            fila, columna = divmod(indice, 2)
            boton.grid(row=fila, column=columna, sticky="ew", padx=6, pady=6, ipady=8)
        rejilla.columnconfigure(0, weight=1)
        rejilla.columnconfigure(1, weight=1)

        pie = ttk.Label(
            contenedor,
            text="Proyecto académico — ESCOM, IPN",
            font=("Segoe UI", 8),
        )
        pie.pack(side="bottom", pady=(16, 0))

    def _abrir_categoria(self, categoria: str, metodos: list[dict]) -> None:
        """Abre la vista de una categoría como ventana secundaria."""
        VistaCategoria(self, categoria, metodos)


if __name__ == "__main__":
    # Permite probar la ventana principal de forma aislada:
    # python -m interfaz.ventana_principal
    VentanaPrincipal().mainloop()
