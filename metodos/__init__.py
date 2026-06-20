"""Paquete `metodos`: lógica numérica pura del proyecto.

Subpaquetes:
    conversion    -- conversión entre bases numéricas
    raices        -- métodos de búsqueda de raíces de ecuaciones
    interpolacion -- métodos de interpolación
    derivacion    -- derivación numérica
    integracion   -- integración numérica
    edo           -- ecuaciones diferenciales ordinarias
    matrices      -- operaciones con matrices y sistemas de ecuaciones

Regla de oro: este paquete NO debe importar nada de `interfaz`. Las
funciones aquí reciben datos primitivos (float, list, etc.) y devuelven
datos primitivos o estructuras simples (dict, tuple, list); el renderizado
en pantalla es responsabilidad de `interfaz`.
"""
