"""
tools/netinfo.py — Herramientas de red.
Fix: sanitización de host antes de subprocess.
Nuevo: port scanner básico, whois.
"""

import urllib.request
import urllib.error
import json
import socket
import subprocess
import platform
from utils.validators import validate_host


# ─────────────────────────────────────────────────────────────
# IP PÚBLICA
# ─────────────────────────────────────────────────────────────

def my_ip() -> str:
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as r:
            return json.loads(r.read())["ip"]
    except Exception as e:
        return f"Error: {e}"


# ─────────────────────────────────────────────────────────────
# GEOLOCALIZACIÓN
# ─────────────────────────────────────────────────────────────

def geolocate(ip: str) -> dict:
    try:
        url = f"https://ipapi.co/{ip}/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "cipherkit/2.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        if data.get("error"):
            return {"Error": data.get("reason", "IP inválida o reservada")}
        return {
            "IP":        data.get("ip", "?"),
            "Ciudad":    data.get("city", "?"),
            "Region":    data.get("region", "?"),
            "País":      data.get("country_name", "?"),
            "ISP":       data.get("org", "?"),
            "Timezone":  data.get("timezone", "?"),
            "Latitud":   data.get("latitude", "?"),
            "Longitud":  data.get("longitude", "?"),
        }
    except Exception as e:
        return {"Error": str(e)}


# ─────────────────────────────────────────────────────────────
# DNS
# ─────────────────────────────────────────────────────────────

def dns_lookup(domain: str) -> str:
    try:
        return socket.gethostbyname(domain.strip())
    except socket.gaierror as e:
        return f"Error: {e}"


def dns_lookup_all(domain: str) -> list[str]:
    """Retorna todas las IPs asociadas al dominio."""
    try:
        results = socket.getaddrinfo(domain.strip(), None)
        return list(dict.fromkeys(r[4][0] for r in results))
    except socket.gaierror as e:
        return [f"Error: {e}"]


def reverse_dns(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip.strip())[0]
    except Exception:
        return "Sin reverse DNS"


# ─────────────────────────────────────────────────────────────
# PING — con sanitización anti-inyección
# ─────────────────────────────────────────────────────────────

def ping(host: str, count: int = 4) -> str:
    ok, msg = validate_host(host)
    if not ok:
        return f"Error: {msg}"

    count = max(1, min(count, 10))
    flag  = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", flag, str(count), host],
            capture_output=True, text=True, timeout=20
        )
        return result.stdout or result.stderr or "Sin respuesta"
    except FileNotFoundError:
        return "ping no disponible en este sistema"
    except subprocess.TimeoutExpired:
        return "Ping agotó el tiempo de espera"


# ─────────────────────────────────────────────────────────────
# PORT SCANNER BÁSICO
# ─────────────────────────────────────────────────────────────

_COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 465: "SMTPS", 587: "SMTP/TLS",
    993: "IMAPS", 995: "POP3S", 3306: "MySQL",
    3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-alt", 8443: "HTTPS-alt", 27017: "MongoDB",
}

def port_scan(host: str, ports: list[int] = None, timeout: float = 1.0) -> list[dict]:
    """
    Escanea puertos en un host.
    Solo usar en sistemas propios o con permiso explícito.
    """
    ok, msg = validate_host(host)
    if not ok:
        return [{"error": msg}]

    target_ports = ports or list(_COMMON_PORTS.keys())
    results = []
    for port in target_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            status = sock.connect_ex((host, port))
            sock.close()
            if status == 0:
                results.append({
                    "port":    port,
                    "estado":  "ABIERTO",
                    "servicio": _COMMON_PORTS.get(port, "desconocido"),
                })
        except Exception:
            pass
    return results


# ─────────────────────────────────────────────────────────────
# WHOIS BÁSICO (sin dependencias)
# ─────────────────────────────────────────────────────────────

def whois(domain: str) -> str:
    """
    Consulta WHOIS básica usando conexión raw al servidor whois.
    """
    ok, msg = validate_host(domain)
    if not ok:
        return f"Error: {msg}"
    try:
        tld = domain.strip().split(".")[-1].lower()
        whois_server = f"whois.iana.org"
        # Intentar servidor específico por TLD
        tld_servers = {
            "com": "whois.verisign-grs.com",
            "net": "whois.verisign-grs.com",
            "org": "whois.pir.org",
            "co":  "whois.nic.co",
            "io":  "whois.nic.io",
        }
        whois_server = tld_servers.get(tld, "whois.iana.org")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((whois_server, 43))
        s.sendall((domain.strip() + "\r\n").encode())
        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
        s.close()
        text = response.decode("utf-8", errors="replace")
        # Retornar solo las primeras 30 líneas relevantes
        lines = [l for l in text.splitlines() if l.strip() and not l.startswith("%")][:30]
        return "\n".join(lines) if lines else "Sin datos WHOIS"
    except Exception as e:
        return f"Error WHOIS: {e}"