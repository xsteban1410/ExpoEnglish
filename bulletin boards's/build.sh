#!/bin/sh
# Regenera el boceto: SVG (Python) → PDF y .vectorcraft (VectorCraft) → boards.pdf (PdfCraft).
set -e
cd "$(dirname "$0")"
T=../tools
python3 boards.py
for i in 1 2 3 4; do
  $T/vc convert "$PWD/board$i.svg" "$PWD/board$i.pdf" >/dev/null
  $T/vc convert "$PWD/board$i.svg" "$PWD/board$i.vectorcraft" >/dev/null
done
$T/pc combine "$PWD/board1.pdf" "$PWD/board2.pdf" "$PWD/board3.pdf" "$PWD/board4.pdf" --out "$PWD/boards.pdf"
rm -f board[1-4].pdf
echo "listo: boards.pdf + board1..4.vectorcraft"
