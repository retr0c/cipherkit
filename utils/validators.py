"""
validators.py — Validación centralizada de inputs para CipherKit
"""

import re


# ─────────────────────────────────────────────────────────────
# TEXTO / MENSAJES
# ─────────────────────────────────────────────────────────────

def validate_text(text: str, name: str = "Texto") -> tuple[bool, str]:
    """Valida que el texto no esté vacío."""
    if not text or not text.strip():
        return False, f"{name} no puede estar vacío."
    return True, ""


def validate_alpha_key(key: str, name: str = "Clave") -> tuple[bool, str]:
    """Valida que la clave contenga solo letras (para Vigenère)."""
    if not key:
        return False, f"{name} no puede estar vacía."
    if not key.isalpha():
        return False, f"{name} debe contener solo letras (sin números ni símbolos)."
    return True, ""


def validate_int_key(raw: str, name: str = "Clave", min_val: int = 1, max_val: int = 25) -> tuple[bool, str, int]:
    """
    Valida y parsea una clave numérica.
    Retorna (ok, mensaje_error, valor_int).
    """
    try:
        val = int(raw.strip())
    except ValueError:
        return False, f"{name} debe ser un número entero.", 0
    if not (min_val <= val <= max_val):
        return False, f"{name} debe estar entre {min_val} y {max_val}.", 0
    return True, "", val


def validate_length(raw: str, name: str = "Longitud", min_val: int = 1, max_val: int = 512) -> tuple[bool, str, int]:
    """Valida un número que representa una longitud."""
    return validate_int_key(raw, name, min_val, max_val)


# ─────────────────────────────────────────────────────────────
# RED / HOSTS
# ─────────────────────────────────────────────────────────────

def validate_host(host: str) -> tuple[bool, str]:
    """
    Valida hostname o IP para evitar inyección de comandos en subprocess.
    Solo permite letras, dígitos, puntos, guiones y dos puntos (IPv6).
    """
    if not host or not host.strip():
        return False, "El host no puede estar vacío."
    host = host.strip()
    pattern = r'^[a-zA-Z0-9.\-:]+$'
    if not re.match(pattern, host):
        return False, "Host inválido. Solo se permiten letras, números, puntos y guiones."
    if len(host) > 253:
        return False, "Host demasiado largo (máx 253 caracteres)."
    return True, ""


def validate_ip(ip: str) -> tuple[bool, str]:
    """Valida formato IPv4 básico."""
    if not ip or not ip.strip():
        return False, "La IP no puede estar vacía."
    parts = ip.strip().split(".")
    if len(parts) != 4:
        return False, "Formato IPv4 inválido. Ejemplo: 192.168.1.1"
    for part in parts:
        try:
            val = int(part)
            if not (0 <= val <= 255):
                raise ValueError
        except ValueError:
            return False, f"Octeto inválido: '{part}'. Cada parte debe ser 0–255."
    return True, ""


def validate_domain(domain: str) -> tuple[bool, str]:
    """Valida formato de dominio básico."""
    if not domain or not domain.strip():
        return False, "El dominio no puede estar vacío."
    domain = domain.strip()
    pattern = r'^[a-zA-Z0-9][a-zA-Z0-9.\-]*\.[a-zA-Z]{2,}$'
    if not re.match(pattern, domain):
        return False, "Dominio inválido. Ejemplo: google.com"
    return True, ""


# ─────────────────────────────────────────────────────────────
# CONTRASEÑAS
# ─────────────────────────────────────────────────────────────

def validate_password_length(raw: str) -> tuple[bool, str, int]:
    """Valida longitud de contraseña (4–512)."""
    ok, msg, val = validate_int_key(raw, "Longitud", min_val=4, max_val=512)
    return ok, msg, val


def validate_count(raw: str, min_val: int = 1, max_val: int = 10) -> tuple[bool, str, int]:
    """Valida cantidad (ej: cuántas contraseñas generar)."""
    return validate_int_key(raw, "Cantidad", min_val, max_val)


# ─────────────────────────────────────────────────────────────
# CAJA CAESAR
# ─────────────────────────────────────────────────────────────

def validate_box_size(raw: str) -> tuple[bool, str, int]:
    """Valida tamaño de caja para Caja Caesar (1–50)."""
    return validate_int_key(raw, "Tamaño de caja", min_val=1, max_val=50)


def validate_box_sep(sep: str) -> tuple[bool, str]:
    """Valida que el separador sea un único carácter no alfabético."""
    if not sep:
        return False, "El separador no puede estar vacío."
    if len(sep) != 1:
        return False, "El separador debe ser exactamente 1 carácter."
    if sep.isalpha():
        return False, "El separador no puede ser una letra (interferiría con el cifrado)."
    return True, ""


# ─────────────────────────────────────────────────────────────
# HELPERS INTERNOS
# ─────────────────────────────────────────────────────────────

def sanitize_text(text: str) -> str:
    """Elimina caracteres de control peligrosos pero preserva el contenido."""
    return "".join(c for c in text if ord(c) >= 32 or c in "\n\t")