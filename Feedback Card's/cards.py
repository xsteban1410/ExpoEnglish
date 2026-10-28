"""Tarjetas de feedback: hoja carta, 10 tarjetas (2 × 5) de 3.5 × 2 in, doble cara.
Estilo DESIGN.md (raíz): frente pergamino con el QR en tarjeta blanca y botón vino;
reverso Deep Lagoon. 1 unidad = 1 mm. Genera front.svg, back.svg y qr.svg."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from svgkit import Svg, crop_marks, qr_group  # noqa: E402

PW, PH = 215.9, 279.4
CW, CH = 88.9, 50.8                       # 3.5 × 2 in
COLS, ROWS = 2, 5
X0, Y0 = (PW - COLS * CW) / 2, (PH - ROWS * CH) / 2
WINE, LILAC, LAGOON, PARCH, INK, STONE, PAPER = (
    "#421d24", "#d4c7ff", "#0c4243", "#f2f0eb", "#292827", "#666666", "#ffffff")
ON_LAGOON, ON_LAGOON_DIM, LAGOON_LINE = "#ced9d9", "#9eb3b4", "#3d6869"   # blanco 80 %, 60 %, 20 % ya mezclado
QUIZ_URL = "https://xsteban1410.github.io/ExpoEnglish/"
M = 5


def front(s):
    s.rect(0, 0, CW, CH, "none", PARCH, 0)
    s.rect(4, 6.4, 38, 38, "none", PAPER, 0, rx=3)
    s.add(qr_group(QUIZ_URL, 7, 9.4, 32, INK))
    x = 47
    s.text(x, 11, "Linux quiz", 2.3, 600, STONE)
    s.text(x, 20, "What Linux", 5.2, 500, INK, spacing=-0.12)
    s.text(x, 26.3, "are you?", 5.2, 500, INK, spacing=-0.12)
    s.text(x, 31.6, "8 questions · 2 minutes", 2.4, 400, STONE)
    s.rect(x, 35.5, 25, 7, "none", WINE, 0, rx=2)
    s.text(x + 12.5, 40, "Scan me →", 2.6, 500, PAPER, "middle")


def back(s):
    s.rect(0, 0, CW, CH, "none", LAGOON, 0)
    s.text(M, 10, "Thanks for listening!", 3.8, 500, PAPER)
    s.para(M, 12.5, "Linux has hundreds of versions called distros. Answer a short quiz "
                    "and discover the one that matches your personality.", 2.4, CW - 2 * M, 1.35, fill=ON_LAGOON)
    y = 28
    for i, (dx, step) in enumerate([(0, "Scan the QR"), (23, "Answer 8 questions"), (52, "Meet your distro")]):
        x = M + dx
        s.circle(x + 2.2, y - 0.9, 2.2, "none", LILAC, 0)
        s.text(x + 2.2, y, str(i + 1), 2.2, 600, INK, "middle")
        s.text(x + 5.5, y, step, 2.2, 500, PAPER)
    s.line(M, 32, CW - M, 32, LAGOON_LINE, 0.25)
    s.text(M, 38, "Fun fact", 2.4, 600, LILAC)
    s.text(M + 12, 38, "Android, on billions of phones, uses the Linux kernel.", 2.2, 400, ON_LAGOON)
    s.text(M, 45, "Tell me your result after the class!", 2.4, 500, PAPER)
    s.text(CW - M, 45, "xsteban1410.github.io/ExpoEnglish", 1.9, 400, ON_LAGOON_DIM, "end")


def sheet(draw, mirror):
    page = Svg(PW, PH)
    for r in range(ROWS):
        for c in range(COLS):
            col = COLS - 1 - c if mirror else c   # reverso espejado para dúplex por borde largo
            p = Svg(CW, CH)
            draw(p)
            page.raw_group(p.body(), f"translate({X0 + col * CW:.2f},{Y0 + r * CH:.2f})")
    crop_marks(page, [X0 + c * CW for c in range(COLS + 1)], [Y0 + r * CH for r in range(ROWS + 1)])
    return page


sheet(front, False).save("front.svg")
sheet(back, True).save("back.svg")
qr = Svg(40, 40)
qr.add(qr_group(QUIZ_URL, 2, 2, 36, INK))
qr.save("qr.svg")
print("ok: front.svg back.svg qr.svg")
