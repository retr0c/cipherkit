"""
Steganography — hide messages inside innocent-looking text
using zero-width Unicode characters (invisible to the naked eye).
"""

# Zero-width space = bit 0, Zero-width non-joiner = bit 1
_BIT0 = "\u200b"  # zero-width space
_BIT1 = "\u200c"  # zero-width non-joiner
_SEP  = "\u200d"  # zero-width joiner (separator)

def _text_to_bits(text):
    bits = []
    for c in text:
        b = format(ord(c), "016b")
        bits.extend(b)
    return bits

def _bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 16):
        chunk = bits[i:i+16]
        if len(chunk) < 16:
            break
        chars.append(chr(int("".join(chunk), 2)))
    return "".join(chars)

def hide(cover_text, secret):
    hidden = _SEP.join(_BIT1 if b == "1" else _BIT0 for b in _text_to_bits(secret))
    return cover_text + _SEP + hidden

def reveal(text):
    if _SEP not in text:
        return None
    parts = text.split(_SEP)
    bits  = []
    for ch in parts[1:]:
        if ch == _BIT0:
            bits.append("0")
        elif ch == _BIT1:
            bits.append("1")
    if not bits:
        return None
    return _bits_to_text(bits)

def has_hidden(text):
    return _SEP in text