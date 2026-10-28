"""Panfleto: hoja carta, doble cara, 4 panfletos iguales por hoja (4.25 × 5.5 in cada uno).
Estilo DESIGN.md (Apple) adaptado a papel: fondo blanco, tinta #1d1d1f, hairlines #d2d2d7,
sin acento azul (la acción con QR va en las tarjetas). 1 unidad = 1 mm. Genera front.svg y back.svg."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from svgkit import Svg  # noqa: E402

PW, PH = 215.9, 279.4             # carta
W, H = PW / 2, PH / 2             # cada panfleto
M = 9                             # margen interior
INK, GRAPH, ASH, LINE, FROST = "#1d1d1f", "#333333", "#707070", "#d2d2d7", "#f5f5f7"
MONO = "DejaVu Sans Mono"


def front(s):
    cx = W / 2
    s.text(cx, 16, "ENGLISH PRESENTATION", 2.6, 600, ASH, "middle", spacing=0.4)
    s.text(cx, 36, "Linux", 17, 600, INK, "middle", spacing=-0.3)
    s.text(cx, 45, "The free system that runs the world.", 4.2, 300, INK, "middle")
    s.line(M, 52, W - M, 52, LINE, 0.25)
    s.text(M, 61, "What is it?", 4.4, 600, INK)
    y = s.para(M, 63.5, "An operating system, like Windows or macOS. Its heart is the kernel: "
                        "the part that talks to the hardware.", 3.2, W - 2 * M, 1.35, fill=GRAPH)
    s.line(M, y + 3, W - M, y + 3, LINE, 0.25)
    facts = [("1991", "Linus Torvalds", "starts it as a hobby"), ("Free", "Open source:", "the code is public"),
             ("500/500", "Top supercomputers", "run Linux")]
    col = (W - 2 * M) / 3
    for i, (big, a, b) in enumerate(facts):
        x = M + col * i + col / 2
        s.text(x, y + 15, big, 6.2 if len(big) < 6 else 5.2, 600, INK, "middle", spacing=-0.1)
        s.text(x, y + 21, a, 2.5, 600, GRAPH, "middle")
        s.text(x, y + 24.5, b, 2.5, 300, GRAPH, "middle")
    y += 31
    s.line(M, y, W - M, y, LINE, 0.25)
    s.text(M, y + 9, "It's everywhere", 4.4, 600, INK)
    s.para(M, y + 11.5, "Internet servers, Android phones, smart TVs, cars, routers, "
                        "the Steam Deck and even a NASA helicopter on Mars.", 3.2, W - 2 * M, 1.35, fill=GRAPH)
    s.text(cx, H - 7, "Free · Secure · Customizable · Big community", 2.6, 300, ASH, "middle")


def back(s):
    s.text(M, 18, "Distros", 7.5, 600, INK, spacing=-0.15)
    s.text(M, 25, "Same kernel, many flavours.", 3.6, 300, INK)
    fams = [("Debian", "Debian · Ubuntu · Linux Mint", "stable, great for beginners"),
            ("Red Hat", "Fedora · RHEL", "modern, used by companies"),
            ("Arch", "Arch · Manjaro · CachyOS", "fast, always up to date")]
    y = 31
    for name, members, desc in fams:
        s.line(M, y, W - M, y, LINE, 0.25)
        s.text(M, y + 5.5, name, 3.4, 600, INK)
        s.text(M + 20, y + 5.5, members, 3.0, 400, GRAPH)
        s.text(M + 20, y + 9.6, desc, 2.6, 300, ASH)
        y += 12.5
    s.line(M, y, W - M, y, LINE, 0.25)
    s.text(M, y + 9, "5 basic commands", 4.4, 600, INK)
    cmds = [("ls", "list files"), ("cd", "change folder"), ("pwd", "where am I?"),
            ("mkdir", "new folder"), ("sudo", "admin power")]
    for i, (c, d) in enumerate(cmds):
        x, yy = M + (i % 2) * (W - 2 * M) / 2, y + 16 + (i // 2) * 5.2
        s.text(x, yy, c, 3.0, 700, INK, family=MONO)
        s.text(x + 13, yy, d, 2.9, 300, GRAPH)
    # Bloque «How does it work?»: las capas de Linux (el QR va solo en las tarjetas)
    by = H - 40
    s.rect(M - 2, by, W - 2 * M + 4, 33, LINE, FROST, 0.25, rx=2)
    layers = [("Applications", "browser, games"), ("Shell & system", "commands"),
              ("Kernel", "the heart"), ("Hardware", "CPU, memory, disk")]
    for i, (name, sub) in enumerate(layers):
        ly = by + 3 + i * 6.9
        s.rect(M + 2, ly, 40, 6, INK if name == "Kernel" else LINE, "#ffffff", 0.35, rx=1.5)
        s.text(M + 4, ly + 4, name, 2.5, 600, INK)
        s.text(M + 40, ly + 4, sub, 2.0, 300, ASH, "end")
    tx = M + 47
    s.text(tx, by + 9, "How does", 5.0, 600, INK, spacing=-0.1)
    s.text(tx, by + 14.5, "it work?", 5.0, 600, INK, spacing=-0.1)
    s.para(tx, by + 17, "Like a cake: layers. Your click goes down to the hardware, "
                        "and the answer comes back up.", 2.6, W - M - tx, 1.35, fill=GRAPH)


def sheet(draw, mirror):
    page = Svg(PW, PH)
    for r in range(2):
        for c in range(2):
            col = 1 - c if mirror else c   # reverso espejado para dúplex por borde largo
            p = Svg(W, H)
            draw(p)
            page.raw_group(p.body(), f"translate({col * W:.2f},{r * H:.2f})")
    # Líneas de corte (centro) y marcas en los bordes
    page.line(PW / 2, 0, PW / 2, PH, LINE, 0.2, "1.5 1.5")
    page.line(0, PH / 2, PW, PH / 2, LINE, 0.2, "1.5 1.5")
    return page


sheet(front, False).save("front.svg")
sheet(back, True).save("back.svg")
print("ok: front.svg back.svg")
