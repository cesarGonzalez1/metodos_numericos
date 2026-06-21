"""Tema visual compartido de la aplicación Tkinter."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

AZUL_NOCHE = "#102A43"
AZUL = "#1677A6"
AZUL_CLARO = "#E8F4FA"
FONDO = "#F4F7FA"
TEXTO = "#1F2933"
SECUNDARIO = "#52606D"
BORDE = "#D9E2EC"
BLANCO = "#FFFFFF"
EXITO = "#16836B"


def configurar_tema(ventana: tk.Misc) -> None:
    """Aplica tipografía, color y espaciado coherentes a widgets ttk."""
    estilo = ttk.Style(ventana)
    if "clam" in estilo.theme_names():
        estilo.theme_use("clam")
    ventana.configure(background=FONDO)
    estilo.configure("TFrame", background=FONDO)
    estilo.configure("Card.TFrame", background=BLANCO, relief="flat")
    estilo.configure(
        "TLabel", background=FONDO, foreground=TEXTO, font=("Segoe UI", 10)
    )
    estilo.configure(
        "Card.TLabel", background=BLANCO, foreground=TEXTO, font=("Segoe UI", 10)
    )
    estilo.configure(
        "Section.TLabel",
        background=BLANCO,
        foreground=AZUL_NOCHE,
        font=("Segoe UI Semibold", 11),
    )
    estilo.configure(
        "Muted.TLabel", background=FONDO, foreground=SECUNDARIO, font=("Segoe UI", 9)
    )
    estilo.configure(
        "Category.TButton",
        font=("Segoe UI Semibold", 11),
        padding=(18, 16),
        background=BLANCO,
        foreground=AZUL_NOCHE,
        bordercolor=BORDE,
        focusthickness=1,
        focuscolor=AZUL,
    )
    estilo.map(
        "Category.TButton",
        background=[("active", AZUL_CLARO), ("pressed", "#D5EAF4")],
        foreground=[("active", AZUL_NOCHE)],
    )
    estilo.configure(
        "Accent.TButton",
        font=("Segoe UI Semibold", 10),
        padding=(14, 10),
        background=AZUL,
        foreground=BLANCO,
        bordercolor=AZUL,
    )
    estilo.map(
        "Accent.TButton",
        background=[("active", "#11658E"), ("pressed", AZUL_NOCHE)],
        foreground=[("disabled", "#CBD5E1"), ("!disabled", BLANCO)],
    )
    estilo.configure("TEntry", padding=7, fieldbackground=BLANCO, bordercolor=BORDE)
    estilo.configure("TCombobox", padding=7, fieldbackground=BLANCO)
    estilo.configure("TNotebook", background=FONDO, borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(16, 9), font=("Segoe UI Semibold", 10))
    estilo.map("TNotebook.Tab", foreground=[("selected", AZUL)])


def centrar(ventana: tk.Misc, ancho: int, alto: int) -> None:
    """Centra una ventana respetando el tamaño disponible de pantalla."""
    pantalla_x = ventana.winfo_screenwidth()
    pantalla_y = ventana.winfo_screenheight()
    ancho = min(ancho, max(720, pantalla_x - 80))
    alto = min(alto, max(560, pantalla_y - 100))
    x = max(0, (pantalla_x - ancho) // 2)
    y = max(0, (pantalla_y - alto) // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
