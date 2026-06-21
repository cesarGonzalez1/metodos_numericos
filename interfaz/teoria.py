"""Catálogo matemático mostrado junto a cada método de la interfaz.

Las fórmulas usan texto Unicode para no exigir un motor LaTeX. La descripción
se toma del docstring de la implementación, por lo que teoría y código quedan
vinculados sin duplicar explicaciones extensas.
"""

# flake8: noqa: E501 - las fórmulas se conservan en una sola línea legible.

from __future__ import annotations

import inspect
from dataclasses import dataclass


@dataclass(frozen=True)
class Teoria:
    descripcion: str
    formula: str
    condiciones: str


# Una fórmula verificable para cada entrada del registro de la GUI.
FORMULAS: dict[str, str] = {
    "Análisis de errores": "Eₐ = |x - x̃|;  Eᵣ = Eₐ/|x|;  E% = 100 Eᵣ",
    "Redondeo y truncamiento": "fl_d(x) = round(x·10ᵈ)/10ᵈ;  tr_d(x) = trunc(x·10ᵈ)/10ᵈ",
    "Decimal a binario": "x = (-1)ˢ · (1.m)₂ · 2^(e-sesgo)  (IEEE 754 normalizado)",
    "Binario a decimal": "(b_k…b₀.b₋₁…)₂ = Σᵢ bᵢ·2ⁱ",
    "Bisección": "cₙ = (aₙ+bₙ)/2;  |r-cₙ| ≤ (b₀-a₀)/2^(n+1)",
    "Falsa posición": "c = b - f(b)(a-b)/(f(a)-f(b))",
    "Punto fijo": "xₙ₊₁ = g(xₙ)",
    "Newton-Raphson": "xₙ₊₁ = xₙ - f(xₙ)/f′(xₙ)",
    "Secante": "xₙ₊₁ = xₙ - f(xₙ)(xₙ-xₙ₋₁)/(f(xₙ)-f(xₙ₋₁))",
    "Müller": "xₙ₊₁ = xₙ - 2c/(b ± √(b²-4ac))  (interpolación cuadrática)",
    "Bairstow": "P(x) = (x²-rx-s)Q(x) + (b₁x+b₀);  corregir r,s hasta b₀,b₁≈0",
    "Deflación": "P(x) = (x-r)Q(x) + P(r)  (división sintética)",
    "Interpolación básica": "p(x)=yᵢ+(yᵢ₊₁-yᵢ)(x-xᵢ)/(xᵢ₊₁-xᵢ)",
    "Polinomio de Lagrange": "Pₙ(x)=Σᵢ yᵢ Lᵢ(x);  Lᵢ(x)=Π_{j≠i}(x-xⱼ)/(xᵢ-xⱼ)",
    "Interpolación de Neville": "Pᵢ,ⱼ(x)=((x-xᵢ)Pᵢ₊₁,ⱼ-(x-xⱼ)Pᵢ,ⱼ₋₁)/(xⱼ-xᵢ)",
    "Diferencias divididas": "Pₙ(x)=f[x₀]+Σₖ f[x₀,…,xₖ] Π_{j<k}(x-xⱼ)",
    "Polinomio de Taylor": "Tₙ(x)=Σ_{k=0}ⁿ f⁽ᵏ⁾(x₀)(x-x₀)ᵏ/k!",
    "Mínimos cuadrados (lineal)": "min Σᵢ(yᵢ-a-bxᵢ)²;  (XᵀX)β=Xᵀy",
    "Aproximación polinómica": "min Σᵢ(yᵢ-Σ_{k=0}ᵐ aₖxᵢᵏ)²;  (VᵀV)a=Vᵀy",
    "Regresión lineal múltiple": "ŷ = β₀+Σⱼβⱼxⱼ;  β=(XᵀX)⁻¹Xᵀy",
    "Regresión no lineal": "a·e^(bx): ln y=ln a+bx;   a·xᵇ: ln y=ln a+b ln x",
    "Interpolación de Hermite": "H(x)=Σᵢ[yᵢhᵢ(x)+y′ᵢĥᵢ(x)], con valores y derivadas prescritos",
    "Trazadores cúbicos (splines)": "Sᵢ(x)=aᵢ+bᵢΔx+cᵢΔx²+dᵢΔx³;  S,S′,S″ continuas",
    "Aproximación de Fourier": "Sₙ(x)=a₀/2+Σ_{k=1}ⁿ[aₖcos(kωx)+bₖsin(kωx)]",
    "Derivación general": "f′(x)≈[f(x+h)-f(x-h)]/(2h)  (centrada)",
    "Fórmula general de n+1 puntos": "f′(x)≈h⁻¹Σⱼwⱼf(x+htⱼ);  Σⱼwⱼtⱼᵏ=δₖ₁",
    "Fórmula de 3 puntos": "f′(x)≈[f(x+h)-f(x-h)]/(2h) = f′(x)+O(h²)",
    "Fórmula de 4 puntos": "f′(x)≈[-11f(x)+18f(x+h)-9f(x+2h)+2f(x+3h)]/(6h)",
    "Fórmula de 5 puntos": "f′(x)≈[f(x-2h)-8f(x-h)+8f(x+h)-f(x+2h)]/(12h)",
    "Extrapolación de Richardson": "Rᵢ,ⱼ=Rᵢ,ⱼ₋₁+(Rᵢ,ⱼ₋₁-Rᵢ₋₁,ⱼ₋₁)/(4ʲ-1)",
    "Trapecio": "∫ₐᵇf(x)dx ≈ (b-a)[f(a)+f(b)]/2",
    "Punto medio": "∫ₐᵇf(x)dx ≈ (b-a)f((a+b)/2)",
    "Punto medio compuesto": "∫ₐᵇf(x)dx ≈ hΣ_{i=0}^{n-1}f(a+(i+1/2)h)",
    "Simpson 1/3": "∫ₐᵇf(x)dx ≈ (b-a)[f(a)+4f((a+b)/2)+f(b)]/6",
    "Simpson 3/8": "∫ₐᵇf(x)dx ≈ 3h[f(a)+3f(a+h)+3f(a+2h)+f(b)]/8",
    "Trapecio compuesto": "Tₙ=h[f(a)/2+Σ_{i=1}^{n-1}f(a+ih)+f(b)/2]",
    "Simpson 1/3 compuesto": "Sₙ=h[f₀+4Σf_impar+2Σf_par+fₙ]/3",
    "Simpson 3/8 compuesto": "Sₙ=3h[f₀+3Σ_{3∤i}fᵢ+2Σ_{3|i}fᵢ+fₙ]/8",
    "Romberg": "Rᵢ,ⱼ=(4ʲRᵢ,ⱼ₋₁-Rᵢ₋₁,ⱼ₋₁)/(4ʲ-1)",
    "Cuadratura adaptativa": "S(a,b)≈S(a,m)+S(m,b);  error≈|S₂-S₁|/15",
    "Cuadratura gaussiana": "∫ₐᵇf(x)dx≈(b-a)/2 Σᵢwᵢf((b-a)ξᵢ/2+(a+b)/2)",
    "Integral doble de Simpson": "∫∫f≈hₓhᵧ/9 ΣᵢΣⱼwᵢwⱼf(xᵢ,yⱼ)",
    "Cuadratura gaussiana doble": "∫∫f≈(b-a)(d-c)/4 ΣᵢΣⱼwᵢwⱼf(Xᵢ,Yⱼ)",
    "Cuadratura gaussiana triple": "∫∫∫f≈J ΣᵢΣⱼΣₖwᵢwⱼwₖf(Xᵢ,Yⱼ,Zₖ)",
    "Euler": "yₙ₊₁=yₙ+h f(xₙ,yₙ)  (error global O(h))",
    "Taylor de orden superior": "yₙ₊₁=yₙ+Σ_{k=1}ᵐ hᵏ y⁽ᵏ⁾(xₙ)/k!",
    "Runge-Kutta 4": "yₙ₊₁=yₙ+h(k₁+2k₂+2k₃+k₄)/6",
    "Runge-Kutta-Fehlberg": "error local≈|y⁽⁵⁾-y⁽⁴⁾|;  h_nuevo=0.84h(tol/error)^(1/4)",
    "Adams (multipaso, predictor-corrector)": "AB4: y*=yₙ+h(55fₙ-59fₙ₋₁+37fₙ₋₂-9fₙ₋₃)/24",
    "Adams con paso variable": "yₙ₊₁=yₙ+Σⱼ[∫_{xₙ}^{xₙ₊₁}Lⱼ(x)dx] fⱼ",
    "Sistema de EDO (RK4)": "Yₙ₊₁=Yₙ+h(K₁+2K₂+2K₃+K₄)/6",
    "Ecuación de orden superior (RK4)": "y⁽ᵐ⁾=g → Y′=(y′,y″,…,g(x,Y)); aplicar RK4 vectorial",
    "Eliminación gaussiana": "mᵢₖ=aᵢₖ/aₖₖ;  Fᵢ←Fᵢ-mᵢₖFₖ;  luego sustitución hacia atrás",
    "Eliminación aritmética (Gauss-Jordan)": "[A|b] → [I|x] mediante operaciones elementales de fila",
    "Pivoteo parcial": "p=argmax_{i≥k}|aᵢₖ|; intercambiar Fₖ↔Fₚ antes de eliminar",
    "Pivoteo escalado": "p=argmax_{i≥k}|aᵢₖ|/sᵢ,  sᵢ=maxⱼ|aᵢⱼ|",
    "Solución por LU (Doolittle)": "A=LU, diag(L)=1;  Ly=b;  Ux=y",
    "Solución por Crout": "A=LU, diag(U)=1;  Ly=b;  Ux=y",
    "Solución por Cholesky (sim. def. pos.)": "A=LLᵀ;  Ly=b;  Lᵀx=y",
    "Solución por LDLᵀ (simétrica)": "A=LDLᵀ;  Ly=b;  Dz=y;  Lᵀx=z",
    "Inversa de matriz": "[A|I] → [I|A⁻¹] por Gauss-Jordan",
    "Factorización LU (Doolittle)": "A=LU;  lᵢᵢ=1",
    "Factorización de Crout": "A=LU;  uᵢᵢ=1",
    "Factorización de Cholesky": "A=LLᵀ,  lᵢᵢ=√(aᵢᵢ-Σ_{k<i}lᵢₖ²)",
    "Factorización LDLᵀ": "A=LDLᵀ, con L triangular inferior unitaria y D diagonal",
}


