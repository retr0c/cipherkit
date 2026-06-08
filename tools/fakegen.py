"""
tools/fakegen.py — Generador de datos falsos para testing y desarrollo.
"""

import random
import uuid as _uuid

_RNG = random.SystemRandom()

FIRST = ["Alex","Jordan","Morgan","Taylor","Casey","Riley","Avery","Quinn","Drew","Sam",
         "Blake","Reese","Skyler","Dakota","Peyton","Rowan","Emery","Finley","Harley","Logan",
         "Maria","Carlos","Juan","Ana","Luis","Pedro","Sofia","Miguel","Isabel","Jose",
         "Laura","Alejandro","Nicolas","Valentina","Sebastian","Camila","Daniel","Paula"]
LAST  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson",
         "Moore","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Lee",
         "Gonzalez","Rodriguez","Martinez","Hernandez","Lopez","Perez","Sanchez","Ramirez"]
DOMAINS    = ["gmail.com","yahoo.com","outlook.com","protonmail.com","hotmail.com","icloud.com"]
TLDS       = ["com","net","org","io","dev","app","co"]
DARK_WORDS = ["dark","cyber","ghost","void","proxy","null","shadow","byte","hex","core",
               "neon","pulse","sigma","delta","omega","krypt","nexus","flux","zero","apex"]

# ─────────────────────────────────────────────────────────────
# IDENTIDAD
# ─────────────────────────────────────────────────────────────

def fake_name() -> str:
    return f"{_RNG.choice(FIRST)} {_RNG.choice(LAST)}"

def fake_email(name: str = None) -> str:
    name = name or fake_name()
    parts = name.lower().split()
    first, last = parts[0], parts[-1]
    sep = _RNG.choice([".", "_", ""])
    num = str(_RNG.randint(1, 999)) if _RNG.random() > 0.5 else ""
    return f"{first}{sep}{last}{num}@{_RNG.choice(DOMAINS)}"

def fake_ip() -> str:
    return ".".join(str(_RNG.randint(1, 254)) for _ in range(4))

def fake_mac() -> str:
    return ":".join(f"{_RNG.randint(0, 255):02X}" for _ in range(6))

def fake_uuid() -> str:
    return str(_uuid.uuid4())

def fake_coordinates() -> dict:
    """Coordenadas aleatorias dentro de Colombia."""
    lat = round(_RNG.uniform(-4.23, 12.45), 6)
    lon = round(_RNG.uniform(-81.73, -66.87), 6)
    return {"lat": lat, "lon": lon}

# ─────────────────────────────────────────────────────────────
# TARJETA DE CRÉDITO (Luhn correcto)
# ─────────────────────────────────────────────────────────────

def _luhn_checksum(number_str: str) -> int:
    """Calcula el dígito de verificación Luhn para un número parcial."""
    digits = [int(d) for d in number_str]
    # Doble cada segundo dígito desde la derecha
    for i in range(len(digits) - 1, -1, -2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    return (10 - sum(digits) % 10) % 10

def fake_card() -> dict:
    """
    Genera tarjeta Luhn-válida de 16 dígitos.
    SOLO PARA TESTING — completamente ficticia.
    """
    # Visa: empieza con 4, 15 dígitos base + 1 check
    prefix  = "4" + "".join(str(_RNG.randint(0, 9)) for _ in range(14))
    check   = _luhn_checksum(prefix)
    number  = prefix + str(check)

    exp_m  = str(_RNG.randint(1, 12)).zfill(2)
    exp_y  = str(_RNG.randint(26, 30))
    cvv    = str(_RNG.randint(100, 999))
    return {"number": number, "expiry": f"{exp_m}/{exp_y}", "cvv": cvv, "type": "Visa (FAKE)"}

# ─────────────────────────────────────────────────────────────
# OTROS
# ─────────────────────────────────────────────────────────────

def fake_domain() -> str:
    return f"{_RNG.choice(DARK_WORDS)}{_RNG.choice(DARK_WORDS)}.{_RNG.choice(TLDS)}"

def fake_user_agent() -> str:
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
        "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
    ]
    return _RNG.choice(agents)

def fake_cedula_colombia() -> str:
    """Genera número de cédula colombiana ficticia (formato válido, no real)."""
    return str(_RNG.randint(10_000_000, 1_299_999_999))

def fake_phone_colombia() -> str:
    """Genera número de celular colombiano ficticio."""
    prefix = _RNG.choice(["300","301","302","304","305","310","311","312",
                           "313","314","315","316","317","318","319","320",
                           "321","322","323","324","350","351"])
    return f"+57 {prefix} {_RNG.randint(100,999)} {_RNG.randint(1000,9999)}"