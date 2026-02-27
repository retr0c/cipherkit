import urllib.request
import urllib.error
import json
import socket
import subprocess
import platform

def my_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as r:
            return json.loads(r.read())["ip"]
    except Exception:
        return "Could not reach API"

def geolocate(ip):
    try:
        url = f"https://ipapi.co/{ip}/json/"
        req = urllib.request.Request(url, headers={"User-Agent": "cipherkit/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        return {
            "IP":       data.get("ip", "?"),
            "City":     data.get("city", "?"),
            "Region":   data.get("region", "?"),
            "Country":  data.get("country_name", "?"),
            "ISP":      data.get("org", "?"),
            "Timezone": data.get("timezone", "?"),
        }
    except Exception as e:
        return {"Error": str(e)}

def dns_lookup(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        return f"Error: {e}"

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "No reverse DNS found"

def ping(host, count=4):
    flag = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", flag, str(count), host],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout or result.stderr
    except FileNotFoundError:
        return "ping not available"
    except subprocess.TimeoutExpired:
        return "Ping timed out"