import random
import string

def generate(length=16, use_symbols=True, no_ambiguous=True):
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    if no_ambiguous:
        for ch in "lI1O0oB8S5Z2":
            chars = chars.replace(ch, "")
    return "".join(random.SystemRandom().choice(chars) for _ in range(length))

def strength(password):
    score = 0
    if len(password) >= 12:  score += 1
    if len(password) >= 20:  score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    labels = {0:"Very Weak", 1:"Weak", 2:"Weak", 3:"Medium", 4:"Good", 5:"Strong", 6:"Very Strong"}
    return labels[score]