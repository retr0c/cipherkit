def apply(text):
    result = []
    for c in text:
        if c.isalpha():
            base = ord("A") if c.isupper() else ord("a")
            result.append(chr((ord(c) - base + 13) % 26 + base))
        else:
            result.append(c)
    return "".join(result)

encrypt = decrypt = apply