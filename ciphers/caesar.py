"""
ciphers/caesar.py — Caesar cipher optimizado con str.translate() precomputado.
"""

from utils.wordlist import get_freq, get_words, get_bigrams

# ─────────────────────────────────────────────────────────────
# TABLAS PRECOMPUTADAS (una sola vez al importar)
# ─────────────────────────────────────────────────────────────

_U = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_L = 'abcdefghijklmnopqrstuvwxyz'

# _ENC_TABLES[k] = tabla para cifrar con clave k
# _DEC_TABLES[k] = tabla para descifrar con clave k (= cifrar con -k)
_ENC_TABLES = {}
_DEC_TABLES = {}
for _k in range(26):
    _dk = (-_k) % 26
    _ENC_TABLES[_k] = str.maketrans(_U + _L, _U[_k:]+_U[:_k] + _L[_k:]+_L[:_k])
    _DEC_TABLES[_k] = str.maketrans(_U + _L, _U[_dk:]+_U[:_dk] + _L[_dk:]+_L[:_dk])


# ─────────────────────────────────────────────────────────────
# CORE
# ─────────────────────────────────────────────────────────────

def encrypt(text: str, key: int) -> str:
    return text.translate(_ENC_TABLES[key % 26])

def decrypt(text: str, key: int) -> str:
    return text.translate(_DEC_TABLES[key % 26])


# ─────────────────────────────────────────────────────────────
# SCORING
# ─────────────────────────────────────────────────────────────

def _score(text: str, lang: str = "es") -> float:
    freq    = get_freq(lang)
    words   = get_words(lang)
    bigrams = get_bigrams(lang)

    counts = {}
    total = 0
    for c in text:
        o = ord(c)
        if 97 <= o <= 122:
            counts[c] = counts.get(c, 0) + 1; total += 1
        elif 65 <= o <= 90:
            lc = chr(o + 32)
            counts[lc] = counts.get(lc, 0) + 1; total += 1
    if total < 4:
        return 0.0

    freq_score = sum(
        1.0 - min(abs(counts.get(c, 0) / total - e) / max(e, 0.001), 1.0)
        for c, e in freq.items()
    ) / 26

    hits = tw = 0
    for w in text.split():
        w2 = w.strip(".,;:!?\"'()[]{}—-").lower()
        if len(w2) >= 2:
            tw += 1
            if w2 in words: hits += 1
    word_score = hits / tw if tw else 0.0

    bg_hits = bg_total = 0
    prev = None
    for c in text:
        if c.isalpha():
            lc = c.lower()
            if prev:
                bg_total += 1
                if prev + lc in bigrams: bg_hits += 1
            prev = lc
    bigram_score = bg_hits / max(bg_total, 1)

    return freq_score * 0.40 + word_score * 0.40 + bigram_score * 0.20


def score(text: str, lang: str = "es") -> float:
    return max(_score(text, "es"), _score(text, "en"))


# ─────────────────────────────────────────────────────────────
# BRUTE FORCE
# ─────────────────────────────────────────────────────────────

def brute_force(text: str, lang: str = "es") -> list[tuple[int, str, float]]:
    results = []
    for k in range(1, 26):
        candidate = decrypt(text, k)
        s = _score(candidate, lang)
        results.append((k, candidate, s))
    results.sort(key=lambda x: x[2], reverse=True)
    return results