"""Conversión decimal -> binario.

Ofrece dos vistas complementarias de un número decimal:

1. La conversión *directa* del número a binario (parte entera por divisiones
   sucesivas y parte fraccionaria por multiplicaciones sucesivas).
2. Su representación en **punto flotante IEEE 754** (precisión simple de 32
   bits o doble de 64 bits), desglosada en sus tres campos: bit de **signo**,
   **característica** (exponente sesgado) y **mantisa**.

Un archivo por conversión/algoritmo, según la convención del subpaquete.
"""

from __future__ import annotations

import struct

from utils.errores import EntradaInvalidaError

# Parámetros de cada formato IEEE 754.
# - "struct": código de `struct` (big-endian) para empaquetar el float.
# - "bits"  : ancho total de la palabra.
# - "exp"   : bits de característica (exponente sesgado).
# - "mantisa": bits de mantisa (fracción).
# - "sesgo" : sesgo (bias) que se resta a la característica.
_FORMATOS: dict[str, dict[str, int | str]] = {
    "simple": {"struct": ">f", "bits": 32, "exp": 8, "mantisa": 23, "sesgo": 127},
    "doble": {"struct": ">d", "bits": 64, "exp": 11, "mantisa": 52, "sesgo": 1023},
}

# Máximo de bits que se generan para la parte fraccionaria en la conversión
# directa (evita bucles infinitos cuando la fracción es periódica en binario).
_MAX_BITS_FRACCION = 60


def _real_a_binario_directo(numero: float, max_bits_fraccion: int) -> str:
    """Convierte un real a binario por el método clásico (entera.fraccionaria).

    Parte entera: divisiones sucesivas entre 2. Parte fraccionaria:
    multiplicaciones sucesivas por 2, tomando el acarreo entero. La parte
    fraccionaria se trunca a `max_bits_fraccion` bits si es periódica.
    """
    signo = "-" if numero < 0 else ""
    x = abs(numero)
    parte_entera = int(x)
    fraccion = x - parte_entera

    bin_entero = bin(parte_entera)[2:]  # "0b1010" -> "1010"

    bits_fraccion: list[str] = []
    while fraccion > 0 and len(bits_fraccion) < max_bits_fraccion:
        fraccion *= 2
        bit = int(fraccion)
        bits_fraccion.append(str(bit))
        fraccion -= bit

    if bits_fraccion:
        return f"{signo}{bin_entero}.{''.join(bits_fraccion)}"
    return f"{signo}{bin_entero}"


def decimal_a_binario(numero: float, precision: str = "doble") -> dict:
    """Convierte un número decimal a binario y a su forma IEEE 754.

    Args:
        numero: Número en base 10 a convertir (admite parte fraccionaria y
            signo).
        precision: ``"simple"`` (32 bits) o ``"doble"`` (64 bits).

    Returns:
        Diccionario con la conversión directa y el desglose IEEE 754: signo,
        característica (exponente sesgado y su valor real) y mantisa.

    Raises:
        EntradaInvalidaError: Si `precision` no es ``"simple"`` ni ``"doble"``
            o si `numero` no es numérico.
    """
    if precision not in _FORMATOS:
        raise EntradaInvalidaError(
            f"Precisión inválida: '{precision}'. Use 'simple' o 'doble'."
        )
    try:
        numero = float(numero)
    except (TypeError, ValueError) as exc:
        raise EntradaInvalidaError(f"'{numero}' no es un número válido.") from exc

    fmt = _FORMATOS[precision]
    bits_exp = int(fmt["exp"])
    sesgo = int(fmt["sesgo"])

    # Patrón de bits exacto que el hardware almacena para este float.
    empaquetado = struct.pack(str(fmt["struct"]), numero)
    entero = int.from_bytes(empaquetado, "big")
    bits = format(entero, f"0{int(fmt['bits'])}b")

    signo = bits[0]
    caracteristica = bits[1 : 1 + bits_exp]
    mantisa = bits[1 + bits_exp :]
    valor_caracteristica = int(caracteristica, 2)

    # Exponente real (sin sesgo). En subnormales (característica = 0) el
    # exponente efectivo es 1 - sesgo.
    if valor_caracteristica == 0:
        exponente_real = 1 - sesgo if int(mantisa, 2) else 0
    else:
        exponente_real = valor_caracteristica - sesgo

    ieee_agrupado = f"{signo} | {caracteristica} | {mantisa}"

    return {
        "numero": numero,
        "precision": f"{precision} ({int(fmt['bits'])} bits)",
        "binario directo": _real_a_binario_directo(numero, _MAX_BITS_FRACCION),
        "signo": f"{signo}  ({'negativo' if signo == '1' else 'positivo'})",
        "caracteristica": f"{caracteristica}  = {valor_caracteristica}",
        "exponente real (sin sesgo)": exponente_real,
        "mantisa": mantisa,
        "IEEE 754 (signo | caracteristica | mantisa)": ieee_agrupado,
        "binario IEEE 754 completo": bits,
    }
