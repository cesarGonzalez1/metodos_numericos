"""Generación de gráficas (matplotlib) para los resultados de los métodos.

Capa de presentación opcional: a partir de la categoría, el método, los
parámetros de entrada y el resultado, construye una ``Figure`` de matplotlib
adecuada para visualizar el problema (la función y su raíz, la solución de
una EDO, los datos y el punto interpolado, el área bajo la curva, etc.).

Diseño:

* No contiene lógica numérica; solo lee lo que ya calcularon los métodos de
  `metodos/` y, a lo sumo, evalúa funciones provistas por el usuario para
  dibujar la curva.
* Es tolerante a fallos: si no hay nada razonable que graficar para un
  método, devuelve ``None`` y la GUI simplemente no muestra figura.
* matplotlib se importa de forma diferida; si no está instalado, todo el
  módulo se degrada con elegancia (``MATPLOTLIB_DISPONIBLE = False``).
"""

from __future__ import annotations

from collections.abc import Callable

try:  # Importación diferida y tolerante a ausencia de matplotlib.
    import matplotlib

    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure

    MATPLOTLIB_DISPONIBLE = True
except Exception:  # pragma: no cover - depende del entorno
    Figure = object  # type: ignore[assignment, misc]
    MATPLOTLIB_DISPONIBLE = False


def _muestrear(f: Callable[[float], float], a: float, b: float, n: int = 400):
    """Muestrea f de forma robusta en [a, b]; descarta puntos no finitos."""
    xs, ys = [], []
    paso = (b - a) / max(n, 1)
    for i in range(n + 1):
        x = a + i * paso
        try:
            y = f(x)
        except Exception:  # Discontinuidades, dominios, etc.
            continue
        if isinstance(y, complex):
            continue
        if y == y and abs(y) != float("inf"):  # excluye NaN/inf
            xs.append(x)
            ys.append(y)
    return xs, ys


def crear_figura(
    categoria: str, nombre: str, parametros: dict, resultado: object
) -> "Figure | None":
    """Construye una figura para el método dado, o ``None`` si no aplica.

    Args:
        categoria: Nombre de la categoría (p. ej. "Raíces").
        nombre: Nombre del método.
        parametros: Parámetros ya convertidos que se pasaron al método.
        resultado: Valor devuelto por el método.

    Returns:
        Una ``matplotlib.figure.Figure`` lista para incrustar, o ``None``.
    """
    if not MATPLOTLIB_DISPONIBLE:
        return None
    try:
        if categoria == "Raíces":
            return _grafica_raices(parametros, resultado)
        if categoria == "Integración":
            return _grafica_integracion(parametros, resultado)
        if categoria == "EDO":
            return _grafica_edo(parametros, resultado)
        if categoria == "Interpolación":
            return _grafica_interpolacion(nombre, parametros, resultado)
        if categoria == "Derivación":
            return _grafica_derivacion(parametros, resultado)
    except Exception:  # La gráfica nunca debe romper el cálculo.
        return None
    return None


def _nueva_figura():
    """Crea una figura compacta con un único eje."""
    figura = Figure(figsize=(5.2, 3.0), dpi=100)
    ejes = figura.add_subplot(111)
    ejes.grid(True, linestyle=":", alpha=0.6)
    return figura, ejes


def _grafica_raices(parametros: dict, resultado: object):
    """Grafica f(x) y marca la raíz aproximada."""
    f = parametros.get("f") or parametros.get("g")
    if not callable(f) or not isinstance(resultado, dict):
        return None
    raiz = resultado.get("raiz")
    # Intervalo: usa [a, b] si existe; si no, una ventana alrededor de la raíz.
    a = parametros.get("a")
    b = parametros.get("b")
    if a is None or b is None:
        centro = raiz if isinstance(raiz, (int, float)) else 0.0
        a, b = centro - 3.0, centro + 3.0
    xs, ys = _muestrear(f, float(a), float(b))
    if not xs:
        return None
    figura, ejes = _nueva_figura()
    ejes.axhline(0, color="black", linewidth=0.8)
    ejes.plot(xs, ys, label="f(x)", color="#1f77b4")
    if isinstance(raiz, (int, float)):
        ejes.plot([raiz], [0], "ro", label=f"raíz ≈ {raiz:.4f}")
    ejes.set_xlabel("x")
    ejes.set_ylabel("f(x)")
    ejes.set_title("Función y raíz")
    ejes.legend(loc="best", fontsize=8)
    figura.tight_layout()
    return figura


