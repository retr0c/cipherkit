"""
tools/passwords.py — Generador y evaluador de contraseñas seguras.
"""

import random
import string

_RNG = random.SystemRandom()

# ─────────────────────────────────────────────────────────────
# GENERACIÓN
# ─────────────────────────────────────────────────────────────

_AMBIGUOUS = set("lI1O0oB8S5Z2")
_SYMBOLS   = "!@#$%^&*()-_=+[]{}|;:,.<>?"

def generate(length: int = 16, use_symbols: bool = True, no_ambiguous: bool = True) -> str:
    """Genera una contraseña criptográficamente segura."""
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += _SYMBOLS
    if no_ambiguous:
        chars = "".join(c for c in chars if c not in _AMBIGUOUS)
    if not chars:
        chars = string.ascii_letters + string.digits
    return "".join(_RNG.choice(chars) for _ in range(length))


def generate_passphrase(word_count: int = 4, separator: str = "-") -> str:
    """
    Genera una passphrase de palabras aleatorias (estilo Diceware).
    Más fácil de recordar y muy segura con 4+ palabras.
    """
    wordlist = [
        "apple","brave","cloud","dance","eagle","flame","grace","house","ivory","jungle",
        "karma","lemon","magic","night","ocean","piano","queen","river","storm","tiger",
        "ultra","venus","water","xenon","youth","zebra","amber","blaze","crisp","drift",
        "ember","frost","gloom","haste","ideal","joker","kneel","lunar","mirth","noble",
        "ombre","prism","quill","raven","shine","tower","umbra","vault","wheat","xerox",
        "yarns","zones","acute","bloom","cedar","dense","exact","finch","grind","honor",
        "inbox","jewel","knack","lived","mason","nerve","onset","pixel","quota","rider",
        "scout","truce","unwed","viper","woken","xylem","yodel","zonal","adept","boxer",
    ]
    return separator.join(_RNG.choice(wordlist) for _ in range(word_count))


# ─────────────────────────────────────────────────────────────
# EVALUACIÓN (funciona con cualquier contraseña, no solo generadas)
# ─────────────────────────────────────────────────────────────

def strength(password: str) -> str:
    """Evalúa la fortaleza de cualquier contraseña."""
    score = _score(password)
    labels = {0:"Muy débil", 1:"Muy débil", 2:"Débil", 3:"Media", 4:"Buena", 5:"Fuerte", 6:"Muy fuerte"}
    return labels.get(score, "Muy fuerte")


def strength_detail(password: str) -> dict:
    """
    Retorna un análisis detallado de la contraseña.
    Útil para mostrar qué criterios cumple o le faltan.
    """
    checks = {
        "longitud_12+":        len(password) >= 12,
        "longitud_20+":        len(password) >= 20,
        "tiene_minusculas":    any(c.islower() for c in password),
        "tiene_mayusculas":    any(c.isupper() for c in password),
        "tiene_numeros":       any(c.isdigit() for c in password),
        "tiene_simbolos":      any(not c.isalnum() for c in password),
    }
    score  = sum(checks.values())
    labels = {0:"Muy débil", 1:"Muy débil", 2:"Débil", 3:"Media", 4:"Buena", 5:"Fuerte", 6:"Muy fuerte"}
    return {
        "nivel":   labels.get(score, "Muy fuerte"),
        "score":   score,
        "maximo":  6,
        "checks":  checks,
        "entropia_bits": _entropy_bits(password),
    }


def _score(password: str) -> int:
    score = 0
    if len(password) >= 12:               score += 1
    if len(password) >= 20:               score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    return score


def _entropy_bits(password: str) -> float:
    """Estima entropía en bits basada en el charset usado."""
    import math
    charset = 0
    if any(c.islower() for c in password):       charset += 26
    if any(c.isupper() for c in password):       charset += 26
    if any(c.isdigit() for c in password):       charset += 10
    if any(c in _SYMBOLS for c in password):     charset += len(_SYMBOLS)
    other = any(c not in string.ascii_letters + string.digits + _SYMBOLS for c in password)
    if other:                                    charset += 32
    if charset == 0:                             return 0.0
    return round(len(password) * math.log2(charset), 1)