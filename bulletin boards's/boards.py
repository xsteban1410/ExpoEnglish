"""Boceto B/N de las 3 carteleras (pliego 100 × 70 cm, horizontal). 1 unidad = 1 mm.
Genera board1..3.svg; build.sh los pasa a PDF/.vectorcraft con VectorCraft y los une con PdfCraft."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from svgkit import Svg, qr_group  # noqa: E402

W, H = 1000, 700
GRAY, NOTE = "#999", "#777"
MONO = "DejaVu Sans Mono"
QUIZ_URL = "https://xsteban1410.github.io/ExpoEnglish/"
T, HD, TX = 80, 30, 22  # tamaños: título, encabezado, texto


def cap_cm(size):
    return f"{size * 0.73 / 10:.1f}".replace(".", ",")


def board(n, title, subtitle, size=T):
    s = Svg(W, H)
    for x in range(100, W, 100):  # cuadrícula de 10 cm para copiar a escala
        s.line(x, 0, x, H, GRAY, 0.3, "4 4")
        s.text(x + 2, 8, f"{x // 10}", 6, fill=GRAY)
    for y in range(100, H, 100):
        s.line(0, y, W, y, GRAY, 0.3, "4 4")
        s.text(2, y - 2, f"{y // 10}", 6, fill=GRAY)
    s.rect(1, 1, W - 2, H - 2, sw=1)
    s.text(40, 115, title, size, 700)
    s.text(42, 160, subtitle, 28, 300)
    s.text(40, 690, f"Pliego {n}/3 · 100 × 70 cm horizontal · cuadrícula = 10 cm · "
                    f"alto de letra: título ≈ {cap_cm(size)} cm, encabezados ≈ {cap_cm(HD)} cm, "
                    f"texto ≈ {cap_cm(TX)} cm", 11, fill=NOTE, italic=True)
    return s


def card(s, x, y, w, h, head, body=None, size=TX):
    s.rect(x, y, w, h, sw=1.2, rx=6)
    s.text(x + 18, y + 18 + HD * 0.8, head, HD, 700)
    if body:
        return s.para(x + 18, y + 30 + HD, body, size, w - 36)
    return y + 30 + HD


def note(s, x, y, txt):
    s.text(x, y, txt, 11, fill=NOTE, italic=True)


# ---------- Pliego 1: What is Linux? ----------
s = board(1, "WHAT IS LINUX?", "An operating system, like Windows or macOS.")
s.circle(880, 90, 48, sw=1)
s.text(880, 98, "Tux", 24, 700, anchor="middle")
note(s, 790, 158, "silueta simple del pingüino (opcional)")

yb = card(s, 40, 190, 440, 230, "OPERATING SYSTEM",
          "The program that controls the computer. It connects the hardware with your programs.")
for i, lab in enumerate(["Hardware", "OS", "Programs"]):
    bx = 60 + i * 140
    s.rect(bx, yb + 10, 110, 50, rx=4)
    s.text(bx + 55, yb + 42, lab, 18, 600, anchor="middle")
    if i:
        s.arrow(bx - 28, yb + 35, bx - 4, yb + 35)
        s.arrow(bx - 4, yb + 35, bx - 28, yb + 35)

card(s, 520, 190, 440, 230, "THE KERNEL",
     "The heart of Linux. It talks directly to the hardware: the processor, the memory and the disk. "
     "Kernel + tools = a complete operating system.")

s.rect(40, 450, 580, 210, sw=1.2, rx=6)
s.text(58, 492, "HISTORY", HD, 700)
s.arrow(70, 560, 600, 560, sw=1.5)
for x, year, a, b in [(110, "1983", "GNU project", "Richard Stallman"),
                      (290, "1991", "Linus Torvalds,", "student in Finland"),
                      (470, "TODAY", "thousands of", "developers")]:
    s.line(x, 548, x, 572, sw=1.5)
    s.text(x, 540, year, 26, 700, anchor="middle")
    s.text(x, 600, a, 18, anchor="middle")
    s.text(x, 624, b, 18, anchor="middle")
s.text(290, 650, '"Just a hobby, it won\'t be big."', 16, italic=True, anchor="middle")

card(s, 660, 450, 300, 210, "FREE & OPEN",
     "Free: $0 + freedom to use, study, change and share.\nOpen source: the code is public.", 19)
s.save("board1.svg")

# ---------- Pliego 2: Distros & how it works ----------
s = board(2, "DISTROS & HOW IT WORKS", "Same kernel, many flavours. And Linux works in layers.", 62)
s.rect(190, 185, 220, 52, sw=1.5, rx=6)
s.text(300, 220, "LINUX KERNEL", 24, 700, anchor="middle")
fams = [("DEBIAN", ["Debian", "Ubuntu", "Linux Mint"], "for beginners"),
        ("RED HAT", ["Fedora", "Red Hat (RHEL)"], "for companies"),
        ("ARCH", ["Arch Linux", "Manjaro", "CachyOS"], "fast & up to date")]
for i, (head, items, desc) in enumerate(fams):
    cx = 120 + i * 180
    s.arrow(300, 237, cx, 282, sw=1.2)
    s.rect(cx - 80, 285, 160, 205, sw=1.2, rx=6)
    s.text(cx, 318, head, 22, 700, anchor="middle")
    s.text(cx, 338, "family", 14, anchor="middle", italic=True)
    s.line(cx - 65, 350, cx + 65, 350)
    for j, it in enumerate(items):
        s.text(cx, 384 + j * 30, it, 18, anchor="middle")
    s.text(cx, 478, desc, 14, italic=True, anchor="middle")
card(s, 40, 515, 520, 150, "SPECIAL DISTROS",
     "Kali Linux → security · SteamOS → games\nLike ice cream: same base, many flavours!", 19)

s.text(600, 212, "HOW IT WORKS", HD, 700)
for i, (head, sub) in enumerate([("APPLICATIONS", "browser · games"), ("SHELL & SYSTEM", "commands"),
                                 ("KERNEL", "the heart"), ("HARDWARE", "CPU · memory · disk")]):
    y = 232 + i * 56
    s.rect(645, y, 315, 48, sw=1.2 if head != "KERNEL" else 2.5, rx=6)
    s.text(660, y + 31, head, 20, 700)
    s.text(945, y + 31, sub, 14, anchor="end", italic=True)
s.arrow(608, 234, 608, 452, sw=1.5)
s.arrow(628, 452, 628, 234, sw=1.5)
note(s, 600, 470, "flechas: el clic baja, la respuesta sube")

s.rect(600, 485, 360, 180, sw=1.2, rx=6)
s.text(618, 520, "TERMINAL: 5 COMMANDS", 24, 700)
cmds = [("ls", "show the files"), ("cd", "change folder"), ("pwd", "where am I?"),
        ("mkdir", "new folder"), ("sudo", "admin (careful!)")]
for j, (c, d) in enumerate(cmds):
    y = 552 + j * 25
    s.text(622, y, c, 18, 700, family=MONO)
    s.text(712, y, "→ " + d, 17)
s.save("board2.svg")

# ---------- Pliego 3: Linux is everywhere ----------
s = board(3, "LINUX IS EVERYWHERE", "You use it every day, maybe without knowing it!")
places = [("SERVERS", "Most of the internet: Google, Netflix"), ("ANDROID", "Billions of phones"),
          ("SUPERCOMPUTERS", "500 of the top 500"), ("TVs & CARS", "Smart TVs, cars, routers"),
          ("MARS", "NASA Ingenuity helicopter"), ("GAMES", "Steam Deck (SteamOS)")]
for i, (head, txt) in enumerate(places):
    x, y = 40 + (i % 3) * 200, 190 + (i // 3) * 150
    s.rect(x, y, 185, 135, sw=1.2, rx=6)
    s.text(x + 92, y + 40, head, 19 if len(head) < 12 else 16, 700, anchor="middle")
    s.para(x + 14, y + 58, txt, 17, 160)
note(s, 40, 490, "opcional: un icono muy simple en cada caja")

s.rect(660, 190, 300, 285, sw=1.2, rx=6)
s.text(678, 232, "WHY USE LINUX?", 28, 700)
for j, r in enumerate(["It's free", "It's secure", "It's customizable", "Old PCs live again",
                       "Big, friendly community"]):
    y = 280 + j * 40
    s.circle(695, y - 7, 14, sw=1)
    s.text(695, y, str(j + 1), 16, 700, anchor="middle")
    s.text(720, y, r, 20)

s.rect(40, 505, 920, 160, sw=1.5, rx=6)
s.text(70, 560, "WHAT LINUX ARE YOU?", 44, 700)
s.text(72, 605, "Scan the QR code and take the quiz!", 26)
s.text(72, 640, "xsteban1410.github.io/ExpoEnglish", 18, family=MONO)
s.rect(800, 515, 140, 140, dash="5 4")
s.add(qr_group(QUIZ_URL, 810, 525, 120))
note(s, 640, 660, "pega aquí el QR impreso (≈ 14 cm)")
s.save("board3.svg")
print("ok: board1..3.svg")
