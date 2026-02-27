#!/usr/bin/env python3
"""
CipherKit — Interactive hacker toolkit
Run with: python main.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.display import banner, ok, err, info, title, ask, menu
from ciphers import caesar, vigenere, rot13, atbash
from tools import passwords, fakegen, stego, netinfo

# ─────────────────────────────────────────────────────────────
# CIPHER MENU
# ─────────────────────────────────────────────────────────────

def menu_ciphers():
    while True:
        title("CIFRADOS")
        choice = menu([
            "Caesar cipher",
            "Vigenère cipher",
            "ROT13",
            "Atbash",
            "← Volver",
        ])
        if choice == "1":   do_caesar()
        elif choice == "2": do_vigenere()
        elif choice == "3": do_rot13()
        elif choice == "4": do_atbash()
        elif choice == "5": break
        else:               err("Opción no válida")

def do_caesar():
    title("CAESAR CIPHER")
    info("Desplaza cada letra del alfabeto N posiciones.")
    action = menu(["Cifrar", "Descifrar", "Romper (brute force)"])
    if action == "3":
        text = ask("Texto cifrado")
        results = caesar.brute_force(text)
        title("RESULTADOS — TODOS LOS DESPLAZAMIENTOS")
        for k, r in results:
            print(f"  \033[93m[{k:>2}]\033[0m  {r}")
        print()
        return
    text = ask("Texto")
    try:
        key = int(ask("Clave numérica (ej: 13)"))
    except ValueError:
        err("La clave debe ser un número"); return
    result = caesar.encrypt(text, key) if action == "1" else caesar.decrypt(text, key)
    ok("Resultado", result)

def do_vigenere():
    title("VIGENÈRE CIPHER")
    info("Usa una palabra clave para cifrar cada letra de forma diferente.")
    action = menu(["Cifrar", "Descifrar"])
    text   = ask("Texto")
    key    = ask("Palabra clave (solo letras, ej: SECRET)")
    if not key.isalpha():
        err("La clave debe contener solo letras"); return
    result = vigenere.encrypt(text, key) if action == "1" else vigenere.decrypt(text, key)
    ok("Resultado", result)

def do_rot13():
    title("ROT13")
    info("Desplazamiento fijo de 13. Aplicarlo dos veces devuelve el original.")
    text = ask("Texto")
    ok("Resultado", rot13.apply(text))

def do_atbash():
    title("ATBASH")
    info("Espejo del alfabeto: A↔Z, B↔Y, C↔X ...")
    text = ask("Texto")
    ok("Resultado", atbash.apply(text))


# ─────────────────────────────────────────────────────────────
# PASSWORDS MENU
# ─────────────────────────────────────────────────────────────

def menu_passwords():
    title("GENERADOR DE CONTRASEÑAS")
    info("Genera contraseñas criptográficamente seguras.")
    print()

    try:
        length = int(ask("Longitud (recomendado: 16-32)"))
    except ValueError:
        length = 16

    sym_choice = menu(["Sí, incluir símbolos (!@#$...)", "No, solo letras y números"])
    use_symbols = sym_choice == "1"

    amb_choice = menu(["Sí, evitar caracteres ambiguos (l, I, 1, O, 0...)", "No, usar todos los caracteres"])
    no_ambiguous = amb_choice == "1"

    how_many = 1
    try:
        how_many = int(ask("¿Cuántas contraseñas generar? (1-10)"))
        how_many = max(1, min(10, how_many))
    except ValueError:
        pass

    title("CONTRASEÑAS GENERADAS")
    for i in range(how_many):
        pwd = passwords.generate(length, use_symbols, no_ambiguous)
        strength = passwords.strength(pwd)
        print(f"  \033[96m{pwd}\033[0m  \033[2m← {strength}\033[0m")
    print()


# ─────────────────────────────────────────────────────────────
# FAKE DATA MENU
# ─────────────────────────────────────────────────────────────

def menu_fakegen():
    while True:
        title("GENERADOR DE DATOS FALSOS")
        info("Útil para testing, formularios de prueba y desarrollo.")
        print()
        choice = menu([
            "Identidad completa (nombre + email + IP + MAC)",
            "Tarjeta de crédito FAKE (solo para testing)",
            "IP aleatoria",
            "Dominio falso",
            "User-Agent aleatorio",
            "← Volver",
        ])

        if choice == "1":
            name  = fakegen.fake_name()
            email = fakegen.fake_email(name)
            ip    = fakegen.fake_ip()
            mac   = fakegen.fake_mac()
            title("IDENTIDAD GENERADA")
            ok("Nombre", name)
            ok("Email",  email)
            ok("IP",     ip)
            ok("MAC",    mac)

        elif choice == "2":
            card = fakegen.fake_card()
            title("TARJETA FAKE — SOLO PARA TESTING")
            info("⚠  Estos datos son completamente ficticios.")
            info("⚠  Nunca uses esto para fraude. Es ilegal.")
            print()
            ok("Número",     card["number"])
            ok("Vencimiento", card["expiry"])
            ok("CVV",        card["cvv"])
            ok("Tipo",       card["type"])

        elif choice == "3":
            ok("IP", fakegen.fake_ip())

        elif choice == "4":
            ok("Dominio", fakegen.fake_domain())

        elif choice == "5":
            ok("User-Agent", fakegen.fake_user_agent())

        elif choice == "6":
            break
        else:
            err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# STEGANOGRAPHY MENU
# ─────────────────────────────────────────────────────────────

def menu_stego():
    while True:
        title("ESTEGANOGRAFÍA")
        info("Oculta mensajes secretos dentro de texto normal usando")
        info("caracteres Unicode invisibles. El texto parece igual a simple vista.")
        print()
        choice = menu([
            "Ocultar mensaje en texto",
            "Revelar mensaje oculto",
            "Comprobar si un texto tiene mensaje oculto",
            "← Volver",
        ])

        if choice == "1":
            cover  = ask("Texto portador (el texto 'inocente')")
            secret = ask("Mensaje secreto a ocultar")
            result = stego.hide(cover, secret)
            title("TEXTO CON MENSAJE OCULTO")
            info("Copia el siguiente texto. Parece normal pero contiene tu mensaje:")
            print(f"\n  {result}\n")
            info("Para revelar el mensaje, usa la opción 2.")

        elif choice == "2":
            text   = ask("Pega el texto con mensaje oculto")
            secret = stego.reveal(text)
            if secret:
                ok("Mensaje oculto encontrado", secret)
            else:
                err("No se encontró ningún mensaje oculto.")

        elif choice == "3":
            text = ask("Texto a analizar")
            if stego.has_hidden(text):
                ok("Estado", "⚠  Este texto CONTIENE un mensaje oculto")
            else:
                ok("Estado", "✓  Sin mensajes ocultos detectados")

        elif choice == "4":
            break
        else:
            err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# NET INFO MENU
# ─────────────────────────────────────────────────────────────

def menu_netinfo():
    while True:
        title("INFO IP / RED")
        choice = menu([
            "Mi IP pública",
            "Geolocalizar una IP",
            "DNS lookup (dominio → IP)",
            "Reverse DNS (IP → dominio)",
            "Ping a un host",
            "← Volver",
        ])

        if choice == "1":
            info("Consultando...")
            ok("Tu IP pública", netinfo.my_ip())

        elif choice == "2":
            ip   = ask("IP a geolocalizar")
            info("Consultando...")
            data = netinfo.geolocate(ip)
            title(f"GEOLOCALIZACIÓN — {ip}")
            for k, v in data.items():
                ok(k, str(v))

        elif choice == "3":
            domain = ask("Dominio (ej: google.com)")
            info("Resolviendo...")
            ok("IP", netinfo.dns_lookup(domain))

        elif choice == "4":
            ip = ask("IP")
            info("Buscando...")
            ok("Hostname", netinfo.reverse_dns(ip))

        elif choice == "5":
            host  = ask("Host o IP")
            try:
                count = int(ask("Número de pings (1-10)"))
                count = max(1, min(10, count))
            except ValueError:
                count = 4
            info("Haciendo ping...")
            print(netinfo.ping(host, count))

        elif choice == "6":
            break
        else:
            err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────

def main():
    banner()
    while True:
        title("MENÚ PRINCIPAL")
        choice = menu([
            "🔐  Cifrados          (Caesar, Vigenère, ROT13, Atbash)",
            "🔑  Contraseñas       (generar contraseñas seguras)",
            "🎲  Datos falsos      (identidades, IPs, tarjetas fake)",
            "🕵️   Esteganografía   (ocultar mensajes en texto)",
            "🌐  Info IP / Red     (geolocalizar, DNS, ping)",
            "❌  Salir",
        ])

        if choice == "1":   menu_ciphers()
        elif choice == "2": menu_passwords()
        elif choice == "3": menu_fakegen()
        elif choice == "4": menu_stego()
        elif choice == "5": menu_netinfo()
        elif choice == "6":
            print(f"\n  \033[2mHasta luego.\033[0m\n")
            sys.exit(0)
        else:
            err("Opción no válida — escribe el número")


if __name__ == "__main__":
    main()