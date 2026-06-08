"""
ciphers/atbash.py — Atbash con str.translate() precomputado.
"""

_U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_L = 'abcdefghijklmnopqrstuvwxyz'
_TABLE = str.maketrans(_U + _L, _U[::-1] + _L[::-1])


def apply(text: str) -> str:
    return text.translate(_TABLE)


encrypt = decrypt = apply


def score(text: str) -> float:
    from ciphers.caesar import score as caesar_score
    return caesar_score(text)