"""Panfleto: hoja carta, doble cara, 4 panfletos iguales por hoja.
Estilo DESIGN.md (raíz): lienzo pergamino, tarjetas blancas, vino y Deep Lagoon como bandas,
lila para etiquetas. Margen de hoja con marcas de corte (las impresoras no imprimen al borde).
1 unidad = 1 mm. Genera front.svg y back.svg."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from svgkit import Svg, crop_marks, qr_group  # noqa: E402

PW, PH = 215.9, 279.4             # carta
MARGIN = 6
W, H = (PW - 2 * MARGIN) / 2, (PH - 2 * MARGIN) / 2   # cada panfleto ≈ 102 × 134 mm
M = 9                             # margen interior
WINE, LILAC, LAGOON, PARCH, MIST, INK, STONE, PAPER = (
    "#421d24", "#d4c7ff", "#0c4243", "#f2f0eb", "#e3e3e2", "#292827", "#666666", "#ffffff")
# Blanco translúcido sobre las bandas, ya mezclado (VectorCraft/impresión sin transparencias).
ON_WINE, ON_LAGOON, LAGOON_CELL, LAGOON_LINE = "#c6bbbd", "#c2cfd0", "#2a595a", "#6d8e8e"
MONO = "DejaVu Sans Mono"
QUIZ_URL = "https://xsteban1410.github.io/ExpoEnglish/"


def front(s):
    s.rect(0, 0, W, H, "none", PARCH, 0)
    s.text(M, 13, "English presentation", 2.6, 600, STONE)
    s.text(M - 0.6, 30, "Linux", 17, 500, INK, spacing=-0.45)
    s.text(M, 38, "The free system that runs the world.", 4.0, 400, INK, spacing=-0.05)

    s.rect(M, 44, W - 2 * M, 26, "none", PAPER, 0, rx=4)
    s.text(M + 4, 51, "What is it?", 3.2, 600, INK)
    s.para(M + 4, 53.5, "An operating system, like Windows or macOS. Its heart is the kernel: "
                        "the part that talks to the hardware.", 2.9, W - 2 * M - 8, 1.35, fill=INK)

    facts = [("1991", "Linus Torvalds", "starts it as a hobby"), ("Free", "Open source", "the code is public"),
             ("500/500", "Supercomputers", "all run Linux")]
    cw = (W - 2 * M - 6) / 3
    for i, (big, a, b) in enumerate(facts):
        x = M + i * (cw + 3)
        s.rect(x, 74, cw, 24, "none", PAPER, 0, rx=4)
        s.text(x + 3, 83, big, 5.6 if len(big) < 6 else 4.6, 500, WINE, spacing=-0.15)
        s.text(x + 3, 89.5, a, 2.3, 600, INK)
        s.text(x + 3, 93.3, b, 2.3, 400, STONE)

    by = 104
    s.rect(0, by, W, H - by, "none", WINE, 0)
    s.text(M, by + 8, "It's everywhere", 3.8, 500, PAPER)
    qs = 22                                   # QR → encuesta, en tarjeta blanca a la derecha
    qx, qy = W - M - qs - 3, by + (H - by - qs - 6) / 2
    s.rect(qx, qy, qs + 6, qs + 6, "none", PAPER, 0, rx=3)
    s.add(qr_group(QUIZ_URL, qx + 3, qy + 3, qs, INK))
    tw = qx - M - 4
    s.para(M, by + 10.5, "Servers, Android phones, smart TVs, cars and even "
                         "a NASA helicopter on Mars.", 2.7, tw, 1.35, fill=ON_WINE)
    s.text(M, H - 5, "What Linux are you? Scan the QR →", 2.5, 600, PAPER)


def back(s):
    s.rect(0, 0, W, H, "none", PARCH, 0)
    s.text(M - 0.3, 19, "Distros", 8.5, 500, INK, spacing=-0.2)
    s.text(M, 26, "Same kernel, many flavours.", 3.6, 400, INK)

    fams = [("Debian", "Debian · Ubuntu · Mint", "stable, great for beginners"),
            ("Red Hat", "Fedora · RHEL", "modern, used by companies"),
            ("Arch", "Arch · Manjaro · CachyOS", "fast, always up to date")]
    s.rect(M, 31, W - 2 * M, 40, "none", PAPER, 0, rx=4)
    for i, (name, members, desc) in enumerate(fams):
        y = 31 + i * 13.3
        if i:
            s.line(M + 4, y, W - M - 4, y, MIST, 0.25)
        s.rect(M + 4, y + 3.2, 16, 5.4, "none", LILAC, 0, rx=2.7)
        s.text(M + 12, y + 6.8, name, 2.4, 600, INK, "middle")
        s.text(M + 24, y + 6.3, members, 3.0, 500, INK)
        s.text(M + 24, y + 10.2, desc, 2.4, 400, STONE)

    s.text(M, 80, "5 basic commands", 3.8, 500, INK)
    cmds = [("ls", "list files"), ("cd", "change folder"), ("pwd", "where am I?"),
            ("mkdir", "new folder"), ("sudo", "admin power")]
    for i, (c, d) in enumerate(cmds):
        x, y = M + (i % 2) * (W - 2 * M) / 2, 86.5 + (i // 2) * 5
        s.text(x, y, c, 2.8, 700, WINE, family=MONO)
        s.text(x + 12, y, d, 2.8, 400, INK)

    by = 101
    s.rect(0, by, W, H - by, "none", LAGOON, 0)
    layers = [("Applications", "browser, games"), ("Shell & system", "commands"),
              ("Kernel", "the heart"), ("Hardware", "CPU, memory")]
    for i, (name, sub) in enumerate(layers):
        ly = by + 4.5 + i * 6.6
        kernel = name == "Kernel"
        s.rect(M, ly, 37, 5.6, LAGOON_LINE, LILAC if kernel else LAGOON_CELL, 0 if kernel else 0.25, rx=1.6)
        s.text(M + 2, ly + 3.8, name, 2.4, 600, INK if kernel else PAPER)
        s.text(M + 35, ly + 3.8, sub, 1.9, 400, INK if kernel else ON_LAGOON, "end")
    tx = M + 41
    s.text(tx, by + 10, "How does", 4.6, 500, PAPER, spacing=-0.1)
    s.text(tx, by + 15.5, "it work?", 4.6, 500, PAPER, spacing=-0.1)
    s.para(tx, by + 18, "Like a cake: layers. Your click goes down to the hardware, "
                        "and the answer comes back up.", 2.5, W - M - tx, 1.35, fill=ON_LAGOON)


def sheet(draw, mirror):
    page = Svg(PW, PH)
    for r in range(2):
        for c in range(2):
            col = 1 - c if mirror else c   # reverso espejado para dúplex por borde largo
            p = Svg(W, H)
            draw(p)
            page.raw_group(p.body(), f"translate({MARGIN + col * W:.2f},{MARGIN + r * H:.2f})")
    crop_marks(page, [MARGIN + i * W for i in range(3)], [MARGIN + i * H for i in range(3)], gap=0.8, length=4)
    return page


sheet(front, False).save("front.svg")
sheet(back, True).save("back.svg")
print("ok: front.svg back.svg")
