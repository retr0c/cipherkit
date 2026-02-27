import random

FIRST = ["Alex","Jordan","Morgan","Taylor","Casey","Riley","Avery","Quinn","Drew","Sam",
         "Blake","Reese","Skyler","Dakota","Peyton","Rowan","Emery","Finley","Harley","Logan"]
LAST  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Wilson",
         "Moore","Anderson","Thomas","Jackson","White","Harris","Martin","Thompson","Lee"]
DOMAINS = ["gmail.com","yahoo.com","outlook.com","protonmail.com","hotmail.com","icloud.com"]
TLDS    = ["com","net","org","io","dev","app","co"]

def fake_name():
    return f"{random.choice(FIRST)} {random.choice(LAST)}"

def fake_email(name=None):
    name = name or fake_name()
    first, last = name.lower().split()
    sep = random.choice([".", "_", ""])
    num = str(random.randint(1, 999)) if random.random() > 0.5 else ""
    return f"{first}{sep}{last}{num}@{random.choice(DOMAINS)}"

def fake_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def fake_mac():
    return ":".join(f"{random.randint(0,255):02X}" for _ in range(6))

def fake_card():
    # Luhn-valid fake Visa (for testing ONLY — not real)
    def luhn(n):
        digits = [int(d) for d in str(n)]
        for i in range(len(digits)-2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        check = (10 - sum(digits) % 10) % 10
        return str(n) + str(check)
    prefix = "4" + "".join(str(random.randint(0,9)) for _ in range(14))
    number = luhn(prefix[:15])
    exp_m  = str(random.randint(1,12)).zfill(2)
    exp_y  = str(random.randint(26,30))
    cvv    = str(random.randint(100,999))
    return {"number": number, "expiry": f"{exp_m}/{exp_y}", "cvv": cvv, "type": "Visa (FAKE)"}

def fake_domain():
    words = ["dark","cyber","ghost","void","proxy","null","shadow","byte","hex","core"]
    return f"{random.choice(words)}{random.choice(words)}.{random.choice(TLDS)}"

def fake_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    ]
    return random.choice(agents)