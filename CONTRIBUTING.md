# Guía de Contribución

Gracias por colaborar en el proyecto de Métodos Numéricos. Esta guía define
cómo trabajamos en equipo dentro de GitHub: ramas, commits, Pull Requests y
estilo de código.

## 1. Configuración inicial

```bash
git clone https://github.com/<organizacion>/metodos-numericos.git
cd metodos-numericos
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Estructura de ramas

| Rama         | Propósito                                              | Protegida |
|--------------|----------------------------------------------------------|-----------|
| `main`       | Versión estable y entregable. Solo recibe merge desde `develop` vía PR revisado. | Sí |
| `develop`    | Integración de todo el trabajo en curso.                | Sí |
| `feature/*`  | Una rama por método numérico o funcionalidad nueva.      | No |
| `fix/*`      | Corrección de bugs detectados en `develop` o `main`.     | No |
| `docs/*`     | Cambios exclusivos de documentación.                     | No |
| `refactor/*` | Reestructuración de código sin cambiar comportamiento.   | No |

### Nomenclatura de ramas

```
feature/metodo-biseccion
feature/interfaz-menu-principal
fix/division-cero-newton-raphson
docs/actualizar-readme
refactor/unificar-validaciones
```

Formato: `tipo/descripcion-corta-en-kebab-case`.

### Flujo recomendado

```
main
 └── develop
       ├── feature/metodo-biseccion
       ├── feature/metodo-simpson
       ├── feature/interfaz-menu-principal
       └── fix/division-cero-newton-raphson
```

1. Crear rama desde `develop` (siempre actualizada):
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/metodo-biseccion
   ```
2. Trabajar y hacer commits pequeños y descriptivos.
3. Subir la rama y abrir un Pull Request hacia `develop`.
4. Esperar al menos 1 revisión aprobada antes de hacer merge.
5. Periódicamente, `develop` se integra a `main` mediante un PR de release.

## 3. Convención de commits

Usamos un formato inspirado en [Conventional Commits](https://www.conventionalcommits.org/):

```
tipo: descripción breve en infinitivo

[cuerpo opcional explicando el porqué]
```

Tipos permitidos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`.

Ejemplos:

```
feat: agregar método de bisección
fix: corregir división entre cero en Newton-Raphson
docs: documentar módulo de integración
test: agregar pruebas unitarias para regla del trapecio
```

## 4. Convenciones de nombres en código

| Elemento              | Convención          | Ejemplo                       |
|------------------------|---------------------|--------------------------------|
| Archivos / módulos     | `snake_case.py`     | `newton_raphson.py`           |
| Funciones / variables   | `snake_case`        | `calcular_raiz`, `tolerancia` |
| Clases                 | `PascalCase`        | `VentanaBiseccion`            |
| Constantes              | `MAYUSCULAS_SNAKE`  | `MAX_ITERACIONES`             |
| Paquetes (carpetas)     | `snake_case` corto  | `raices`, `edo`               |

Reglas adicionales:

- Cada método numérico vive en su **propio archivo** dentro de la carpeta de
  su categoría (ej. `metodos/raices/biseccion.py`).
- Toda función pública debe tener **docstring** (formato Google o NumPy) y
  **type hints**.
- No mezclar lógica numérica con código de interfaz: `metodos/` no debe
  importar nada de `interfaz/`.
- Validaciones de entrada reutilizables van en `utils/validaciones.py`.
- Formatear con `black .` y revisar con `flake8` antes de hacer commit.

## 5. Pull Requests

- Un PR debe resolver **una sola cosa** (un método, un bug, una feature).
- Título claro, mismo estilo que los commits: `feat: agregar método de Simpson 1/3`.
- Debe incluir, cuando aplique, pruebas en `tests/`.
- Debe pasar CI (lint + tests) antes de poder fusionarse.
- Se requiere al menos **1 aprobación** del equipo.
- Quien abre el PR no debe ser quien lo aprueba (revisión cruzada).

Plantilla de PR en [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).

### Ejemplo de Pull Request

**Título:** `feat: agregar método de bisección`

**Descripción:**

```markdown
## Descripción
Implementa el método de bisección para encontrar raíces de funciones
continuas en un intervalo [a, b].

## Cambios
- Se agrega `metodos/raices/biseccion.py` con la función `biseccion()`.
- Se agregan pruebas en `tests/test_biseccion.py`.
- Se actualiza `docs/ESTRUCTURA.md` con la firma del nuevo método.

## Tipo de cambio
- [x] Nueva funcionalidad (feature)
- [ ] Corrección de bug (fix)
- [ ] Documentación
- [ ] Refactor

## Checklist
- [x] El código sigue las convenciones de `CONTRIBUTING.md`
- [x] Se agregaron/actualizaron pruebas
- [x] `black .` y `flake8` ejecutados sin errores
- [x] Probado localmente con casos de prueba conocidos

## Cómo probar
\```bash
pytest tests/test_biseccion.py -v
\```
```

## 6. Reporte de errores

Usar la plantilla de Issue correspondiente
([`.github/ISSUE_TEMPLATE/bug_report.md`](.github/ISSUE_TEMPLATE/bug_report.md))
incluyendo pasos para reproducir, comportamiento esperado y comportamiento
actual.

## 7. Código de conducta básico

- Revisar PRs en menos de 48 h cuando sea posible.
- Comentarios de revisión orientados al código, no a la persona.
- Si hay conflicto de criterio técnico, se discute en el PR o en reunión de
  equipo, no se hace force-push sobre ramas compartidas sin avisar.
