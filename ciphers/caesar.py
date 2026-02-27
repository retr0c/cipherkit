def encrypt(text, key):
    key = key % 26
    result = []
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base + key) % 26 + base))
        else:
            result.append(c)
    return "".join(result)

def decrypt(text, key):
    return encrypt(text, -key)

def brute_force(text):
    return [(k, decrypt(text, k)) for k in range(1, 26)]