CONDICIONES: dict[str, str] = {
    "Bisección": "f continua en [a,b] y f(a)f(b)≤0; convergencia garantizada.",
    "Falsa posición": "f continua y cambio de signo en [a,b].",
    "Punto fijo": "Convergencia local si g conserva el intervalo y sup|g′|<1.",
    "Newton-Raphson": "Requiere f′(xₙ)≠0; convergencia cuadrática cerca de una raíz simple.",
    "Secante": "Requiere valores consecutivos de f distintos; orden ≈1.618 cerca de raíz simple.",
    "Müller": "Admite aritmética compleja; elegir el signo que evita cancelación en el denominador.",
    "Fórmula general de n+1 puntos": "h>0; plantilla centrada simétrica con cantidad impar de puntos.",
    "Simpson 1/3 compuesto": "n debe ser par.",
    "Simpson 3/8 compuesto": "n debe ser múltiplo de 3.",
    "Punto medio compuesto": "f integrable; si f″ es continua, error global O(h²).",
    "Cuadratura gaussiana": "Con p nodos es exacta para polinomios de grado ≤2p-1.",
    "Runge-Kutta-Fehlberg": "Integra hacia adelante y adapta h para satisfacer la tolerancia local.",
    "Adams (multipaso, predictor-corrector)": "Paso uniforme; tres puntos iniciales se calculan con RK4.",
    "Adams con paso variable": "Malla no uniforme; pesos obtenidos por integración de Lagrange y control local.",
    "Solución por Cholesky (sim. def. pos.)": "A debe ser simétrica definida positiva.",
    "Factorización de Cholesky": "A debe ser simétrica definida positiva.",
    "Solución por LDLᵀ (simétrica)": "A debe ser simétrica y los pivotes de D no nulos.",
    "Factorización LDLᵀ": "A debe ser simétrica y admitir la factorización sin pivoteo.",
}


def obtener_teoria(metodo: dict) -> Teoria:
    """Devuelve descripción, fórmula y condiciones de una entrada del registro."""
    nombre = metodo["nombre"]
    doc = inspect.getdoc(metodo["funcion"]) or "Método numérico."
    descripcion = doc.split("\n\n", maxsplit=1)[0].replace("\n", " ")
    return Teoria(
        descripcion=descripcion,
        formula=FORMULAS[nombre],
        condiciones=CONDICIONES.get(
            nombre,
            "Revise los parámetros y las hipótesis indicadas por la validación del método.",
        ),
    )
