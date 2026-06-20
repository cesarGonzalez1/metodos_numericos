"""Vista genérica de una categoría de métodos.

Construye, a partir del registro declarativo (`interfaz/registro.py`), un
formulario para el método seleccionado, ejecuta la función de `metodos/`
correspondiente y muestra el resultado. Los errores de validación o de
entrada se informan mediante cuadros de diálogo (`tkinter.messagebox`).

Esta clase es 100% presentación: no contiene lógica numérica; solo recoge
parámetros, los convierte con `interfaz.evaluador` y delega el cálculo.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from interfaz import evaluador
from interfaz.formato_resultado import formatear_resultado
from interfaz.vista_base import VistaBase
from utils.errores import MetodosNumericosError


class VistaCategoria(VistaBase):
    """Toplevel que presenta los métodos de una categoría."""

    def __init__(self, master: tk.Misc, categoria: str, metodos: list[dict]) -> None:
        super().__init__(master, titulo=f"Métodos Numéricos — {categoria}")
        self.geometry("640x560")
        self._metodos = {m["nombre"]: m for m in metodos}
        self._entradas: dict[str, object] = {}
        self._construir_selector(metodos)
        self._construir_form_y_boton()
        # Carga el primer método por defecto.
        if metodos:
            self._combo_metodo.current(0)
            self._cambiar_metodo()

    def _construir_selector(self, metodos: list[dict]) -> None:
        """Combobox para elegir el método dentro de la categoría."""
        ttk.Label(self.frame_formulario, text="Método:").pack(anchor="w")
        self._combo_metodo = ttk.Combobox(
            self.frame_formulario,
            state="readonly",
            values=[m["nombre"] for m in metodos],
        )
        self._combo_metodo.pack(fill="x", pady=(0, 10))
        self._combo_metodo.bind(
            "<<ComboboxSelected>>", lambda _evento: self._cambiar_metodo()
        )

    def _construir_form_y_boton(self) -> None:
        """Contenedor de campos dinámicos y botón Calcular."""
        self._frame_campos = ttk.Frame(self.frame_formulario)
        self._frame_campos.pack(fill="x")
        ttk.Button(self.frame_formulario, text="Calcular", command=self._calcular).pack(
            fill="x", pady=10
        )

    def _cambiar_metodo(self) -> None:
        """Reconstruye los campos del formulario según el método elegido."""
        for hijo in self._frame_campos.winfo_children():
            hijo.destroy()
        self._entradas.clear()

        metodo = self._metodos[self._combo_metodo.get()]
        for campo in metodo["campos"]:
            fila = ttk.Frame(self._frame_campos)
            fila.pack(fill="x", pady=3)
            ttk.Label(fila, text=campo["etiqueta"], width=22).pack(side="left")

            if campo["tipo"] == "opcion":
                widget = ttk.Combobox(fila, state="readonly", values=campo["opciones"])
                widget.set(campo["default"])
            else:
                widget = ttk.Entry(fila)
                widget.insert(0, campo["default"])
            widget.pack(side="left", fill="x", expand=True)
            self._entradas[campo["clave"]] = widget

    def _convertir(self, campo: dict, texto: str):
        """Convierte el texto de un campo al tipo de Python esperado."""
        tipo = campo["tipo"]
        if tipo == "funcion_x":
            return evaluador.crear_funcion_x(texto)
        if tipo == "funcion_xy":
            return evaluador.crear_funcion_xy(texto)
        if tipo == "lista":
            return evaluador.parsear_lista(texto)
        if tipo == "matriz":
            return evaluador.parsear_matriz(texto)
        if tipo == "lista_funciones_xy":
            return evaluador.parsear_lista_funciones_xy(texto)
        if tipo == "float":
            return float(texto)
        if tipo == "int":
            return int(texto)
        if tipo == "complejo":
            return complex(texto.replace(" ", ""))
        if tipo == "opcion":
            return texto
        raise ValueError(f"Tipo de campo no soportado: {tipo}")

    def _recolectar_parametros(self, metodo: dict) -> dict:
        """Lee y convierte todos los campos; lanza ValueError si alguno falla."""
        parametros = {}
        for campo in metodo["campos"]:
            texto = self._entradas[campo["clave"]].get().strip()
            try:
                parametros[campo["clave"]] = self._convertir(campo, texto)
            except ValueError as exc:
                raise ValueError(f"Campo '{campo['etiqueta']}': {exc}") from exc
        return parametros

    def _calcular(self) -> None:
        """Ejecuta el método seleccionado y muestra el resultado o el error."""
        metodo = self._metodos[self._combo_metodo.get()]
        try:
            parametros = self._recolectar_parametros(metodo)
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc), parent=self)
            return

        try:
            resultado = metodo["funcion"](**parametros)
        except MetodosNumericosError as exc:
            messagebox.showerror("Error de cálculo", str(exc), parent=self)
            return
        except NotImplementedError:
            messagebox.showwarning(
                "No disponible",
                "Este método aún no está implementado en el proyecto.",
                parent=self,
            )
            return
        except Exception as exc:  # noqa: BLE001 - última red de seguridad GUI
            messagebox.showerror(
                "Error inesperado", f"{type(exc).__name__}: {exc}", parent=self
            )
            return

        self.mostrar_resultado(formatear_resultado(resultado))
