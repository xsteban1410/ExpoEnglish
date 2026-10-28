#!/bin/sh
# Reproduce la voz de la exposición. Pensado para atajos de teclado (niri).
#   play.sh next     siguiente segmento de la lista (audio/playlist.txt)
#   play.sh repeat   repite el último
#   play.sh N        segmento N de la lista (1, 2, 3…)
#   play.sh ID       segmento por id (p. ej. kernel)
#   play.sh stop     para el audio
#   play.sh reset    vuelve al principio de la lista
DIR="$(cd "$(dirname "$0")" && pwd)"
LIST="$DIR/audio/playlist.txt"
RUN="${XDG_RUNTIME_DIR:-/tmp}/expo-voice"
mkdir -p "$RUN"
POS="$RUN/pos"; PID="$RUN/pid"

stop() { [ -f "$PID" ] && kill "$(cat "$PID")" 2>/dev/null; rm -f "$PID"; }
nth() { sed -n "${1}p" "$LIST"; }
count() { grep -c . "$LIST"; }
pos() { cat "$POS" 2>/dev/null || echo 0; }

play_id() {
  f="$DIR/audio/$1.wav"
  [ -f "$f" ] || { notify-send -a "Expo Voice" "No existe audio/$1.wav" "Ejecuta ./build.sh" 2>/dev/null; exit 1; }
  stop
  notify-send -a "Expo Voice" -t 2500 "▶ $1" 2>/dev/null
  pw-play "$f" & echo $! > "$PID"
}

case "${1:-next}" in
  stop)   stop ;;
  reset)  stop; echo 0 > "$POS" ;;
  next)   n=$(( $(pos) + 1 )); [ "$n" -gt "$(count)" ] && n=1
          echo "$n" > "$POS"; play_id "$(nth "$n")" ;;
  repeat) n=$(pos); [ "$n" -lt 1 ] && n=1; play_id "$(nth "$n")" ;;
  *[!0-9]*) play_id "$1" ;;
  *)      echo "$1" > "$POS"; play_id "$(nth "$1")" ;;
esac
