"""Genera audio/<id>.wav para cada segmento activado de voice.toml con Kokoro (local, en-gb)
y escribe audio/playlist.txt en el orden del archivo. Solo regenera lo que cambió.
Uso: .venv/bin/python build.py [--all]   (--all genera también los desactivados)"""
import hashlib
import json
import os
import re
import sys
import tomllib

import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(DIR, "audio")
MODEL = os.path.join(DIR, "models", "kokoro-v1.0.int8.onnx")
VOICES = os.path.join(DIR, "models", "voices-v1.0.bin")


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if s]


def main():
    with open(os.path.join(DIR, "voice.toml"), "rb") as f:
        cfg = tomllib.load(f)
    v = cfg["voice"]
    ids = [s["id"] for s in cfg["segment"]]
    assert len(ids) == len(set(ids)), "hay id repetidos en voice.toml"
    assert abs(sum(v["blend"].values()) - 1) < 1e-6, "los pesos de blend deben sumar 1"

    k = Kokoro(MODEL, VOICES)
    style = sum(k.get_voice_style(name) * w for name, w in v["blend"].items())
    os.makedirs(AUDIO, exist_ok=True)
    cache_path = os.path.join(AUDIO, "cache.json")
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}

    todo = [s for s in cfg["segment"] if s.get("enabled") or "--all" in sys.argv]
    for seg in todo:
        key = hashlib.sha1(json.dumps([seg["text"], v], sort_keys=True).encode()).hexdigest()
        out = os.path.join(AUDIO, f"{seg['id']}.wav")
        if cache.get(seg["id"]) == key and os.path.exists(out):
            print(f"= {seg['id']}")
            continue
        parts, sr = [], 24000
        for s in sentences(seg["text"]):
            audio, sr = k.create(s, voice=style, speed=v["speed"], lang="en-gb")
            parts += [audio, np.zeros(int(sr * v["pause"]), dtype=audio.dtype)]
        sf.write(out, np.concatenate(parts), sr)
        cache[seg["id"]] = key
        print(f"+ {seg['id']} ({sum(len(p) for p in parts) / sr:.1f} s)")

    json.dump(cache, open(cache_path, "w"), indent=1)
    with open(os.path.join(AUDIO, "playlist.txt"), "w") as f:
        f.write("".join(f"{s['id']}\n" for s in cfg["segment"] if s.get("enabled")))
    print("playlist:", ", ".join(s["id"] for s in cfg["segment"] if s.get("enabled")))


if __name__ == "__main__":
    main()
