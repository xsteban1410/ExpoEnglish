#!/bin/sh
# Uso: svg2pdf.sh SALIDA.pdf a.svg [b.svg …]
# Cada SVG → .vectorcraft editable (VectorCraft) y una página PDF; PdfCraft las une en SALIDA.pdf.
set -e
T="$(cd "$(dirname "$0")" && pwd)"
out="$(realpath -m "$1")"; shift
for svg; do   # la lista se expande antes del bucle: se puede reemplazar "$@" por las páginas
  svg="$(realpath "$svg")"; base="${svg%.svg}"
  "$T/vc" convert "$svg" "$base.vectorcraft" >/dev/null
  "$T/vc" convert "$svg" "$base.page.pdf" >/dev/null
  shift; set -- "$@" "$base.page.pdf"
done
"$T/pc" combine "$@" --out "$out" >/dev/null
rm -f "$@"
echo "listo: $out"
