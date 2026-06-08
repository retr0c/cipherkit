"""
tools/analyzer.py — Análisis de texto cifrado.
Frecuencia de letras, índice de coincidencia, detección de idioma,
y scoring general de legibilidad.
"""

from utils.wordlist import get_freq, get_words, get_bigrams, FREQ_ES, FREQ_EN


# ─────────────────────────────────────────────────────────────
# ANÁLISIS DE FRECUENCIA
# ─────────────────────────────────────────────────────────────

def letter_frequency(text: str) -> dict[str, float]:
    """Retorna frecuencia relativa de cada letra en el texto (0.0–1.0)."""
    letters = [c.lower() for c in text if c.isalpha()]
    total   = len(letters)
    if not total:
        return {}
    counts = {}
    for c in letters:
        counts[c] = counts.get(c, 0) + 1
    return {c: n / total for c, n in sorted(counts.items())}


def index_of_coincidence(text: str) -> float:
    """
    IC del texto.
    Natural español ≈ 0.075 | Natural inglés ≈ 0.065 | Aleatorio ≈ 0.038
    """
    letters = [c.lower() for c in text if c.isalpha()]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = {}
    for c in letters:
        counts[c] = counts.get(c, 0) + 1
    return sum(f * (f - 1) for f in counts.values()) / (n * (n - 1))


def detect_language(text: str) -> str:
    """
    Detecta si el texto parece español o inglés comparando
    frecuencias de letras. Retorna 'es' o 'en'.
    """
    observed = letter_frequency(text)
    if not observed:
        return "es"

    def dist(freq_table):
        return sum(abs(observed.get(c, 0) - freq_table.get(c, 0)) for c in "abcdefghijklmnopqrstuvwxyz")

    return "es" if dist(FREQ_ES) <= dist(FREQ_EN) else "en"


# ─────────────────────────────────────────────────────────────
# SCORING DE LEGIBILIDAD
# ─────────────────────────────────────────────────────────────

def legibility_score(text: str, lang: str = None) -> float:
    """
    Puntúa la legibilidad del texto (0.0–1.0).
    Mayor score = más probable que sea texto natural descifrado correctamente.

    Combina:
    - Correlación de frecuencia de letras (40%)
    - % de palabras reconocidas (40%)
    - % de bigramas frecuentes (20%)
    """
    if lang is None:
        lang = detect_language(text)

    freq    = get_freq(lang)
    words   = get_words(lang)
    bigrams = get_bigrams(lang)

    letters = [c.lower() for c in text if c.isalpha()]
    if len(letters) < 4:
        return 0.0

    # Frecuencia de letras
    total    = len(letters)
    counts   = {}
    for c in letters:
        counts[c] = counts.get(c, 0) + 1
    observed = {c: n / total for c, n in counts.items()}

    freq_score = 0.0
    for c, expected in freq.items():
        got = observed.get(c, 0.0)
        freq_score += 1.0 - min(abs(got - expected) / max(expected, 0.001), 1.0)
    freq_score /= 26

    # Palabras reconocidas
    raw_words  = [w.strip(".,;:!?\"'()[]{}—-").lower() for w in text.split()]
    real_words = [w for w in raw_words if len(w) >= 2]
    word_score = 0.0
    if real_words:
        hits = sum(1 for w in real_words if w in words)
        word_score = hits / len(real_words)

    # Bigramas
    bigram_hits  = sum(1 for i in range(len(letters)-1) if letters[i]+letters[i+1] in bigrams)
    bigram_score = bigram_hits / max(len(letters) - 1, 1)

    return freq_score * 0.40 + word_score * 0.40 + bigram_score * 0.20


def quick_score(text: str) -> float:
    """Score rápido usando el mejor resultado entre ES y EN."""
    return max(legibility_score(text, "es"), legibility_score(text, "en"))


# ─────────────────────────────────────────────────────────────
# DETECCIÓN DE TIPO DE CIFRADO
# ─────────────────────────────────────────────────────────────

def suggest_ciphers(text: str) -> list[tuple[str, str]]:
    """
    Analiza el texto y sugiere qué cifrados podría tener.
    Retorna lista de (cifrado, razón).
    """
    suggestions = []
    ic = index_of_coincidence(text)
    letters = [c for c in text if c.isalpha()]
    has_invisible = any(ord(c) in (0x200b, 0x200c, 0x200d) for c in text)
    has_nonalpha  = any(not c.isalpha() and not c.isspace() for c in text)

    if has_invisible:
        suggestions.append(("stego", "Contiene caracteres Unicode invisibles"))

    if ic > 0.060:
        suggestions.append(("caesar",     f"IC alto ({ic:.3f}) → posible sustitución simple"))
        suggestions.append(("rot13",      f"IC alto ({ic:.3f}) → posible ROT13"))
        suggestions.append(("atbash",     f"IC alto ({ic:.3f}) → posible Atbash"))
        suggestions.append(("box_caesar", f"IC alto ({ic:.3f}) → posible Caja Caesar"))
    elif 0.040 < ic <= 0.060:
        suggestions.append(("vigenere", f"IC medio ({ic:.3f}) → posible Vigenère o cifrado polialfabético"))

    if has_nonalpha:
        suggestions.append(("box_caesar", "Contiene separadores no-alfabéticos → posible Caja Caesar"))

    if not suggestions:
        suggestions.append(("vigenere", f"IC bajo ({ic:.3f}) → texto posiblemente aleatorio o cifrado fuerte"))

    return suggestions


# ─────────────────────────────────────────────────────────────
# REPORTE COMPLETO
# ─────────────────────────────────────────────────────────────

def full_report(text: str) -> dict:
    """
    Genera un reporte completo de análisis del texto.
    """
    letters  = [c for c in text if c.isalpha()]
    ic       = index_of_coincidence(text)
    lang     = detect_language(text)
    score    = legibility_score(text, lang)
    freq     = letter_frequency(text)
    top5     = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
    suggestions = suggest_ciphers(text)

    return {
        "longitud_total":  len(text),
        "total_letras":    len(letters),
        "ic":              round(ic, 4),
        "idioma_probable": "Español" if lang == "es" else "Inglés",
        "score_legib":     round(score, 4),
        "top5_letras":     top5,
        "sugerencias":     suggestions,
    }