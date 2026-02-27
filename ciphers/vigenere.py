def _clean(key):
    return "".join(c for c in key.upper() if c.isalpha())

def encrypt(text, key):
    key = _clean(key)
    result, i = [], 0
    for c in text:
        if c.isalpha():
            shift = ord(key[i % len(key)]) - ord("A")
            base  = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base + shift) % 26 + base))
            i += 1
        else:
            result.append(c)
    return "".join(result)

def decrypt(text, key):
    key = _clean(key)
    result, i = [], 0
    for c in text:
        if c.isalpha():
            shift = ord(key[i % len(key)]) - ord("A")
            base  = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base - shift) % 26 + base))
            i += 1
        else:
            result.append(c)
    return "".join(result)