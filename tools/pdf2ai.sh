#!/bin/sh
# Uso: pdf2ai.sh ENTRADA.pdf SALIDA.ai — .ai para Illustrator (una mesa de trabajo por página),
# con el texto trazado para que no haga falta tener las fuentes en el otro ordenador.
set -e
T="$(cd "$(dirname "$0")" && pwd)"
"$T/vc" run --in "$(realpath "$1")" --cmd select.all --cmd type.createOutlines --export "$(realpath -m "$2")" >/dev/null
echo "listo: $2"
