# 🔐 CipherKit

> Hacker-style interactive toolkit — ciphers, passwords, steganography & net info
```
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ██╗  ██╗██╗████████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██║ ██╔╝██║╚══██╔══╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝█████╔╝ ██║   ██║
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██╔═██╗ ██║   ██║
╚██████╗██║██║     ██║  ██║███████╗██║  ██║██║  ██╗██║   ██║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝
```

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen?style=flat-square)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey?style=flat-square)

---

## What is this?

CipherKit is a terminal-based hacker toolkit with an interactive step-by-step menu. No commands to memorize — just run it and follow the prompts.

**Zero external dependencies.** Everything uses Python's standard library.

---

## Features

### 🔐 Ciphers
Encrypt and decrypt messages using classical cryptography methods.

| Cipher | Description |
|--------|-------------|
| **Caesar** | Shifts each letter by a numeric key. Includes brute-force crack mode (tries all 25 keys). |
| **Vigenère** | Uses a keyword to apply a different shift to each letter — much harder to crack than Caesar. |
| **ROT13** | Fixed shift of 13 positions. Self-reversing: apply it twice to get the original back. |
| **Atbash** | Mirrors the alphabet: A↔Z, B↔Y, C↔X. Ancient Hebrew cipher, also self-reversing. |

### 🔑 Password Generator
Generates cryptographically secure passwords using Python's `SystemRandom`.
- Choose length, whether to include symbols, and whether to exclude ambiguous characters (`l`, `I`, `1`, `O`, `0`...)
- Generate up to 10 passwords at once
- Each password is rated: Weak / Medium / Good / Strong / Very Strong

### 🎲 Fake Data Generator
Generates realistic fake data for development, testing, and form filling.
- **Full identity** — name, email, IP address, MAC address
- **Fake credit card** — Luhn-valid Visa number, expiry, CVV *(for testing only — never for fraud)*
- **Random IP, domain, User-Agent**

### 🕵️ Steganography
Hides secret messages inside innocent-looking text using invisible Unicode zero-width characters. The carrier text looks completely normal to the naked eye.
- Hide a secret message inside any text
- Reveal hidden messages from suspicious text
- Detect whether a text contains a hidden message

### 🌐 Net Info
Network reconnaissance tools using only Python's standard library.
- **My public IP** — fetches your current external IP
- **Geolocate an IP** — city, region, country, ISP, timezone
- **DNS lookup** — resolve a domain to its IP address
- **Reverse DNS** — find the hostname behind an IP
- **Ping** — send ICMP packets to any host

---

## Installation & Usage

**Requirements:** Python 3.10 or higher. No pip install needed.
```bash
git clone https://github.com/YOUR_USERNAME/cipherkit.git
cd cipherkit
python main.py
```

Then just follow the interactive menu.

---

## Project Structure
```
cipherkit/
├── main.py              # Interactive menu entry point
├── ciphers/
│   ├── caesar.py        # Caesar cipher + brute-force
│   ├── vigenere.py      # Vigenère cipher
│   ├── rot13.py         # ROT13
│   └── atbash.py        # Atbash mirror cipher
├── tools/
│   ├── passwords.py     # Secure password generator
│   ├── fakegen.py       # Fake data generator
│   ├── stego.py         # Unicode steganography
│   └── netinfo.py       # IP/network info tools
└── utils/
    └── display.py       # Terminal colors and menus
```

---

## ⚠️ Legal Notice

This tool is intended for **educational purposes and legitimate use only.**
- Fake data generation is for software testing only
- Steganography is for learning and privacy research
- Network tools only on systems you own or have permission to test

---

## License

MIT — free to use, modify, and share.