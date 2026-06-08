"""
wordlist.py — Diccionario integrado para scoring de legibilidad.
Usado por el motor de brute force para detectar texto descifrado correctamente.
"""

# ─────────────────────────────────────────────────────────────
# FRECUENCIAS DE LETRAS (español normalizado a 1.0)
# ─────────────────────────────────────────────────────────────

FREQ_ES = {
    'a': 0.1253, 'b': 0.0142, 'c': 0.0468, 'd': 0.0586, 'e': 0.1368,
    'f': 0.0069, 'g': 0.0101, 'h': 0.0070, 'i': 0.0625, 'j': 0.0044,
    'k': 0.0002, 'l': 0.0497, 'm': 0.0315, 'n': 0.0671, 'o': 0.0868,
    'p': 0.0251, 'q': 0.0088, 'r': 0.0687, 's': 0.0798, 't': 0.0463,
    'u': 0.0393, 'v': 0.0090, 'w': 0.0001, 'x': 0.0022, 'y': 0.0090,
    'z': 0.0052,
}

FREQ_EN = {
    'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0425, 'e': 0.1270,
    'f': 0.0223, 'g': 0.0202, 'h': 0.0609, 'i': 0.0697, 'j': 0.0015,
    'k': 0.0077, 'l': 0.0403, 'm': 0.0241, 'n': 0.0675, 'o': 0.0751,
    'p': 0.0193, 'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
    'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015, 'y': 0.0197,
    'z': 0.0007,
}

# ─────────────────────────────────────────────────────────────
# PALABRAS COMUNES — ESPAÑOL
# ─────────────────────────────────────────────────────────────

WORDS_ES = {
    # artículos y determinantes
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "del", "al",
    # pronombres
    "yo", "tu", "el", "ella", "nosotros", "ellos", "ellas",
    "me", "te", "se", "nos", "le", "lo", "les",
    "este", "esta", "estos", "estas", "ese", "esa", "esos",
    "mi", "mis", "su", "sus",
    # preposiciones y conjunciones
    "de", "en", "con", "por", "para", "sin", "sobre", "bajo",
    "ante", "tras", "entre", "hacia", "desde", "hasta", "segun",
    "y", "o", "pero", "sino", "aunque", "porque", "que", "si",
    "como", "cuando", "donde", "mientras", "pues",
    # verbos comunes
    "es", "son", "era", "fue", "ser", "estar", "tener", "hacer",
    "poder", "querer", "saber", "ver", "dar", "ir", "venir",
    "hay", "ha", "han", "he", "hemos", "tiene", "tienen",
    "puede", "pueden", "quiere", "quieren", "sabe", "saben",
    "hace", "hacen", "va", "van", "viene", "vienen",
    "dije", "dijo", "dijeron", "hizo", "hicieron",
    # adverbios
    "no", "si", "mas", "muy", "bien", "mal", "ya", "aun",
    "tambien", "nunca", "siempre", "aqui", "alli", "ahi",
    "antes", "despues", "ahora", "hoy", "ayer", "manana",
    "solo", "todo", "nada", "algo", "alguien", "nadie",
    # palabras de alta frecuencia
    "que", "con", "una", "por", "sus", "les", "hay",
    "cual", "han", "vez", "dos", "tres", "mas",
    "otro", "otra", "otros", "otras", "mismo", "misma",
    "cada", "todo", "toda", "todos", "todas",
    "gran", "grande", "nuevo", "nueva", "primer", "primera",
    "caso", "parte", "vez", "tiempo", "dia", "vida", "mundo",
    "hombre", "mujer", "nino", "casa", "ciudad", "pais",
    "trabajo", "agua", "mano", "forma", "lugar", "grupo",
}

# ─────────────────────────────────────────────────────────────
# PALABRAS COMUNES — INGLÉS
# ─────────────────────────────────────────────────────────────

WORDS_EN = {
    # articles / determiners
    "the", "a", "an", "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their",
    # pronouns
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "us", "them", "who", "what", "which",
    # prepositions / conjunctions
    "of", "in", "to", "for", "on", "with", "at", "by",
    "from", "up", "about", "into", "through", "during",
    "and", "but", "or", "nor", "so", "yet", "if", "as",
    "than", "because", "when", "while", "although",
    # common verbs
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "will", "would", "could", "should", "may", "might",
    "can", "get", "got", "go", "went", "come", "came",
    "say", "said", "see", "saw", "know", "knew",
    "think", "thought", "take", "took", "make", "made",
    # adverbs / adjectives
    "not", "no", "yes", "just", "also", "very", "more",
    "all", "some", "any", "much", "many", "most",
    "one", "two", "three", "new", "old", "first", "last",
    "now", "then", "here", "there", "where", "how", "why",
    "never", "always", "still", "again", "too", "well",
    # high-freq nouns
    "time", "year", "people", "way", "day", "man", "woman",
    "world", "life", "hand", "part", "place", "case", "group",
    "work", "government", "company", "number", "night",
}

# ─────────────────────────────────────────────────────────────
# BIGRAMAS FRECUENTES (pares de letras consecutivas)
# para detectar texto con estructura natural
# ─────────────────────────────────────────────────────────────

BIGRAMS_ES = {
    "de", "en", "es", "el", "la", "os", "ar", "er", "or",
    "al", "re", "on", "an", "ie", "ra", "se", "ue", "as",
    "ta", "te", "co", "lo", "ma", "na", "ro", "ca", "st",
    "to", "ti", "pr", "le", "no", "ne", "ri", "tr", "ul",
}

BIGRAMS_EN = {
    "th", "he", "in", "er", "an", "re", "on", "en", "at",
    "es", "ed", "ti", "or", "hi", "as", "to", "it", "is",
    "nd", "ha", "nt", "ou", "st", "ng", "al", "be", "de",
    "ea", "io", "le", "ve", "co", "me", "ow", "ri", "ro",
}

# Agrégalos a tu lista existente
WORDS_ES.update({
    "programa", "parece", "funcionar", "sistema", "seguridad", 
    "cifrado", "descifrar", "hacker", "toolkit", "archivo",
    "computadora", "proceso", "algoritmo", "fuerza", "bruta", "nicole"
})

# ─────────────────────────────────────────────────────────────
# API PÚBLICA
# ─────────────────────────────────────────────────────────────

def get_words(lang: str = "es") -> set:
    """Retorna el conjunto de palabras para el idioma dado ('es' o 'en')."""
    return WORDS_ES if lang == "es" else WORDS_EN


def get_freq(lang: str = "es") -> dict:
    """Retorna la tabla de frecuencias de letras para el idioma dado."""
    return FREQ_ES if lang == "es" else FREQ_EN


def get_bigrams(lang: str = "es") -> set:
    """Retorna el conjunto de bigramas frecuentes para el idioma dado."""
    return BIGRAMS_ES if lang == "es" else BIGRAMS_EN