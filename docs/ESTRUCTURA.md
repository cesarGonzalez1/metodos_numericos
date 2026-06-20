# Estructura del Proyecto (detalle)

Este documento amplía la estructura resumida en el `README.md` y explica
el propósito de cada módulo, para que cualquier integrante sepa dónde
agregar su código.

## Árbol completo

```
metodos-numericos/
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml
│
├── interfaz/
│   ├── __init__.py
│   ├── ventana_principal.py      # Ventana raíz / navegación por categorías
│   ├── vista_base.py             # Clase base para sub-ventanas (Toplevel)
│   ├── vista_categoria.py        # Vista genérica (formulario + resultado)
│   ├── registro.py               # Conexión declarativa GUI <-> metodos/
│   ├── evaluador.py              # Texto -> función / lista / matriz (seguro)
│   └── formato_resultado.py      # Resultado -> texto para mostrar
│
├── metodos/
│   ├── __init__.py
│   ├── conversion/
│   │   ├── __init__.py
│   │   └── decimal_a_binario.py  # Ejemplo / plantilla
│   ├── raices/                  # Búsqueda de raíces (1 método por archivo)
│   │   ├── __init__.py           # Reexporta todas las funciones públicas
│   │   ├── biseccion.py
│   │   ├── falsa_posicion.py
│   │   ├── punto_fijo.py
│   │   ├── newton_raphson.py
│   │   ├── secante.py
│   │   ├── muller.py             # Soporta raíces complejas (cmath)
│   │   ├── bairstow.py           # Todas las raíces de un polinomio
│   │   └── deflacion.py          # División sintética por (x - raiz)
│   ├── interpolacion/
│   │   ├── __init__.py
│   │   └── lagrange.py           # Ejemplo / plantilla
│   ├── derivacion/
│   │   ├── __init__.py
│   │   └── diferencias_finitas.py # Ejemplo / plantilla
│   ├── integracion/
│   │   ├── __init__.py
│   │   └── trapecio.py           # Ejemplo / plantilla
│   ├── edo/
│   │   ├── __init__.py
│   │   └── euler.py              # Ejemplo / plantilla
│   └── matrices/
│       ├── __init__.py
│       └── eliminacion_gaussiana.py # Ejemplo / plantilla
│
├── utils/
│   ├── __init__.py
│   ├── errores.py                # Excepciones del dominio
│   ├── validaciones.py           # Validaciones reutilizables
│   └── formato.py                # Formateo de resultados
│
├── tests/                       # Una suite por método (pytest)
│   ├── __init__.py
│   ├── test_biseccion.py
│   ├── test_falsa_posicion.py
│   ├── test_punto_fijo.py
│   ├── test_newton_raphson.py
│   ├── test_secante.py
│   ├── test_muller.py
│   ├── test_bairstow.py
│   └── test_deflacion.py
│
├── docs/
│   └── ESTRUCTURA.md             # Este archivo
│
└── .github/
    ├── workflows/ci.yml          # Lint + tests automáticos
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE/
        ├── bug_report.md
        └── feature_request.md
```

## Regla de dependencias entre capas

```
interfaz/  ──depende de──>  metodos/  ──depende de──>  utils/
```

- `utils/` no depende de nadie (es la base).
- `metodos/` puede usar `utils/`, pero **nunca** importa de `interfaz/`.
- `interfaz/` puede usar `metodos/` y `utils/`.

Esto permite probar toda la lógica numérica con pytest sin necesidad de
abrir ninguna ventana gráfica.

## Cómo agregar un método nuevo

1. Elegir la carpeta correspondiente en `metodos/<categoria>/`.
2. Crear un archivo `snake_case.py` con el nombre del método
   (ej. `metodos/raices/newton_raphson.py`).
3. Escribir la función pública con docstring y type hints (usar
   `metodos/raices/biseccion.py` como plantilla de formato).
4. Agregar pruebas en `tests/test_<metodo>.py`.
5. (Opcional, cuando exista la vista) conectar el método a su botón en
   `interfaz/ventana_principal.py` o en la vista de su categoría.
6. Abrir un Pull Request siguiendo [CONTRIBUTING.md](../CONTRIBUTING.md).

## Cómo agregar una vista nueva en la interfaz

1. Crear `interfaz/<categoria>_vista.py`.
2. Heredar de `VistaBase` (ver `interfaz/vista_base.py`) para mantener
   consistencia visual.
3. Importar únicamente las funciones de `metodos/<categoria>/` necesarias.
4. Conectar el botón correspondiente en `ventana_principal.py`.
