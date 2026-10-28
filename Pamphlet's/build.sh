#!/bin/sh
# Regenera el panfleto: SVG (Python) → pamphlet.pdf (2 caras) + pamphlet.ai + front/back.vectorcraft.
set -e
cd "$(dirname "$0")"
python3 pamphlet.py
../tools/svg2pdf.sh pamphlet.pdf front.svg back.svg
../tools/pdf2ai.sh pamphlet.pdf pamphlet.ai
