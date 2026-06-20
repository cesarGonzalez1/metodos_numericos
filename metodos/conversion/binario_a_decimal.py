"""Conversión binario -> decimal.

Soporta dos modos de entrada, detectados automáticamente:

1. **Binario con punto** (ej. ``"1010.101"``): se interpreta posicionalmente,
   los bits a la izquierda del punto como potencias positivas de 2 y los de la
   derecha como potencias negativas.
2. **Palabra IEEE 754** (32 o 64 bits, sin punto): se descompone en bit de
   **signo**, **característica** (exponente sesgado) y **mantisa**, y se
   reconstruye el valor con la fórmula

   ``valor = (-1)^signo * (1 + mantisa) * 2^(caracteristica - sesgo)``

   (forma normalizada; los subnormales usan ``2^(1 - sesgo)`` sin el 1 implícito).

Un archivo por conversión/algoritmo, según la convención del subpaquete.
"""

from __future__ import annotations

import math

from utils.errores import EntradaInvalidaError

# Parámetros de cada formato IEEE 754 (mismos que en decimal_a_binario).
_FORMATOS: dict[str, dict[str, int]] = {
    "simple": {"bits": 32, "exp": 8, "mantisa": 23, "sesgo": 127},
    "doble": {"bits": 64, "exp": 11, "mantisa": 52, "sesgo": 1023},
}


def _limpiar(bits: str) -> str:
    """Quita separadores visuales (espacios, ``|`` y ``_``) de la cadena."""
    return bits.replace(" ", "").replace("|", "").replace("_", "")


def _validar_bits(cadena: str) -> None:
    """Valida que `cadena` contenga solo caracteres ``0`` y ``1``."""
    if not cadena or any(c not in "01" for c in cadena):
        raise EntradaInvalidaError(
            "La entrada debe contener solo bits (0 y 1), opcionalmente con un "
            "punto binario o separadores ' ', '|', '_'."
        )


def _binario_con_punto_a_decimal(cadena: str) -> dict:
    """Convierte un binario posicional ``entera.fraccionaria`` a decimal."""
    signo = -1 if cadena.startswith("-") else 1
    cadena = cadena.lstrip("+-")

    if cadena.count(".") > 1:
        raise EntradaInvalidaError("La entrada tiene más de un punto binario.")
    parte_entera, _, parte_fraccion = cadena.partition(".")
    _validar_bits(parte_entera + parte_fraccion)

    valor_entero = int(parte_entera, 2) if parte_entera else 0
    valor_fraccion = 0.0
    for posicion, bit in enumerate(parte_fraccion, start=1):
        valor_fraccion += int(bit) * 2 ** (-posicion)

    valor = signo * (valor_entero + valor_fraccion)
    return {
        "entrada": ("-" if signo < 0 else "") + cadena,
        "modo": "binario posicional (con punto)",
        "parte entera (decimal)": float(valor_entero),
        "parte fraccionaria (decimal)": valor_fraccion,
        "valor decimal": valor,
    }


def _ieee_a_decimal(cadena: str, precision: str) -> dict:
    """Descompone una palabra IEEE 754 y reconstruye su valor decimal."""
    fmt = _FORMATOS[precision]
    n = fmt["bits"]
    if len(cadena) != n:
        raise EntradaInvalidaError(
            f"Para precisión '{precision}' se esperan {n} bits, se "
            f"recibieron {len(cadena)}."
        )

    signo_bit = cadena[0]
    caracteristica = cadena[1 : 1 + fmt["exp"]]
    mantisa = cadena[1 + fmt["exp"] :]

    signo = -1 if signo_bit == "1" else 1
    valor_caracteristica = int(caracteristica, 2)
    mantisa_entera = int(mantisa, 2) if mantisa else 0
    mantisa_fraccion = mantisa_entera / (2 ** fmt["mantisa"])
    sesgo = fmt["sesgo"]
    exp_max = 2 ** fmt["exp"] - 1  # característica con todos los bits en 1

    if valor_caracteristica == exp_max:
        # Casos especiales: infinito o NaN.
        if mantisa_entera == 0:
            valor: float = signo * math.inf
            exponente_real: int | str = "—"
            significando: float | str = "—"
            nota = "infinito" + (" negativo" if signo < 0 else "")
        else:
            valor = math.nan
            exponente_real = "—"
            significando = "—"
            nota = "NaN (no es número)"
    elif valor_caracteristica == 0:
        # Subnormal (o cero): sin el 1 implícito, exponente 1 - sesgo.
        exponente_real = 1 - sesgo
        significando = mantisa_fraccion
        valor = signo * significando * 2 ** exponente_real
        nota = "cero" if mantisa_entera == 0 else "subnormal (sin 1 implícito)"
    else:
        # Normalizado: con el 1 implícito.
        exponente_real = valor_caracteristica - sesgo
        significando = 1 + mantisa_fraccion
        valor = signo * significando * 2 ** exponente_real
        nota = "normalizado (con 1 implícito)"

    return {
        "entrada": cadena,
        "modo": f"IEEE 754 {precision} ({n} bits)",
        "signo": f"{signo_bit}  ({'negativo' if signo < 0 else 'positivo'})",
        "caracteristica": f"{caracteristica}  = {valor_caracteristica}",
        "exponente real (sin sesgo)": exponente_real,
        "mantisa": mantisa,
        "significando (1.mantisa)": significando,
        "tipo": nota,
        "valor decimal": valor,
    }


def binario_a_decimal(bits: str, precision: str = "doble") -> dict:
    """Convierte una cadena binaria a decimal.

    Detecta el modo automáticamente: si contiene un punto se trata como
    binario posicional; si no, se interpreta como una palabra IEEE 754 de la
    `precision` indicada, desglosando signo, característica y mantisa.

    Args:
        bits: Cadena de ``0`` y ``1`` (admite ``.``, espacios, ``|`` y ``_``).
        precision: ``"simple"`` (32 bits) o ``"doble"`` (64 bits); solo aplica
            al modo IEEE 754.

    Returns:
        Diccionario con el desglose de la conversión y el valor decimal.

    Raises:
        EntradaInvalidaError: Si la cadena no es binaria válida, la precisión
            es desconocida o la longitud no coincide con el formato IEEE 754.
    """
    if precision not in _FORMATOS:
        raise EntradaInvalidaError(
            f"Precisión inválida: '{precision}'. Use 'simple' o 'doble'."
        )
    if not isinstance(bits, str) or not bits.strip():
        raise EntradaInvalidaError("La entrada binaria no puede estar vacía.")

    limpio = _limpiar(bits.strip())

    if "." in limpio:
        return _binario_con_punto_a_decimal(limpio)

    _validar_bits(limpio.lstrip("+-"))
    return _ieee_a_decimal(limpio.lstrip("+-"), precision)
