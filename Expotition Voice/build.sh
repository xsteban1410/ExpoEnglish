#!/bin/sh
# Prepara el entorno (una vez) y regenera los audios desde voice.toml.
set -e
cd "$(dirname "$0")"
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -x .venv/bin/python ] || { uv venv -q .venv && uv pip install -q -p .venv/bin/python kokoro-onnx soundfile; }
mkdir -p models
for f in kokoro-v1.0.int8.onnx voices-v1.0.bin; do
  if [ ! -f "models/$f" ]; then
    curl -fL --progress-bar -o "models/$f.part" "$REL/$f"
    mv "models/$f.part" "models/$f"
  fi
done
.venv/bin/python build.py "$@"
