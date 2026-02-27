GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
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

def banner():       print(BANNER)
def ok(k, v):       print(f"\n  {GREEN}✔ {BOLD}{k}:{RESET}  {CYAN}{v}{RESET}\n")
def err(msg):       print(f"\n  {RED}✘ {msg}{RESET}\n")
def info(msg):      print(f"  {DIM}{msg}{RESET}")
def title(t):       print(f"\n{YELLOW}{BOLD}  ━━━━  {t}  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}\n")
def ask(prompt):    return input(f"  {CYAN}▶ {prompt}: {RESET}").strip()
def menu(options):
    for i, opt in enumerate(options, 1):
        print(f"  {YELLOW}[{i}]{RESET}  {opt}")
    return input(f"\n  {CYAN}▶ Elige una opción: {RESET}").strip()