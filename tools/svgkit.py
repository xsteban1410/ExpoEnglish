"""Helpers mínimos para generar SVG (1 unidad = 1 mm) que luego convierte VectorCraft."""
from xml.sax.saxutils import escape

FONT = "Inter"


class Svg:
    def __init__(self, w_mm, h_mm):
        self.w, self.h, self.parts = w_mm, h_mm, []

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, stroke="#000", fill="none", sw=0.5, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke="#000", sw=0.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, cx, cy, r, stroke="#000", fill="none", sw=0.5):
        self.add(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def arrow(self, x1, y1, x2, y2, stroke="#000", sw=0.5, head=None):
        """Flecha recta con punta triangular simple."""
        import math
        head = head or sw * 6
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
        self.line(x1, y1, bx, by, stroke, sw)
        p = [(x2, y2),
             (bx + head * 0.5 * math.sin(a), by - head * 0.5 * math.cos(a)),
             (bx - head * 0.5 * math.sin(a), by + head * 0.5 * math.cos(a))]
        self.add('<polygon points="' + " ".join(f"{px:.2f},{py:.2f}" for px, py in p) + f'" fill="{stroke}"/>')

    def text(self, x, y, s, size, weight=400, fill="#000", anchor="start", italic=False,
             family=FONT, spacing=0):
        # Inter no trae cursiva instalada: «italic» se dibuja en Light.
        st, weight = ("", 300) if italic else ("", weight)
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        self.add(f'<text x="{x:.2f}" y="{y:.2f}" font-family="{family}" font-size="{size:.2f}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}{ls}>{escape(s)}</text>')

    def para(self, x, y, s, size, width, lh=1.3, **kw):
        """Texto con salto de línea aproximado; devuelve la y siguiente.
        shortcut: ancho medio de glifo 0.53·size (Inter); si se cambia de fuente, revisar los PNG."""
        for line in wrap(s, width, size):
            self.text(x, y + size * 0.8, line, size, **kw)
            y += size * lh
        return y

    def image(self, x, y, w, h, href):
        self.add(f'<image x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" href="{href}"/>')

    def raw_group(self, inner, transform=""):
        self.add(f'<g transform="{transform}">{inner}</g>')

    def body(self):
        return "\n".join(self.parts)

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                    f'width="{self.w}mm" height="{self.h}mm" viewBox="0 0 {self.w} {self.h}">\n'
                    f'<rect width="{self.w}" height="{self.h}" fill="#fff"/>\n{self.body()}\n</svg>\n')


def wrap(s, width, size):
    max_chars = max(1, int(width / (size * 0.53)))
    out = []
    for para in s.split("\n"):
        line = ""
        for word in para.split():
            cand = f"{line} {word}".strip()
            if len(cand) > max_chars and line:
                out.append(line)
                line = word
            else:
                line = cand
        out.append(line)
    return out


def qr_group(data, x, y, size, fill="#000"):
    """QR como rectángulos SVG (qrencode → matriz), sin depender de imágenes."""
    import subprocess
    rows = subprocess.run(["qrencode", "-t", "ASCII", "-m", "0", "-l", "M", data],
                          capture_output=True, text=True, check=True).stdout.splitlines()
    # En ASCII cada módulo son dos caracteres '#'.
    rows = [r[::2] for r in rows if r.strip() or r]
    n = len(rows)
    m = size / n
    parts = [f'<rect x="{x + c * m:.3f}" y="{y + r * m:.3f}" width="{m + 0.02:.3f}" height="{m + 0.02:.3f}" fill="{fill}"/>'
             for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "#"]
    return "".join(parts)


def crop_marks(page, xs, ys, stroke="#292827", gap=1.5, length=4):
    """Marcas de corte en el margen de la hoja para cada x (verticales) e y (horizontales)."""
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    for x in xs:
        page.line(x, y0 - gap - length, x, y0 - gap, stroke, 0.2)
        page.line(x, y1 + gap, x, y1 + gap + length, stroke, 0.2)
    for y in ys:
        page.line(x0 - gap - length, y, x0 - gap, y, stroke, 0.2)
        page.line(x1 + gap, y, x1 + gap + length, y, stroke, 0.2)
