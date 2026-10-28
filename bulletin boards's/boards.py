"""Boceto B/N de las 4 carteleras (pliego 100 × 70 cm, horizontal). 1 unidad = 1 mm.
Genera board1..4.svg; build.sh los pasa a PDF/.vectorcraft con VectorCraft y los une con PdfCraft."""
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


def board(n, title, subtitle):
    s = Svg(W, H)
    for x in range(100, W, 100):  # cuadrícula de 10 cm para copiar a escala
        s.line(x, 0, x, H, GRAY, 0.3, "4 4")
        s.text(x + 2, 8, f"{x // 10}", 6, fill=GRAY)
    for y in range(100, H, 100):
        s.line(0, y, W, y, GRAY, 0.3, "4 4")
        s.text(2, y - 2, f"{y // 10}", 6, fill=GRAY)
    s.rect(1, 1, W - 2, H - 2, sw=1)
    s.text(40, 115, title, T, 700)
    s.text(42, 160, subtitle, 28, 300)
    s.text(40, 690, f"Pliego {n}/4 · 100 × 70 cm horizontal · cuadrícula = 10 cm · "
                    f"alto de letra: título ≈ {cap_cm(T)} cm, encabezados ≈ {cap_cm(HD)} cm, "
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

# ---------- Pliego 2: Distros ----------
s = board(2, "DISTROS", "Distro = Linux kernel + programs + design + tools.")
s.rect(370, 190, 260, 60, sw=1.5, rx=6)
s.text(500, 230, "LINUX KERNEL", 26, 700, anchor="middle")
fams = [("DEBIAN FAMILY", ["Debian", "Ubuntu", "Linux Mint"], "stable · great for beginners"),
        ("RED HAT FAMILY", ["Fedora", "Red Hat Enterprise"], "modern · used by companies"),
        ("ARCH FAMILY", ["Arch Linux", "Manjaro", "CachyOS"], "fast · always up to date")]
for i, (head, items, desc) in enumerate(fams):
    cx = 175 + i * 325
    s.arrow(500, 250, cx, 312, sw=1.2)
    s.rect(cx - 140, 315, 280, 210, sw=1.2, rx=6)
    s.text(cx, 352, head, 24, 700, anchor="middle")
    s.line(cx - 120, 366, cx + 120, 366)
    for j, it in enumerate(items):
        s.text(cx, 404 + j * 34, it, TX, anchor="middle")
    s.text(cx, 510, desc, 16, italic=True, anchor="middle")
card(s, 40, 550, 440, 115, "SPECIAL DISTROS",
     "Kali Linux → security · SteamOS → video games", 19)
card(s, 520, 550, 440, 115, "LIKE ICE CREAM",
     "Same base, many flavours. There are hundreds of distros!", 19)
s.save("board2.svg")

# ---------- Pliego 3: How does it work? ----------
s = board(3, "HOW DOES IT WORK?", "Linux is like a cake: it has layers.")
layers = [("APPLICATIONS", "browser · music · games"), ("SHELL & SYSTEM", "commands · services"),
          ("KERNEL", "the heart"), ("HARDWARE", "CPU · memory · disk · screen")]
for i, (head, sub) in enumerate(layers):
    y = 190 + i * 115
    s.rect(110, y, 360, 100, sw=1.2 if head != "KERNEL" else 2.5, rx=6)
    s.text(290, y + 45, head, 26, 700, anchor="middle")
    s.text(290, y + 78, sub, 17, anchor="middle", italic=True)
s.arrow(60, 200, 60, 640, sw=1.5)
s.arrow(85, 640, 85, 200, sw=1.5)
note(s, 40, 670, "flechas: el clic baja, la respuesta sube")

s.rect(520, 190, 440, 230, sw=1.2, rx=6)
s.text(538, 232, "DESKTOP  vs  TERMINAL", HD, 700)
s.line(740, 250, 740, 405, dash="6 4")
s.para(538, 255, "Windows, icons and a mouse. GNOME · KDE Plasma", 18, 190)
s.para(758, 255, "Write commands. Fast and powerful!", 18, 185)
s.rect(758, 340, 180, 60, fill="#000", rx=4)
s.text(770, 378, "$ _", 24, 700, fill="#fff", family=MONO)

s.rect(520, 450, 440, 210, sw=1.2, rx=6)
s.text(538, 492, "5 BASIC COMMANDS", HD, 700)
cmds = [("ls", "show the files"), ("cd", "change folder"), ("pwd", "where am I?"),
        ("mkdir", "new folder"), ("sudo", "admin power (careful!)")]
for j, (c, d) in enumerate(cmds):
    y = 528 + j * 28
    s.text(545, y, c, 20, 700, family=MONO)
    s.text(650, y, "→ " + d, 19)
s.save("board3.svg")

# ---------- Pliego 4: Linux is everywhere ----------
s = board(4, "LINUX IS EVERYWHERE", "You use it every day, maybe without knowing it!")
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
s.save("board4.svg")
print("ok: board1..4.svg")
