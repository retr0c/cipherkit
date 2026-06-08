#!/usr/bin/env python3
"""
CipherKit v2 — Interactive hacker toolkit
Run with: python main.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from utils.display  import (banner, ok, err, info, warn, title, ask, menu,
                             confirm, paginate, table, ProgressBar)
from utils.validators import (validate_text, validate_alpha_key, validate_int_key,
                               validate_host, validate_ip, validate_domain,
                               validate_password_length, validate_count,
                               validate_box_size, validate_box_sep)
from ciphers import caesar, vigenere, rot13, atbash, box_caesar
from ciphers.chain import CipherChain, CipherStep, CIPHER_IDS
from tools import passwords, fakegen, stego, netinfo
from tools.analyzer import full_report, suggest_ciphers
from tools.brute_chain import crack, estimate_combinations, CIPHER_DISPLAY_NAMES


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _ask_text(prompt: str = "Texto") -> str | None:
    text = ask(prompt)
    ok_v, msg = validate_text(text, prompt)
    if not ok_v:
        err(msg)
        return None
    return text


def _ask_int(prompt: str, min_v: int, max_v: int) -> int | None:
    raw = ask(prompt)
    ok_v, msg, val = validate_int_key(raw, prompt, min_v, max_v)
    if not ok_v:
        err(msg)
        return None
    return val


# ─────────────────────────────────────────────────────────────
# CIFRADOS — MENÚ
# ─────────────────────────────────────────────────────────────

def menu_ciphers():
    while True:
        title("CIFRADOS")
        choice = menu([
            "Caesar cipher",
            "Vigenère cipher",
            "ROT13",
            "Atbash",
            "Caja Caesar",
            "← Volver",
        ])
        if   choice == "1": do_caesar()
        elif choice == "2": do_vigenere()
        elif choice == "3": do_rot13()
        elif choice == "4": do_atbash()
        elif choice == "5": do_box_caesar()
        elif choice == "6": break
        else: err("Opción no válida")


def do_caesar():
    title("CAESAR CIPHER")
    info("Desplaza cada letra del alfabeto N posiciones.")
    action = menu(["Cifrar", "Descifrar", "Romper (brute force)"])
    if action == "3":
        text = _ask_text("Texto cifrado")
        if not text: return
        results = caesar.brute_force(text)
        title("RESULTADOS — TODOS LOS DESPLAZAMIENTOS")
        def fmt(item):
            k, r, s = item
            return f"[{k:>2}] score={s:.3f}  {r[:80]}"
        paginate(results, page_size=10, formatter=fmt)
        return
    text = _ask_text("Texto")
    if not text: return
    raw_key = ask("Clave numérica (1–25)")
    ok_v, msg, key = validate_int_key(raw_key, "Clave", 1, 25)
    if not ok_v: err(msg); return
    result = caesar.encrypt(text, key) if action == "1" else caesar.decrypt(text, key)
    ok("Resultado", result)


def do_vigenere():
    title("VIGENÈRE CIPHER")
    info("Usa una palabra clave para cifrar cada letra de forma diferente.")
    action = menu(["Cifrar", "Descifrar"])
    text = _ask_text("Texto")
    if not text: return
    key  = ask("Palabra clave (solo letras)")
    ok_v, msg = validate_alpha_key(key, "Clave")
    if not ok_v: err(msg); return
    result = vigenere.encrypt(text, key) if action == "1" else vigenere.decrypt(text, key)
    ok("Resultado", result)


def do_rot13():
    title("ROT13")
    info("Desplazamiento fijo de 13. Aplicarlo dos veces devuelve el original.")
    text = _ask_text("Texto")
    if not text: return
    ok("Resultado", rot13.apply(text))


def do_atbash():
    title("ATBASH")
    info("Espejo del alfabeto: A↔Z, B↔Y, C↔X ...")
    text = _ask_text("Texto")
    if not text: return
    ok("Resultado", atbash.apply(text))


def do_box_caesar():
    title("CAJA CAESAR")
    info("Divide el texto por un separador y aplica Caesar a cada segmento.")
    info("Parámetros: separador, tamaño de caja (0=sin límite), clave numérica.")

    action = menu(["Cifrar", "Descifrar", "Romper (brute force)"])

    sep_raw = ask("Separador (carácter, ej: .)")
    ok_v, msg = validate_box_sep(sep_raw)
    if not ok_v: err(msg); return
    sep = sep_raw

    if action == "3":
        text = _ask_text("Texto cifrado")
        if not text: return
        info("Probando todas las combinaciones de clave y tamaño de caja...")
        results = box_caesar.brute_force_full(text, sep)
        title("TOP RESULTADOS — CAJA CAESAR BRUTE FORCE")
        def fmt(item):
            k, bs, r, s = item
            return f"key={k:>2} caja={bs:>2} score={s:.3f}  {r[:70]}"
        paginate(results[:50], page_size=10, formatter=fmt)
        return

    bs_raw = ask("Tamaño de caja en letras (0 = sin subdivisión)")
    ok_v, msg, box_size = validate_box_size(bs_raw)
    if not ok_v: err(msg); return

    text = _ask_text("Texto")
    if not text: return
    raw_key = ask("Clave numérica (1–25)")
    ok_v, msg, key = validate_int_key(raw_key, "Clave", 1, 25)
    if not ok_v: err(msg); return

    if action == "1":
        result = box_caesar.encrypt(text, key, sep, box_size)
    else:
        result = box_caesar.decrypt(text, key, sep, box_size)
    ok("Resultado", result)


# ─────────────────────────────────────────────────────────────
# ANALIZADOR
# ─────────────────────────────────────────────────────────────

def menu_analyzer():
    title("ANALIZADOR DE TEXTO CIFRADO")
    info("Analiza un texto cifrado y sugiere qué cifrados podrían haberse usado.")
    text = _ask_text("Texto cifrado a analizar")
    if not text: return

    report = full_report(text)
    title("REPORTE DE ANÁLISIS")
    ok("Longitud total",    str(report["longitud_total"]))
    ok("Total letras",      str(report["total_letras"]))
    ok("Índice coincidenc", str(report["ic"]))
    ok("Idioma probable",   report["idioma_probable"])
    ok("Score legibilidad", str(report["score_legib"]))

    top5 = report["top5_letras"]
    info(f"\n  Top 5 letras: " + "  ".join(f"{c.upper()}={v:.3f}" for c, v in top5))

    title("CIFRADOS SUGERIDOS")
    for cipher, reason in report["sugerencias"]:
        info(f"  → {CIPHER_DISPLAY_NAMES.get(cipher, cipher)}: {reason}")
    print()


# ─────────────────────────────────────────────────────────────
# DESCIFRADO POR FUERZA BRUTA INTELIGENTE
# ─────────────────────────────────────────────────────────────

def menu_brute_chain():
    title("DESCIFRADO AUTOMÁTICO — FUERZA BRUTA INTELIGENTE")
    info("Selecciona los cifrados que SE USARON (no importa el orden ni las claves).")
    info("El programa prueba todas las combinaciones posibles y muestra los mejores resultados.")
    print()

    # Selección de cifrados
    cipher_options = list(CIPHER_DISPLAY_NAMES.items())
    while True:
        title("SELECCIONA LOS CIFRADOS USADOS")
        for i, (cid, name) in enumerate(cipher_options, 1):
            print(f"  [{ i}]  {name}")
        print()
        raw = ask("Ingresa los números separados por coma (ej: 1,3,4)")
        selected = []
        error    = False
        for part in raw.split(","):
            part = part.strip()
            ok_v, msg, idx = validate_int_key(part, "Opción", 1, len(cipher_options))
            if not ok_v:
                err(f"'{part}' no es válido — {msg}")
                error = True
                break
            selected.append(cipher_options[idx - 1][0])
        if error:
            continue
        if not selected:
            err("Debes seleccionar al menos un cifrado.")
            continue
        break

    title("CIFRADOS SELECCIONADOS")
    for cid in selected:
        info(f"  ✔ {CIPHER_DISPLAY_NAMES[cid]}")
    print()

    # Texto a descifrar
    text = _ask_text("Texto cifrado")
    if not text: return

    # Estimación
    est = estimate_combinations(selected)
    info(f"Combinaciones estimadas: {est:,}")
    if est > 5_000_000:
        warn(f"Son {est:,} combinaciones — puede tardar varios minutos.")
        if not confirm("¿Continuar de todas formas?"):
            return

    # Ejecutar con barra de progreso
    title("EJECUTANDO BRUTE FORCE")
    est = estimate_combinations(selected)
    bar = ProgressBar(total=est, label="Probando combinaciones")

    def progress(current, total):
        bar.update(min(current, est))

    try:
        results = crack(text, selected)
    except KeyboardInterrupt:
        bar.abort("Interrumpido por el usuario")
        return

    bar.done(f"{len(results)} candidatos encontrados")

    if not results:
        err("No se encontraron resultados con score suficiente.")
        info("Sugerencia: prueba añadir o quitar algún cifrado de la selección.")
        return

    # Mostrar resultados
    title(f"TOP {len(results)} RESULTADOS")

    def fmt_result(item):
        # Extraemos la secuencia de métodos
        methods = " → ".join(item.get("sequence", ["Desconocido"]))
        # Extraemos las llaves asociadas
        keys_list = item.get("keys", [])
        keys = " → ".join(str(k) for k in keys_list) if isinstance(keys_list, list) else str(keys_list)
        
        score = item.get("score", 0.0)
        texto = item.get("text", "")

        return f"Score: {score:.2f} | Cadena: {methods} (Llaves: {keys})\n    Texto: {texto}"

    # Asegurar que resultados estén ordenados por score antes de mostrar
    results = sorted(results, key=lambda x: x.get("score", 0), reverse=True)
    # Ahora sí, el paginador
    paginate(results, page_size=5, formatter=fmt_result)
# ─────────────────────────────────────────────────────────────
# CONTRASEÑAS
# ─────────────────────────────────────────────────────────────

def menu_passwords():
    while True:
        title("CONTRASEÑAS")
        choice = menu([
            "Generar contraseña segura",
            "Generar passphrase (palabras)",
            "Evaluar una contraseña",
            "← Volver",
        ])

        if choice == "1":
            title("GENERADOR DE CONTRASEÑAS")
            raw_len = ask("Longitud (recomendado: 16-32)")
            ok_v, msg, length = validate_password_length(raw_len)
            if not ok_v: err(msg); continue

            sym = menu(["Sí, incluir símbolos (!@#$…)", "No, solo letras y números"]) == "1"
            amb = menu(["Sí, evitar ambiguos (l,I,1,O,0…)", "No, usar todos"]) == "1"

            raw_n = ask("¿Cuántas contraseñas? (1-10)")
            ok_v, msg, n = validate_count(raw_n)
            if not ok_v: n = 1

            title("CONTRASEÑAS GENERADAS")
            for _ in range(n):
                pwd = passwords.generate(length, sym, amb)
                det = passwords.strength_detail(pwd)
                print(f"  \033[96m{pwd}\033[0m  ← {det['nivel']} ({det['entropia_bits']} bits)")
            print()

        elif choice == "2":
            title("GENERADOR DE PASSPHRASES")
            raw_n = ask("Número de palabras (3-8)")
            ok_v, msg, n = validate_int_key(raw_n, "Palabras", 3, 8)
            if not ok_v: err(msg); continue
            sep = ask("Separador (ej: - o espacio o .)")
            if not sep: sep = "-"
            phrase = passwords.generate_passphrase(n, sep)
            det    = passwords.strength_detail(phrase)
            ok("Passphrase", phrase)
            ok("Fortaleza",  f"{det['nivel']} ({det['entropia_bits']} bits)")

        elif choice == "3":
            title("EVALUAR CONTRASEÑA")
            pwd = ask("Contraseña a evaluar")
            if not pwd: err("Texto vacío"); continue
            det = passwords.strength_detail(pwd)
            ok("Nivel",   det["nivel"])
            ok("Entropía", f"{det['entropia_bits']} bits")
            print()
            info("Criterios:")
            for check, passed in det["checks"].items():
                icon = "\033[92m✔\033[0m" if passed else "\033[91m✘\033[0m"
                print(f"    {icon}  {check.replace('_', ' ')}")
            print()

        elif choice == "4":
            break
        else:
            err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# DATOS FALSOS
# ─────────────────────────────────────────────────────────────

def menu_fakegen():
    while True:
        title("GENERADOR DE DATOS FALSOS")
        choice = menu([
            "Identidad completa",
            "Tarjeta de crédito FAKE (solo testing)",
            "IP aleatoria",
            "Dominio falso",
            "User-Agent aleatorio",
            "UUID",
            "Cédula colombiana ficticia",
            "Celular colombiano ficticio",
            "Coordenadas (Colombia)",
            "← Volver",
        ])

        if choice == "1":
            name  = fakegen.fake_name()
            title("IDENTIDAD GENERADA")
            ok("Nombre",  name)
            ok("Email",   fakegen.fake_email(name))
            ok("IP",      fakegen.fake_ip())
            ok("MAC",     fakegen.fake_mac())
            ok("UUID",    fakegen.fake_uuid())
            ok("Cédula",  fakegen.fake_cedula_colombia())
            ok("Celular", fakegen.fake_phone_colombia())

        elif choice == "2":
            card = fakegen.fake_card()
            title("TARJETA FAKE — SOLO TESTING")
            warn("Datos completamente ficticios. Nunca usar para fraude.")
            ok("Número",      card["number"])
            ok("Vencimiento", card["expiry"])
            ok("CVV",         card["cvv"])
            ok("Tipo",        card["type"])

        elif choice == "3":  ok("IP",      fakegen.fake_ip())
        elif choice == "4":  ok("Dominio", fakegen.fake_domain())
        elif choice == "5":  ok("UA",      fakegen.fake_user_agent())
        elif choice == "6":  ok("UUID",    fakegen.fake_uuid())
        elif choice == "7":  ok("Cédula",  fakegen.fake_cedula_colombia())
        elif choice == "8":  ok("Celular", fakegen.fake_phone_colombia())
        elif choice == "9":
            coords = fakegen.fake_coordinates()
            ok("Latitud",  str(coords["lat"]))
            ok("Longitud", str(coords["lon"]))

        elif choice == "10": break
        else: err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# ESTEGANOGRAFÍA
# ─────────────────────────────────────────────────────────────

def menu_stego():
    while True:
        title("ESTEGANOGRAFÍA")
        info("Oculta mensajes en texto usando caracteres Unicode invisibles.")
        print()
        choice = menu([
            "Ocultar mensaje en texto",
            "Revelar mensaje oculto",
            "Analizar texto sospechoso",
            "← Volver",
        ])

        if choice == "1":
            cover  = _ask_text("Texto portador (el texto 'inocente')")
            if not cover: continue
            secret = _ask_text("Mensaje secreto a ocultar")
            if not secret: continue
            result = stego.hide(cover, secret)
            title("TEXTO CON MENSAJE OCULTO")
            info("Copia el siguiente texto — parece normal pero contiene tu mensaje:")
            print(f"\n  {result}\n")

        elif choice == "2":
            text   = _ask_text("Pega el texto con mensaje oculto")
            if not text: continue
            secret = stego.reveal(text)
            if secret:
                ok("Mensaje oculto encontrado", secret)
            else:
                err("No se encontró ningún mensaje oculto (formato CipherKit).")

        elif choice == "3":
            text = _ask_text("Texto a analizar")
            if not text: continue
            report = stego.analyze(text)
            title("ANÁLISIS DE CARACTERES INVISIBLES")
            ok("Mensaje propio (CipherKit)", "SÍ" if report["tiene_mensaje_propio"] else "NO")
            ok("Zero-width space  (U+200B)", str(report["zero_width_space_u200b"]))
            ok("Zero-width ZWNJ   (U+200C)", str(report["zero_width_nonjoin_u200c"]))
            ok("Zero-width joiner (U+200D)", str(report["zero_width_joiner_u200d"]))
            ok("Word joiner       (U+2060)", str(report["word_joiner_u2060"]))
            ok("Total invisibles",           str(report["total_invisibles"]))
            if report["sospechoso"]:
                warn("El texto contiene caracteres invisibles de formato desconocido.")

        elif choice == "4": break
        else: err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# RED / IP
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
            "Escaneo de puertos básico",
            "WHOIS de dominio",
            "← Volver",
        ])

        if choice == "1":
            info("Consultando...")
            ok("Tu IP pública", netinfo.my_ip())

        elif choice == "2":
            ip = ask("IP a geolocalizar")
            ok_v, msg = validate_ip(ip)
            if not ok_v: err(msg); continue
            info("Consultando...")
            data = netinfo.geolocate(ip)
            title(f"GEOLOCALIZACIÓN — {ip}")
            for k, v in data.items():
                ok(k, str(v))

        elif choice == "3":
            domain = ask("Dominio (ej: google.com)")
            ok_v, msg = validate_domain(domain)
            if not ok_v: err(msg); continue
            info("Resolviendo...")
            ips = netinfo.dns_lookup_all(domain)
            title(f"DNS — {domain}")
            for ip in ips:
                ok("IP", ip)

        elif choice == "4":
            ip = ask("IP")
            ok_v, msg = validate_ip(ip)
            if not ok_v: err(msg); continue
            info("Buscando...")
            ok("Hostname", netinfo.reverse_dns(ip))

        elif choice == "5":
            host = ask("Host o IP")
            ok_v, msg = validate_host(host)
            if not ok_v: err(msg); continue
            raw_n = ask("Número de pings (1–10)")
            ok_v2, msg2, count = validate_int_key(raw_n, "Pings", 1, 10)
            if not ok_v2: count = 4
            info("Haciendo ping...")
            print(netinfo.ping(host, count))

        elif choice == "6":
            host = ask("Host o IP a escanear")
            ok_v, msg = validate_host(host)
            if not ok_v: err(msg); continue
            warn("Solo usar en sistemas propios o con permiso explícito.")
            if not confirm("¿Continuar?"):
                continue
            info("Escaneando puertos comunes...")
            bar = ProgressBar(total=len(netinfo._COMMON_PORTS), label="Escaneando")
            results_scan = []
            for i, port in enumerate(netinfo._COMMON_PORTS.keys(), 1):
                bar.update(i)
                r = netinfo.port_scan(host, [port], timeout=0.5)
                results_scan.extend(r)
            bar.done()
            open_ports = [r for r in results_scan if r.get("estado") == "ABIERTO" and "error" not in r]
            if open_ports:
                title("PUERTOS ABIERTOS")
                table(
                    [(p["port"], p["servicio"], p["estado"]) for p in open_ports],
                    headers=["Puerto", "Servicio", "Estado"]
                )
            else:
                info("No se encontraron puertos abiertos entre los comunes.")
            print()

        elif choice == "7":
            domain = ask("Dominio (ej: google.com)")
            ok_v, msg = validate_domain(domain)
            if not ok_v: err(msg); continue
            info("Consultando WHOIS...")
            result = netinfo.whois(domain)
            title(f"WHOIS — {domain}")
            print(result)
            print()

        elif choice == "8": break
        else: err("Opción no válida")


# ─────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────

def main():
    banner()
    while True:
        title("MENÚ PRINCIPAL")
        choice = menu([
            "🔐  Cifrados          (Caesar, Vigenère, ROT13, Atbash, Caja Caesar)",
            "🔍  Analizador        (analizar texto cifrado desconocido)",
            "🤖  Descifrado auto   (fuerza bruta inteligente multicifrado)",
            "🔑  Contraseñas       (generar y evaluar contraseñas seguras)",
            "🎲  Datos falsos      (identidades, IPs, tarjetas, cédulas)",
            "🕵️   Esteganografía   (ocultar mensajes en texto)",
            "🌐  Info IP / Red     (geolocalizar, DNS, ping, ports, whois)",
            "❌  Salir",
        ])

        if   choice == "1": menu_ciphers()
        elif choice == "2": menu_analyzer()
        elif choice == "3": menu_brute_chain()
        elif choice == "4": menu_passwords()
        elif choice == "5": menu_fakegen()
        elif choice == "6": menu_stego()
        elif choice == "7": menu_netinfo()
        elif choice == "8":
            print(f"\n  \033[2mHasta luego.\033[0m\n")
            sys.exit(0)
        else:
            err("Opción no válida — escribe el número")


if __name__ == "__main__":
    main()