def _grafica_integracion(parametros: dict, resultado: object):
    """Grafica f(x) y sombrea el área aproximada en [a, b]."""
    f = parametros.get("f")
    a = parametros.get("a")
    b = parametros.get("b")
    if not callable(f) or a is None or b is None:
        return None
    try:
        f(float(a))  # Detecta f(x, y) (integrales múltiples): no graficable 1D.
    except TypeError:
        return None
    xs, ys = _muestrear(f, float(a), float(b))
    if not xs:
        return None
    figura, ejes = _nueva_figura()
    ejes.plot(xs, ys, color="#1f77b4", label="f(x)")
    ejes.fill_between(xs, ys, alpha=0.3, color="#1f77b4")
    valor = resultado.get("integral") if isinstance(resultado, dict) else resultado
    titulo = "Área bajo la curva"
    if isinstance(valor, (int, float)):
        titulo += f"  ≈ {valor:.6f}"
    ejes.set_title(titulo)
    ejes.set_xlabel("x")
    ejes.set_ylabel("f(x)")
    ejes.legend(loc="best", fontsize=8)
    figura.tight_layout()
    return figura


def _extraer_solucion_edo(resultado: object):
    """Devuelve (xs, [series]) a partir de los distintos retornos de EDO."""
    if isinstance(resultado, list) and resultado and isinstance(resultado[0], tuple):
        xs = [p[0] for p in resultado]
        if isinstance(resultado[0][1], (tuple, list)):
            m = len(resultado[0][1])
            series = [[p[1][k] for p in resultado] for k in range(m)]
        else:
            series = [[p[1] for p in resultado]]
        return xs, series
    if isinstance(resultado, dict):
        if "x" in resultado and "columnas" in resultado:
            return resultado["x"], resultado["columnas"]
        if "solucion" in resultado:
            return _extraer_solucion_edo(resultado["solucion"])
    return None, None


def _grafica_edo(parametros: dict, resultado: object):
    """Grafica la(s) componente(s) de la solución y(x)."""
    xs, series = _extraer_solucion_edo(resultado)
    if not xs or not series:
        return None
    figura, ejes = _nueva_figura()
    for k, serie in enumerate(series):
        etiqueta = "y(x)" if len(series) == 1 else f"y{k + 1}(x)"
        ejes.plot(xs, serie, label=etiqueta)
    ejes.set_xlabel("x")
    ejes.set_ylabel("y")
    ejes.set_title("Solución de la EDO")
    ejes.legend(loc="best", fontsize=8)
    figura.tight_layout()
    return figura


def _grafica_interpolacion(nombre: str, parametros: dict, resultado: object):
    """Grafica los nodos (x, y) y, si existe, el punto evaluado."""
    x_datos = parametros.get("x_datos")
    y_datos = parametros.get("y_datos")
    # Regresión múltiple usa x_datos como matriz: no es graficable en 2D.
    if not isinstance(x_datos, list) or not isinstance(y_datos, list):
        return None
    if x_datos and isinstance(x_datos[0], (list, tuple)):
        return None
    figura, ejes = _nueva_figura()
    ejes.plot(x_datos, y_datos, "o", color="#1f77b4", label="datos")
    x_eval = parametros.get("x_evaluar")
    valor = resultado.get("valor") if isinstance(resultado, dict) else resultado
    if isinstance(x_eval, (int, float)) and isinstance(valor, (int, float)):
        ejes.plot([x_eval], [valor], "rs", label=f"({x_eval:.3f}, {valor:.3f})")
    ejes.set_xlabel("x")
    ejes.set_ylabel("y")
    ejes.set_title(nombre)
    ejes.legend(loc="best", fontsize=8)
    figura.tight_layout()
    return figura


def _grafica_derivacion(parametros: dict, resultado: object):
    """Grafica f(x) alrededor del punto y marca la pendiente estimada."""
    f = parametros.get("f")
    x = parametros.get("x")
    if not callable(f) or not isinstance(x, (int, float)):
        return None
    a, b = x - 1.5, x + 1.5
    xs, ys = _muestrear(f, a, b)
    if not xs:
        return None
    figura, ejes = _nueva_figura()
    ejes.plot(xs, ys, color="#1f77b4", label="f(x)")
    # Recta tangente con la derivada estimada (si el resultado es escalar).
    derivada = (
        resultado
        if isinstance(resultado, (int, float))
        else (resultado.get("derivada") if isinstance(resultado, dict) else None)
    )
    try:
        fx = f(x)
        if isinstance(derivada, (int, float)) and isinstance(fx, (int, float)):
            tang = [fx + derivada * (xi - x) for xi in xs]
            ejes.plot(xs, tang, "--", color="#d62728", label="tangente")
            ejes.plot([x], [fx], "ko")
    except Exception:
        pass
    ejes.set_xlabel("x")
    ejes.set_ylabel("f(x)")
    ejes.set_title("Derivación numérica")
    ejes.legend(loc="best", fontsize=8)
    figura.tight_layout()
    return figura
