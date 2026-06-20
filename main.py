"""Punto de entrada de la aplicación de Métodos Numéricos.

Inicializa la ventana principal de Tkinter y arranca el bucle de eventos.
No debe contener lógica numérica: esa vive en el paquete `metodos`.
"""

from __future__ import annotations

from interfaz.ventana_principal import VentanaPrincipal


def main() -> None:
    """Crea la ventana principal y arranca la aplicación."""
    app = VentanaPrincipal()
    app.mainloop()


if __name__ == "__main__":
    main()
