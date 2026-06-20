# Guía de la interfaz gráfica (Tkinter)

Interfaz académica para ejecutar los métodos numéricos del proyecto sin
escribir código. La GUI es **solo presentación**: no contiene algoritmos;
invoca las funciones de `metodos/` a través de una capa de conexión
declarativa.

## Requisitos

- Python 3.12+ **compilado con soporte Tk** (módulo `tkinter`).
  - Windows / macOS (instalador oficial): viene incluido.
  - Linux: `sudo apt install python3-tk` (Debian/Ubuntu) o equivalente.
- Verifica que Tk está disponible:

  ```bash
  python -c "import tkinter; print('Tk OK')"
  ```

## Ejecución

```bash
python main.py
```

## Arquitectura (separación GUI ↔ lógica)

```
main.py
  └─ interfaz/ventana_principal.py   Navegación: un botón por categoría
       └─ interfaz/vista_categoria.py  Vista genérica (Toplevel)
            ├─ interfaz/registro.py       Qué métodos hay y qué parámetros piden
            ├─ interfaz/evaluador.py      Texto -> función / lista / matriz (seguro)
            └─ interfaz/formato_resultado.py  Resultado -> texto para mostrar
                 └─ metodos/...            LÓGICA NUMÉRICA (no se toca desde la GUI)
```

- `interfaz/` depende de `metodos/` y `utils/`; **nunca al revés**.
- Agregar un método nuevo a la GUI = agregar una entrada en
  `interfaz/registro.py` (no se modifica ninguna vista).

## Flujo de uso

1. Al iniciar, la **ventana principal** muestra un botón por categoría:
   Conversión, Raíces, Interpolación, Derivación, Integración, EDO y
   Sistemas lineales. El número entre paréntesis indica cuántos métodos
   tiene cada categoría.
2. Al pulsar una categoría se abre una **ventana de categoría** con:
   - Un desplegable (*Combobox*) para elegir el método.
   - Un formulario que se **reconstruye automáticamente** según el método
     elegido, con valores de ejemplo precargados.
   - Un botón **Calcular**.
   - Un área de **Resultado**.
3. Se completan los parámetros y se pulsa **Calcular**:
   - Si la entrada es inválida (texto no numérico, función mal escrita,
     intervalo incorrecto, etc.) aparece un **cuadro de diálogo de error**
     y no se ejecuta el cálculo.
   - Si todo es correcto, el resultado se muestra en el área inferior
     (incluyendo tablas/historiales cuando el método los devuelve).

### Diagrama del flujo visual

```
┌─────────────────────────────────────────────┐
│              Métodos Numéricos                │
│      Selecciona una categoría de método       │
│                                               │
│  [ Conversión (1) ]   [ Raíces (8) ]          │
│  [ Interpolación (7)]  [ Derivación (5) ]      │
│  [ Integración (10)]  [ EDO (4) ]             │
│  [ Sistemas lineales (4) ]                    │
│                                               │
│         Proyecto académico — ESCOM, IPN       │
└─────────────────────────────────────────────┘
                    │  (clic en una categoría)
                    ▼
┌─────────────────────────────────────────────┐
│   Métodos Numéricos — Raíces                  │
│   Método:  [ Bisección            ▼]          │
│                                               │
│   f(x)             [ x**2 - 2          ]      │
│   a                [ 0                 ]      │
│   b                [ 2                 ]      │
│   Tolerancia       [ 1e-6              ]      │
│   Máx. iteraciones [ 100               ]      │
│                                               │
│             [      Calcular      ]            │
│  ┌── Resultado ─────────────────────────────┐ │
│  │ raiz: 1.414214                            │ │
│  │ iteraciones: 21                           │ │
│  │ convergio: True                           │ │
│  │ Historial: ...                            │ │
│  └───────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
                    │  (entrada inválida)
                    ▼
        ┌───────────────────────────┐
        │  ⚠  Entrada inválida       │
        │  Campo 'f(x)': Expresión   │
        │  inválida: ...             │
        │            [ Aceptar ]     │
        └───────────────────────────┘
```

## Sintaxis de entrada

| Campo            | Formato                  | Ejemplo                 |
|------------------|--------------------------|-------------------------|
| Función `f(x)`   | expresión en `x`         | `x**2 - 2`, `sin(x)`    |
| Función `f(x,y)` | expresión en `x`, `y`    | `x - y`, `y`            |
| Lista de números | separados por `,` o espacio | `0, 1, 2, 3`         |
| Matriz           | filas separadas por `;`  | `2 1; 1 3`              |
| Número complejo  | sintaxis de Python       | `1`, `0.5j`, `1+2j`     |
| Derivadas (Taylor superior) | funciones separadas por `;` | `y; y`       |

Las funciones admiten constantes y funciones de `math` (`sin`, `cos`, `exp`,
`sqrt`, `pi`, `e`, ...). Por seguridad, no se permite código arbitrario:
las expresiones se evalúan sin `__builtins__`.

## Manejo de errores

Los métodos lanzan `utils.errores.EntradaInvalidaError` (subclase de
`MetodosNumericosError`); la vista la captura y la traduce a un cuadro de
diálogo `messagebox.showerror`. Errores de conversión de entrada se informan
como *“Entrada inválida”* y cualquier otro error inesperado se muestra sin
cerrar la aplicación.
