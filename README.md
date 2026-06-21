# Métodos Numéricos — Proyecto Universitario

Aplicación de escritorio en Python para resolver problemas clásicos de Métodos
Numéricos (conversión de bases, raíces de ecuaciones, interpolación,
derivación, integración, ecuaciones diferenciales ordinarias y operaciones
con matrices), con interfaz gráfica en Tkinter.

La cobertura fue contrastada renglón por renglón con el programa sintético
LCD 2020. Consulta la [matriz de cumplimiento](docs/CUMPLIMIENTO_TEMARIO.md).
Cada pantalla incluye fundamento, fórmula, condiciones de aplicación,
resultado, tabla de iteraciones cuando procede y gráfica opcional.

## Tabla de contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución](#ejecución)
- [Cobertura del temario](docs/CUMPLIMIENTO_TEMARIO.md)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Convenciones de código](#convenciones-de-código)
- [Flujo de trabajo en Git](#flujo-de-trabajo-en-git)
- [Pruebas](#pruebas)
- [Equipo](#equipo)
- [Licencia](#licencia)

## Requisitos

- Python 3.12 o superior
- Tkinter (incluido en la instalación estándar de Python en Windows/macOS;
  en Linux instalar `python3-tk` vía el gestor de paquetes del sistema)
- pip

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/<organizacion>/metodos-numericos.git
cd metodos-numericos

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

Esto abre la interfaz gráfica (Tkinter) con navegación por categorías. Ver
la guía de uso y el flujo visual en [`docs/GUI.md`](docs/GUI.md). En Linux,
si falta Tk, instalar `python3-tk`.

## Estructura del proyecto

```
metodos-numericos/
├── main.py                  # Punto de entrada de la aplicación
├── interfaz/                # Capa de presentación (Tkinter)
├── metodos/                 # Lógica numérica, organizada por tema
│   ├── conversion/          # Conversión entre bases numéricas
│   ├── raices/              # Métodos de búsqueda de raíces
│   ├── interpolacion/       # Métodos de interpolación
│   ├── derivacion/          # Derivación numérica
│   ├── integracion/         # Integración numérica
│   ├── edo/                 # Ecuaciones diferenciales ordinarias
│   └── matrices/            # Operaciones y sistemas de ecuaciones lineales
├── utils/                   # Utilidades compartidas (validación, formato, errores)
├── tests/                   # Pruebas unitarias (pytest)
├── docs/                    # Documentación adicional
├── .github/                 # Plantillas de Issues/PR y CI
├── requirements.txt
├── .gitignore
├── CONTRIBUTING.md
└── README.md
```

Ver [`docs/ESTRUCTURA.md`](docs/ESTRUCTURA.md) para el detalle de cada módulo.

## Convenciones de código

Resumen rápido (detalle completo en [CONTRIBUTING.md](CONTRIBUTING.md)):

| Elemento            | Convención            | Ejemplo                     |
|---------------------|------------------------|------------------------------|
| Módulos / archivos  | `snake_case.py`        | `biseccion.py`               |
| Funciones           | `snake_case`           | `calcular_raiz()`            |
| Clases              | `PascalCase`           | `VentanaPrincipal`           |
| Constantes          | `MAYUSCULAS_SNAKE`     | `TOLERANCIA_DEFAULT`         |
| Ramas Git           | `tipo/descripcion`     | `feature/metodo-biseccion`   |

Todo el código sigue [PEP 8](https://peps.python.org/pep-0008/) y usa
*type hints* en las firmas de funciones públicas.

## Flujo de trabajo en Git

Ver guía completa en [CONTRIBUTING.md](CONTRIBUTING.md). Resumen:

```
main        → versión estable, solo recibe merges vía Pull Request
develop     → integración de features antes de pasar a main
feature/*   → una rama por método/funcionalidad nueva
fix/*       → corrección de errores
docs/*      → cambios de documentación
```

## Pruebas

```bash
pytest tests/
```

## Equipo

| Nombre | Rol | GitHub |
|--------|-----|--------|
| Por definir | Por definir | Por definir |

## Licencia

Proyecto académico. Uso educativo — ESCOM, Instituto Politécnico Nacional.
