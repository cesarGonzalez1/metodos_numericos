# Propuesta de integración del módulo de Integración con la GUI

Esta nota describe cómo conectar los métodos de `metodos/integracion/` con
la futura interfaz Tkinter, respetando la separación GUI ↔ lógica.

## Contrato de los métodos

Todas las funciones reciben una función `f: Callable[[float], float]` y
parámetros numéricos, y **devuelven** el resultado (sin `print`):

| Método                              | Firma resumida                       | Retorno |
|-------------------------------------|--------------------------------------|---------|
| `trapecio`                          | `(f, a, b)`                          | `float` |
| `punto_medio`                       | `(f, a, b)`                          | `float` |
| `simpson_un_tercio`                 | `(f, a, b)`                          | `float` |
| `simpson_tres_octavos`              | `(f, a, b)`                          | `float` |
| `trapecio_compuesto`                | `(f, a, b, n)`                       | `float` |
| `simpson_un_tercio_compuesto`       | `(f, a, b, n)` (n par)               | `float` |
| `simpson_tres_octavos_compuesto`    | `(f, a, b, n)` (n múltiplo de 3)     | `float` |
| `romberg`                           | `(f, a, b, niveles)`                 | `dict` (`valor`, `tabla`) |
| `cuadratura_adaptativa`             | `(f, a, b, tolerancia)`              | `float` |
| `cuadratura_gaussiana`              | `(f, a, b, puntos)`                  | `float` |

## Vista propuesta (`interfaz/integracion_vista.py`)

Hereda de `VistaBase` (`interfaz/vista_base.py`):

1. **Entrada de función**: campo de texto `f(x)` (p. ej. `x**2 + 1`). La
   GUI la convierte a un `Callable` con un evaluador seguro (sin `eval`
   global; usar un espacio de nombres restringido con `math`).
2. **Campos de parámetros**: `a`, `b`, y según el método `n` / `niveles` /
   `puntos` / `tolerancia`. Mostrar/ocultar campos según el método elegido
   en un `Combobox`.
3. **Botón Calcular** → llama al método, captura `EntradaInvalidaError` y
   muestra el mensaje con `tkinter.messagebox.showerror`.
4. **Área de resultado** (`mostrar_resultado`): imprime el valor; para
   `romberg` además renderiza la `tabla` con `utils.formato.tabla_iteraciones`.

## Manejo de errores

Los métodos lanzan `utils.errores.EntradaInvalidaError` (subclase de
`MetodosNumericosError`). La vista captura esa excepción base y la traduce a
un cuadro de diálogo, sin que la GUI conozca los detalles del algoritmo.
