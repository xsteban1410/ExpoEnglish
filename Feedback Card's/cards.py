"""Tarjetas de feedback: hoja carta, 10 tarjetas (2 × 5) de 3.5 × 2 in, doble cara.
Estilo DESIGN.md (Apple) en papel. 1 unidad = 1 mm. Genera front.svg, back.svg y qr.svg."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from svgkit import Svg, qr_group  # noqa: E402

PW, PH = 215.9, 279.4
CW, CH = 88.9, 50.8                       # 3.5 × 2 in
COLS, ROWS = 2, 5
X0, Y0 = (PW - COLS * CW) / 2, (PH - ROWS * CH) / 2
INK, GRAPH, ASH, LINE, FROST, BLUE = "#1d1d1f", "#333333", "#707070", "#d2d2d7", "#f5f5f7", "#0071e3"
QUIZ_URL = "https://xsteban1410.github.io/ExpoEnglish/"
M = 5


def front(s):
    s.rect(0, 0, 38, CH, "none", FROST, 0)
    s.add(qr_group(QUIZ_URL, 5, (CH - 28) / 2, 28, INK))
    x = 44
    s.text(x, 11, "LINUX QUIZ", 2.2, 600, ASH, spacing=0.3)
    s.text(x, 20, "What Linux", 5.4, 600, INK, spacing=-0.1)
    s.text(x, 26.5, "are you?", 5.4, 600, INK, spacing=-0.1)
    s.text(x, 32.5, "8 questions · 2 minutes", 2.6, 300, GRAPH)
    s.rect(x, 36.5, 22, 6, "none", BLUE, 0, rx=3)       # píldora
    s.text(x + 11, 40.6, "Scan me", 2.6, 400, "#f4f8fb", "middle")


def back(s):
    s.text(M, 10, "Thanks for listening!", 3.8, 600, INK)
    s.para(M, 12.5, "Linux has hundreds of versions called distros. Answer a short quiz "
                    "and discover the one that matches your personality.", 2.45, CW - 2 * M, 1.35, fill=GRAPH)
    y = 28
    for i, (dx, step) in enumerate([(0, "Scan the QR"), (23, "Answer 8 questions"), (52, "Meet your distro")]):
        x = M + dx
        s.circle(x + 2.2, y - 0.9, 2.2, INK, "none", 0.25)
        s.text(x + 2.2, y, str(i + 1), 2.2, 600, INK, "middle")
        s.text(x + 5.5, y, step, 2.2, 400, GRAPH)
    s.line(M, 32, CW - M, 32, LINE, 0.2)
    s.text(M, 38, "Fun fact", 2.4, 600, INK)
    s.text(M + 12, 38, "Android, on billions of phones, uses the Linux kernel.", 2.2, 300, GRAPH)
    s.text(M, 45, "Tell me your result after the class!", 2.4, 400, INK)
    s.text(CW - M, 45, "xsteban1410.github.io/ExpoEnglish", 1.9, 300, ASH, "end")


def sheet(draw, mirror):
    page = Svg(PW, PH)
    for r in range(ROWS):
        for c in range(COLS):
            col = COLS - 1 - c if mirror else c   # reverso espejado para dúplex por borde largo
            p = Svg(CW, CH)
            draw(p)
            page.raw_group(p.body(), f"translate({X0 + col * CW:.2f},{Y0 + r * CH:.2f})")
    for c in range(COLS + 1):                     # guías de corte
        page.line(X0 + c * CW, 0, X0 + c * CW, PH, LINE, 0.15)
    for r in range(ROWS + 1):
        page.line(0, Y0 + r * CH, PW, Y0 + r * CH, LINE, 0.15)
    return page


sheet(front, False).save("front.svg")
sheet(back, True).save("back.svg")
qr = Svg(40, 40)
qr.add(qr_group(QUIZ_URL, 2, 2, 36, INK))
qr.save("qr.svg")
print("ok: front.svg back.svg qr.svg")
