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

from interfaz import evaluador, graficador
from interfaz.formato_resultado import formatear_resultado
from interfaz.teoria import obtener_teoria
from interfaz.tema import BORDE, SECUNDARIO
from interfaz.vista_base import VistaBase
from utils.errores import MetodosNumericosError


class VistaCategoria(VistaBase):
    """Toplevel que presenta los métodos de una categoría."""

    def __init__(self, master: tk.Misc, categoria: str, metodos: list[dict]) -> None:
        super().__init__(master, titulo=f"Métodos Numéricos — {categoria}")
        self._categoria = categoria
        self._metodos = {m["nombre"]: m for m in metodos}
        self._entradas: dict[str, object] = {}
        self._canvas_grafica = None
        self._construir_selector(metodos)
        self._construir_teoria()
        self._construir_form_y_boton()
        self._construir_panel_grafica()
        # Carga el primer método por defecto.
        if metodos:
            self._combo_metodo.current(0)
            self._cambiar_metodo()

    def _construir_panel_grafica(self) -> None:
        """Crea el área donde se incrustará la gráfica (si hay matplotlib)."""
        self._frame_grafica = ttk.Frame(self.notebook, padding=8, style="Card.TFrame")
        self.notebook.add(self._frame_grafica, text="Gráfica")
        self._placeholder_grafica = ttk.Label(
            self._frame_grafica,
            text=(
                ""
                if graficador.MATPLOTLIB_DISPONIBLE
                else "Instala matplotlib para ver gráficas (pip install matplotlib)."
            ),
            style="Card.TLabel",
        )
        self._placeholder_grafica.pack()

    def _mostrar_grafica(self, figura) -> None:
        """Incrusta `figura` en el panel de gráfica; limpia la anterior."""
        # Importación diferida del backend de Tk para no exigir matplotlib.
        if self._canvas_grafica is not None:
            self._canvas_grafica.get_tk_widget().destroy()
            self._canvas_grafica = None
        if hasattr(self, "_placeholder_grafica"):
            self._placeholder_grafica.pack_forget()
        if figura is None:
            self._placeholder_grafica.configure(text="(Sin gráfica para este método)")
            self._placeholder_grafica.pack()
            return
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        self._canvas_grafica = FigureCanvasTkAgg(figura, master=self._frame_grafica)
        self._canvas_grafica.draw()
        self._canvas_grafica.get_tk_widget().pack(fill="both", expand=True)

    def _construir_selector(self, metodos: list[dict]) -> None:
        """Combobox para elegir el método dentro de la categoría."""
        ttk.Label(self.frame_formulario, text="Método", style="Section.TLabel").pack(
            anchor="w"
        )
        self._combo_metodo = ttk.Combobox(
            self.frame_formulario,
            state="readonly",
            values=[m["nombre"] for m in metodos],
        )
        self._combo_metodo.pack(fill="x", pady=(5, 12))
        self._combo_metodo.bind(
            "<<ComboboxSelected>>", lambda _evento: self._cambiar_metodo()
        )

    def _construir_teoria(self) -> None:
        """Crea la ficha de fundamento matemático del método seleccionado."""
        ttk.Label(
            self.frame_formulario, text="Fundamento matemático", style="Section.TLabel"
        ).pack(anchor="w", pady=(2, 5))
        self._texto_teoria = tk.Text(
            self.frame_formulario,
            height=9,
            wrap="word",
            state="disabled",
            font=("Segoe UI", 9),
            background="#F8FBFD",
            foreground="#243B53",
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDE,
            padx=9,
            pady=8,
        )
        self._texto_teoria.pack(fill="x", pady=(0, 12))

    def _construir_form_y_boton(self) -> None:
        """Contenedor de campos dinámicos y botón Calcular."""
        self._frame_campos = ttk.Frame(self.frame_formulario, style="Card.TFrame")
        self._frame_campos.pack(fill="x")
        ttk.Button(
            self.frame_formulario,
            text="Calcular método",
            style="Accent.TButton",
            command=self._calcular,
        ).pack(fill="x", pady=(14, 6))
        self._estado = ttk.Label(
            self.frame_formulario,
            text="Completa los datos y calcula.",
            style="Card.TLabel",
            foreground=SECUNDARIO,
        )
        self._estado.pack(anchor="w")

    def _cambiar_metodo(self) -> None:
        """Reconstruye los campos del formulario según el método elegido."""
        for hijo in self._frame_campos.winfo_children():
            hijo.destroy()
        self._entradas.clear()

        metodo = self._metodos[self._combo_metodo.get()]
        teoria = obtener_teoria(metodo)
        contenido = (
            f"{teoria.descripcion}\n\n"
            f"FÓRMULA\n{teoria.formula}\n\n"
            f"CONDICIONES\n{teoria.condiciones}"
        )
        self._texto_teoria.configure(state="normal")
        self._texto_teoria.delete("1.0", tk.END)
        self._texto_teoria.insert("1.0", contenido)
        self._texto_teoria.configure(state="disabled")
        for campo in metodo["campos"]:
            fila = ttk.Frame(self._frame_campos, style="Card.TFrame")
            fila.pack(fill="x", pady=3)
            ttk.Label(fila, text=campo["etiqueta"], width=21, style="Card.TLabel").pack(
                side="left"
            )

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
        if tipo == "funcion_xyz":
            return evaluador.crear_funcion_xyz(texto)
        if tipo == "sistema_edo":
            return evaluador.crear_sistema_edo(texto)
        if tipo == "funcion_estado":
            return evaluador.crear_funcion_estado(texto)
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
        if tipo in ("opcion", "texto"):
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
        self.notebook.select(self.frame_resultado)
        self._estado.configure(text="Cálculo completado correctamente.")

        # Gráfica opcional (no debe interrumpir el flujo si falla).
        try:
            figura = graficador.crear_figura(
                self._categoria, metodo["nombre"], parametros, resultado
            )
        except Exception:  # noqa: BLE001 - la gráfica nunca rompe el cálculo
            figura = None
        self._mostrar_grafica(figura)
