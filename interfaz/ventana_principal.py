"""Ventana principal de la aplicación.

Define el menú/navegación hacia cada módulo de métodos numéricos. Cada
integrante del equipo agregará aquí la entrada correspondiente a su módulo
(botón o entrada de menú) que abra su propia vista en `interfaz/`.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

APP_TITLE = "Métodos Numéricos"
APP_MIN_WIDTH = 720
APP_MIN_HEIGHT = 480


class VentanaPrincipal(tk.Tk):
    """Ventana raíz de la aplicación.

    Responsable únicamente de la navegación general. Cada categoría de
    método (raíces, interpolación, integración, etc.) debe implementarse
    como su propia vista/Toplevel y conectarse aquí mediante un botón.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self._construir_layout()

    def _construir_layout(self) -> None:
        """Construye el layout base de la ventana principal.

        TODO(equipo): reemplazar los botones de ejemplo por la navegación
        real hacia cada vista (conversion, raices, interpolacion,
        derivacion, integracion, edo, matrices).
        """
        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text=APP_TITLE, font=("Segoe UI", 18, "bold"))
        titulo.pack(pady=(0, 20))

        subtitulo = ttk.Label(
            contenedor,
            text="Selecciona una categoría de método (en construcción)",
        )
        subtitulo.pack(pady=(0, 10))

        categorias = [
            "Conversión de bases",
            "Raíces de ecuaciones",
            "Interpolación",
            "Derivación numérica",
            "Integración numérica",
            "Ecuaciones diferenciales (EDO)",
            "Matrices / Sistemas de ecuaciones",
        ]

        for categoria in categorias:
            ttk.Button(
                contenedor,
                text=categoria,
                state="disabled",  # TODO(equipo): habilitar al conectar vista
            ).pack(fill="x", pady=4)


if __name__ == "__main__":
    # Permite probar la ventana principal de forma aislada:
    # python -m interfaz.ventana_principal
    VentanaPrincipal().mainloop()
