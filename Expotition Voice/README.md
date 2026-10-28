# Expotition Voice

Voz británica cálida (Kokoro local, `bf_emma` + `bf_isabella`, en-gb) que explica partes de la cartelera.

1. Edita `voice.toml`: pon `enabled = true` en los segmentos que quieres que explique (el orden del archivo es el orden de reproducción). Puedes cambiar el texto, la mezcla de voces y la velocidad.
2. Ejecuta `./build.sh` (la primera vez crea `.venv` y descarga el modelo, ~115 MB). Solo regenera lo que cambió.
3. Durante la expo:

| Atajo | Acción |
|---|---|
| `Mod+Alt+→` | siguiente segmento |
| `Mod+Alt+←` | repetir el último |
| `Mod+Alt+↓` | parar |
| `Mod+Alt+↑` | volver al principio |
| `Mod+Alt+1…9` | segmento n de la lista |

Sin atajos: `./play.sh next`, `./play.sh kernel`, `./play.sh stop`.
Los atajos están en `expo-voice.kdl`, incluido desde `~/.config/niri/config.d/90-user-extra.kdl`.
