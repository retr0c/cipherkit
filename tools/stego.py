"""
tools/stego.py — Esteganografía Unicode.
Oculta mensajes usando caracteres zero-width invisibles.
Fix: usa marcador de inicio/fin propio para evitar falsos positivos con emojis.
"""

# Marcadores propios — secuencia de inicio y fin del mensaje oculto
# Se usa U+2060 (Word Joiner) como delimitador — no aparece en emojis normales
_START = "\u2060\u200b\u2060"   # marcador de inicio
_END   = "\u2060\u200c\u2060"   # marcador de fin
_BIT0  = "\u200b"               # zero-width space = bit 0
_BIT1  = "\u200c"               # zero-width non-joiner = bit 1
_SEP   = "\u200d"               # zero-width joiner = separador entre bits


def _text_to_bits(text: str) -> list[str]:
    bits = []
    for c in text:
        b = format(ord(c), "016b")
        bits.extend(b)
    return bits


def _bits_to_text(bits: list[str]) -> str:
    chars = []
    for i in range(0, len(bits), 16):
        chunk = bits[i:i+16]
        if len(chunk) < 16:
            break
        chars.append(chr(int("".join(chunk), 2)))
    return "".join(chars)


def hide(cover_text: str, secret: str) -> str:
    """
    Oculta secret dentro de cover_text usando caracteres Unicode invisibles.
    Retorna el texto portador con el mensaje oculto incrustado al final.
    """
    encoded = _SEP.join(_BIT1 if b == "1" else _BIT0 for b in _text_to_bits(secret))
    return cover_text + _START + encoded + _END


def reveal(text: str) -> str | None:
    """
    Extrae el mensaje oculto de un texto.
    Retorna el mensaje o None si no hay nada.
    """
    if _START not in text or _END not in text:
        return None
    try:
        inner = text.split(_START, 1)[1].split(_END, 1)[0]
    except IndexError:
        return None

    bits = []
    for ch in inner.split(_SEP):
        if ch == _BIT0:
            bits.append("0")
        elif ch == _BIT1:
            bits.append("1")

    if not bits:
        return None
    result = _bits_to_text(bits)
    return result if result else None


def has_hidden(text: str) -> bool:
    """
    Detecta si un texto contiene un mensaje oculto con nuestro formato.
    Usa marcadores propios para evitar falsos positivos con emojis.
    """
    return _START in text and _END in text


def analyze(text: str) -> dict:
    """
    Análisis detallado de caracteres invisible en un texto.
    Útil para detectar esteganografía de terceros.
    """
    zwsp  = text.count("\u200b")
    zwnj  = text.count("\u200c")
    zwj   = text.count("\u200d")
    wj    = text.count("\u2060")
    total = zwsp + zwnj + zwj + wj

    return {
        "tiene_mensaje_propio":     has_hidden(text),
        "zero_width_space_u200b":   zwsp,
        "zero_width_nonjoin_u200c": zwnj,
        "zero_width_joiner_u200d":  zwj,
        "word_joiner_u2060":        wj,
        "total_invisibles":         total,
        "sospechoso":               total > 5 and not has_hidden(text),
    }