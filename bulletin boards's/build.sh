#!/bin/sh
# Regenera el boceto: SVG (Python) → boards.pdf + board1..4.vectorcraft.
set -e
cd "$(dirname "$0")"
python3 boards.py
../tools/svg2pdf.sh boards.pdf board1.svg board2.svg board3.svg board4.svg
