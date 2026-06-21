# Auditoría de cobertura del plan de estudios LCD 2020

Fuente auditada: `metodosNumericos_LCD2020.pdf`, programa sintético de
Métodos Numéricos, vigente a partir de enero de 2021. Se contrastaron las
unidades temáticas de las páginas 3 a 5 y la relación de prácticas de la
página 6 con el registro ejecutable de la interfaz.

La cobertura es completa: cada renglón del temario tiene una implementación
invocable desde la GUI, validaciones de dominio y una fórmula visible. Los
métodos iterativos devuelven historial y error cuando esos conceptos forman
parte del algoritmo; los métodos directos reportan resultado, pasos,
factores o tablas según corresponda.

## Matriz de trazabilidad

| Unidad y contenido oficial | Implementación en la aplicación | Estado |
|---|---|---|
| 1.1 Punto flotante; redondeo y truncamiento | IEEE 754 decimal/binario, análisis de errores, redondeo y truncamiento | Completo |
| 1.2 Métodos cerrados | Bisección y falsa posición | Completo |
| 1.3 Métodos abiertos | Punto fijo, Newton-Raphson y secante | Completo |
| 1.4 Raíces de polinomios | Müller y Bairstow; deflación como apoyo | Completo |
| 2.1 Derivación numérica | Progresiva, regresiva, centrada, fórmula general de n+1 puntos, fórmulas de 3, 4 y 5 puntos, Richardson | Completo |
| 2.2 Integración simple | Trapecio, Simpson 1/3, Simpson 3/8 y punto medio | Completo |
| 2.3 Integración compuesta | Trapecio, Simpson 1/3, Simpson 3/8 y punto medio compuestos | Completo |
| 2.4 Integración múltiple | Simpson doble, Gauss-Legendre doble y triple | Completo |
| 3.1 Problemas de valor inicial | Formularios con f, x0, y0 y extremo final | Completo |
| 3.2 Euler | Euler explícito | Completo |
| 3.3 Taylor, Runge-Kutta y Fehlberg | Taylor superior, RK4 y RKF45 adaptativo | Completo |
| 3.4 Multipaso fijo y variable | Adams-Bashforth-Moulton uniforme y Adams variable con pesos de Lagrange | Completo |
| 3.5 Orden superior y sistemas | Reducción a sistema de primer orden y RK4 vectorial | Completo |
| 4.1 Sistemas lineales | Gauss, Gauss-Jordan, pivoteo parcial y parcial escalado | Completo |
| 4.2 Inversa | Gauss-Jordan sobre [A\|I] | Completo |
| 4.3 Factorizaciones | LU/Doolittle, LDLᵀ, Cholesky y Crout | Completo |
| 5.1 Regresión y mínimos cuadrados | Lineal, polinomial, múltiple, mínimos cuadrados y no lineal | Completo |
| 5.2 Interpolación | Diferencias divididas, Lagrange, Hermite y splines cúbicos | Completo |
| Práctica 16 | Aproximación discreta de Fourier | Completo |

## Criterios matemáticos y de software

- Las funciones de usuario se evalúan en un espacio de nombres restringido;
  no se permite acceso a `builtins` ni a atributos de objetos.
- Las hipótesis críticas se validan antes de calcular: cambio de signo,
  tolerancias positivas, paridad de Simpson, dimensiones matriciales,
  simetría/definición positiva y denominadores no nulos.
- La fórmula general de n+1 puntos construye sus pesos imponiendo exactitud
  monomial, en lugar de mantener tablas incompletas de coeficientes.
- El Adams variable integra las bases cardinales de Lagrange sobre cada paso;
  no reutiliza incorrectamente coeficientes de malla uniforme.
- La GUI separa presentación, registro declarativo, evaluación de entradas y
  lógica numérica. Las fórmulas viven en `interfaz/teoria.py` y los algoritmos
  en `metodos/`.

## Verificación reproducible

```bash
python -m pytest -q
python -m compileall -q main.py interfaz metodos utils
python main.py
```

La suite incluye casos conocidos, entradas inválidas, precisión numérica,
registro de la interfaz y presencia de fórmula para cada método publicado.
