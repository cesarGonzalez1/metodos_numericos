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
from interfaz.tema import AZUL, AZUL_NOCHE, BLANCO, FONDO, centrar, configurar_tema
from interfaz.vista_categoria import VistaCategoria

APP_TITLE = "Métodos Numéricos"
APP_MIN_WIDTH = 760
APP_MIN_HEIGHT = 560


class VentanaPrincipal(tk.Tk):
    """Ventana raíz de la aplicación.

    Responsable únicamente de la navegación general hacia cada categoría.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        configurar_tema(self)
        centrar(self, 920, 650)
        self._construir_layout()

    def _construir_layout(self) -> None:
        """Construye el encabezado y los botones de navegación."""
        encabezado = tk.Frame(self, background=AZUL_NOCHE, padx=34, pady=24)
        encabezado.pack(fill="x")
        tk.Label(
            encabezado,
            text=APP_TITLE,
            background=AZUL_NOCHE,
            foreground=BLANCO,
            font=("Segoe UI Semibold", 24),
        ).pack(anchor="w")
        tk.Label(
            encabezado,
            text="Laboratorio interactivo · Plan de estudios LCD 2020",
            background=AZUL_NOCHE,
            foreground="#D9EAF2",
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        contenedor = ttk.Frame(self, padding=(34, 24, 34, 18))
        contenedor.pack(fill="both", expand=True)
        ttk.Label(
            contenedor,
            text="Elige una unidad para comenzar",
            font=("Segoe UI Semibold", 14),
            foreground=AZUL_NOCHE,
        ).pack(anchor="w", pady=(0, 4))
        ttk.Label(
            contenedor,
            text=(
                "Cada método incluye fórmula, condiciones, entradas validadas "
                "y resultados auditables."
            ),
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(0, 18))

        # Rejilla de botones, uno por categoría del registro.
        rejilla = ttk.Frame(contenedor)
        rejilla.pack(fill="both", expand=True)
        for indice, (categoria, metodos) in enumerate(CATEGORIAS):
            boton = ttk.Button(
                rejilla,
                text=f"{categoria}\n{len(metodos)} métodos",
                style="Category.TButton",
                command=lambda c=categoria, m=metodos: self._abrir_categoria(c, m),
            )
            fila, columna = divmod(indice, 2)
            boton.grid(row=fila, column=columna, sticky="nsew", padx=7, pady=7)
            rejilla.rowconfigure(fila, weight=1)
        rejilla.columnconfigure(0, weight=1)
        rejilla.columnconfigure(1, weight=1)

        pie = ttk.Label(
            contenedor,
            text="Cobertura verificada: 5 unidades temáticas · ESCOM, IPN",
            foreground=AZUL,
            background=FONDO,
            font=("Segoe UI", 9),
        )
        pie.pack(side="bottom", pady=(16, 0))

    def _abrir_categoria(self, categoria: str, metodos: list[dict]) -> None:
        """Abre la vista de una categoría como ventana secundaria."""
        VistaCategoria(self, categoria, metodos)


if __name__ == "__main__":
    # Permite probar la ventana principal de forma aislada:
    # python -m interfaz.ventana_principal
    VentanaPrincipal().mainloop()
