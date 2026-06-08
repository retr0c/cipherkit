"""
ciphers/chain.py — Pipeline para encadenar múltiples cifrados.
Permite cifrar/descifrar aplicando una secuencia de cifrados en orden.
"""

from ciphers import caesar, vigenere, rot13, atbash, box_caesar

# ─────────────────────────────────────────────────────────────
# IDENTIFICADORES DE CIFRADOS
# ─────────────────────────────────────────────────────────────

CIPHER_IDS = {
    "caesar":     "Caesar",
    "vigenere":   "Vigenère",
    "rot13":      "ROT13",
    "atbash":     "Atbash",
    "box_caesar": "Caja Caesar",
}


# ─────────────────────────────────────────────────────────────
# PASO DE PIPELINE
# ─────────────────────────────────────────────────────────────

class CipherStep:
    """
    Representa un paso individual en el pipeline de cifrado.

    Attributes:
        cipher_id : identificador del cifrado (ver CIPHER_IDS)
        params    : dict con parámetros específicos del cifrado
                    caesar      → {"key": int}
                    vigenere    → {"key": str}
                    rot13       → {}
                    atbash      → {}
                    box_caesar  → {"key": int, "sep": str, "box_size": int}
    """

    def __init__(self, cipher_id: str, params: dict = None):
        if cipher_id not in CIPHER_IDS:
            raise ValueError(f"Cifrado desconocido: '{cipher_id}'. Opciones: {list(CIPHER_IDS)}")
        self.cipher_id = cipher_id
        self.params    = params or {}

    def encrypt(self, text: str) -> str:
        cid = self.cipher_id
        p   = self.params
        if cid == "caesar":
            return caesar.encrypt(text, p.get("key", 13))
        if cid == "vigenere":
            return vigenere.encrypt(text, p.get("key", "key"))
        if cid == "rot13":
            return rot13.apply(text)
        if cid == "atbash":
            return atbash.apply(text)
        if cid == "box_caesar":
            return box_caesar.encrypt(text, p.get("key", 7), p.get("sep", "."), p.get("box_size", 0))
        return text

    def decrypt(self, text: str) -> str:
        cid = self.cipher_id
        p   = self.params
        if cid == "caesar":
            return caesar.decrypt(text, p.get("key", 13))
        if cid == "vigenere":
            return vigenere.decrypt(text, p.get("key", "key"))
        if cid == "rot13":
            return rot13.apply(text)
        if cid == "atbash":
            return atbash.apply(text)
        if cid == "box_caesar":
            return box_caesar.decrypt(text, p.get("key", 7), p.get("sep", "."), p.get("box_size", 0))
        return text

    def __repr__(self) -> str:
        return f"CipherStep({self.cipher_id}, {self.params})"

    def describe(self) -> str:
        cid  = CIPHER_IDS[self.cipher_id]
        p    = self.params
        if self.cipher_id == "caesar":
            return f"{cid} (clave: {p.get('key', 13)})"
        if self.cipher_id == "vigenere":
            return f"{cid} (clave: '{p.get('key', 'key')}')"
        if self.cipher_id == "box_caesar":
            return (f"{cid} (clave: {p.get('key',7)}, "
                    f"sep: '{p.get('sep','.')}', "
                    f"caja: {p.get('box_size',0)})")
        return cid


# ─────────────────────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────────────────────

class CipherChain:
    """
    Secuencia ordenada de CipherStep.
    encrypt() aplica los pasos de izquierda a derecha.
    decrypt() aplica los pasos en orden inverso.
    """

    def __init__(self, steps: list[CipherStep] = None):
        self.steps = steps or []

    def add(self, step: CipherStep):
        self.steps.append(step)

    def encrypt(self, text: str) -> tuple[str, list[str]]:
        """
        Cifra el texto aplicando todos los pasos en orden.
        Retorna (texto_final, [intermedios]) donde intermedios[i] es el
        resultado después del paso i.
        """
        current     = text
        intermedios = []
        for step in self.steps:
            current = step.encrypt(current)
            intermedios.append(current)
        return current, intermedios

    def decrypt(self, text: str) -> tuple[str, list[str]]:
        """
        Descifra el texto deshaciendo los pasos en orden inverso.
        Retorna (texto_final, [intermedios]).
        """
        current     = text
        intermedios = []
        for step in reversed(self.steps):
            current = step.decrypt(current)
            intermedios.append(current)
        return current, intermedios

    def describe(self) -> str:
        if not self.steps:
            return "(sin cifrados)"
        return " → ".join(s.describe() for s in self.steps)

    def __len__(self):
        return len(self.steps)