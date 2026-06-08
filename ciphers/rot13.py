"""
ciphers/rot13.py — ROT13 con str.translate() precomputado.
"""

_U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_L = 'abcdefghijklmnopqrstuvwxyz'
_TABLE = str.maketrans(_U + _L, _U[13:]+_U[:13] + _L[13:]+_L[:13])


def apply(text: str) -> str:
    return text.translate(_TABLE)


encrypt = decrypt = apply


def score(text: str) -> float:
    from ciphers.caesar import score as caesar_score
    return caesar_score(text)