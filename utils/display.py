"""
display.py — Terminal UI para CipherKit
Colores, menús, barra de progreso, paginación.
"""

import sys
import time

GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
MAGENTA= "\033[95m"
DIM    = "\033[2m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BANNER = f"""{GREEN}{BOLD}
 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ ██╗  ██╗██╗████████╗
██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗██║ ██╔╝██║╚══██╔══╝
██║     ██║██████╔╝███████║█████╗  ██████╔╝█████╔╝ ██║   ██║
██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗██╔═██╗ ██║   ██║
╚██████╗██║██║     ██║  ██║███████╗██║  ██║██║  ██╗██║   ██║
 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝   ╚═╝
{RESET}{DIM}  Hacker toolkit — ciphers · passwords · steganography · net info{RESET}
"""

# ─────────────────────────────────────────────────────────────
# BÁSICOS
# ─────────────────────────────────────────────────────────────

def banner():       print(BANNER)
def ok(k, v=""):
    if v:
        print(f"\n  {GREEN}✔ {BOLD}{k}:{RESET}  {CYAN}{v}{RESET}\n")
    else:
        print(f"\n  {GREEN}✔ {BOLD}{k}{RESET}\n")
def err(msg):       print(f"\n  {RED}✘ {msg}{RESET}\n")
def info(msg):      print(f"  {DIM}{msg}{RESET}")
def warn(msg):      print(f"\n  {YELLOW}⚠  {msg}{RESET}\n")
def title(t):       print(f"\n{YELLOW}{BOLD}  ━━━━  {t}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
def ask(prompt):    return input(f"  {CYAN}▶ {prompt}: {RESET}").strip()
def sep():          print(f"  {DIM}{'─' * 60}{RESET}")

def menu(options):
    for i, opt in enumerate(options, 1):
        print(f"  {YELLOW}[{i}]{RESET}  {opt}")
    return input(f"\n  {CYAN}▶ Elige una opción: {RESET}").strip()

def confirm(msg: str) -> bool:
    """Pide confirmación s/n. Retorna True si el usuario dice s/y."""
    resp = input(f"\n  {YELLOW}▶ {msg} (s/n): {RESET}").strip().lower()
    return resp in ("s", "si", "sí", "y", "yes")

# ─────────────────────────────────────────────────────────────
# BARRA DE PROGRESO
# ─────────────────────────────────────────────────────────────

class ProgressBar:
    """
    Barra de progreso para operaciones largas (brute force, etc).

    Uso:
        bar = ProgressBar(total=1000, label="Probando combinaciones")
        for i in range(1000):
            bar.update(i + 1)
        bar.done()
    """

    def __init__(self, total: int, label: str = "Progreso", width: int = 40):
        self.total   = max(total, 1)
        self.label   = label
        self.width   = width
        self.current = 0
        self._start  = time.time()
        self._last_render = -1
        self._render(0)

    def update(self, current: int):
        self.current = current
        pct = int(current * 100 / self.total)
        if pct != self._last_render:
            self._last_render = pct
            self._render(pct)

    def _render(self, pct: int):
        filled = int(self.width * pct / 100)
        bar    = "█" * filled + "░" * (self.width - filled)
        elapsed = time.time() - self._start
        sys.stdout.write(
            f"\r  {CYAN}{self.label}:{RESET} {YELLOW}[{bar}]{RESET} "
            f"{BOLD}{pct:>3}%{RESET}  {DIM}{self.current}/{self.total}  "
            f"({elapsed:.1f}s){RESET}   "
        )
        sys.stdout.flush()

    def done(self, msg: str = "Completado"):
        elapsed = time.time() - self._start
        bar = "█" * self.width
        sys.stdout.write(
            f"\r  {GREEN}{self.label}:{RESET} {GREEN}[{bar}]{RESET} "
            f"{BOLD}100%{RESET}  {DIM}{self.total}/{self.total}  "
            f"({elapsed:.1f}s) — {msg}{RESET}\n"
        )
        sys.stdout.flush()

    def abort(self, msg: str = "Interrumpido"):
        pct = int(self.current * 100 / self.total)
        elapsed = time.time() - self._start
        sys.stdout.write(
            f"\r  {RED}{self.label}:{RESET} {DIM}abortado en {pct}%  "
            f"({elapsed:.1f}s) — {msg}{RESET}\n"
        )
        sys.stdout.flush()


# ─────────────────────────────────────────────────────────────
# PAGINACIÓN DE RESULTADOS
# ─────────────────────────────────────────────────────────────

def paginate(items: list, page_size: int = 10, formatter=None):
    """
    Muestra una lista larga página por página.

    Args:
        items:      lista de cualquier cosa
        page_size:  cuántos items por página
        formatter:  función(item) → str para renderizar cada item.
                    Si es None se usa str().
    """
    if not items:
        warn("No hay resultados para mostrar.")
        return

    fmt      = formatter or str
    total    = len(items)
    pages    = (total + page_size - 1) // page_size
    page     = 0

    while True:
        start = page * page_size
        end   = min(start + page_size, total)
        sep()
        for idx, item in enumerate(items[start:end], start=start + 1):
            print(f"  {YELLOW}[{idx:>3}]{RESET}  {fmt(item)}")
        sep()
        print(f"\n  {DIM}Página {page + 1}/{pages}  —  {total} resultados totales{RESET}\n")

        if pages == 1:
            break

        nav_opts = []
        if page > 0:
            nav_opts.append(f"{CYAN}[p]{RESET} Anterior")
        if page < pages - 1:
            nav_opts.append(f"{CYAN}[n]{RESET} Siguiente")
        nav_opts.append(f"{CYAN}[q]{RESET} Salir")

        print("  " + "   ".join(nav_opts))
        choice = input(f"\n  {CYAN}▶ Navegación: {RESET}").strip().lower()

        if choice == "n" and page < pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "q":
            break


# ─────────────────────────────────────────────────────────────
# TABLA SIMPLE
# ─────────────────────────────────────────────────────────────

def table(rows: list[tuple], headers: list[str] = None):
    """
    Imprime una tabla simple alineada por columnas.

    Args:
        rows:    lista de tuplas con los valores
        headers: lista de encabezados (opcional)
    """
    if not rows:
        return

    all_rows = []
    if headers:
        all_rows.append(tuple(str(h) for h in headers))
    all_rows.extend(tuple(str(c) for c in row) for row in rows)

    col_count = max(len(r) for r in all_rows)
    widths    = [0] * col_count
    for row in all_rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    sep_line = "  " + "─┼─".join("─" * w for w in widths)

    for idx, row in enumerate(all_rows):
        cells = [str(c).ljust(widths[i]) for i, c in enumerate(row)]
        line  = "  " + " │ ".join(cells)
        if idx == 0 and headers:
            print(f"{BOLD}{YELLOW}{line}{RESET}")
            print(sep_line)
        else:
            print(f"{DIM}{line}{RESET}" if idx % 2 == 0 else line)
    print()