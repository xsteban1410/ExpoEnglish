#!/bin/sh
# Regenera las tarjetas: SVG (Python) → cards.pdf (2 caras) + front/back.vectorcraft.
set -e
cd "$(dirname "$0")"
python3 cards.py
../tools/svg2pdf.sh cards.pdf front.svg back.svg
