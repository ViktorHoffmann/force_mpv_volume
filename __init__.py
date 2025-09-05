# __init__.py — Force Pulse/PA sink-input volume for Anki's mpv TTS
# Works by running `pactl` right after playback starts.

import re
import subprocess
from aqt import gui_hooks
from aqt.qt import QTimer

# Change this if you want a different target volume
TARGET_VOL = "100%"

def _set_sink_input_volume():
    try:
        # List all sink inputs
        out = subprocess.run(
            ["pactl", "list", "sink-inputs"],
            check=True, text=True, capture_output=True
        ).stdout

        # Split into blocks: ["<id1>", "<block1>", "<id2>", "<block2>", ...]
        parts = re.split(r"Sink Input #(\d+)\n", out)[1:]
        # Pick the most recent mpv-based input we can find
        idx_to_set = None
        for i in range(0, len(parts), 2):
            idx = parts[i].strip()
            block = parts[i+1]

            # Match on mpv; Anki uses mpv for playback on Linux
            if (re.search(r'application\.process\.binary = "mpv"', block)
                or re.search(r'application\.name = "mpv"', block, re.IGNORECASE)
                or re.search(r'media\.name = "mpv"', block)):
                idx_to_set = idx  # keep last match (most recent entry)
        if not idx_to_set:
            return

        # Ensure unmuted + set volume
        subprocess.run(["pactl", "set-sink-input-mute", idx_to_set, "0"], check=False)
        subprocess.run(["pactl", "set-sink-input-volume", idx_to_set, TARGET_VOL], check=False)

        # Give the stream a unique identity + non-music role so pulse remembers a separate volume
        # (These commands are best-effort; ignore errors if unsupported.)
        subprocess.run(
            ["pactl", "update-sink-input-proplist", idx_to_set, "application.name=Anki TTS"],
            check=False
        )
        subprocess.run(
            ["pactl", "update-sink-input-proplist", idx_to_set, "media.role=event"],
            check=False
        )

    except Exception as e:
        print(f"[force_tts_sink_volume] pactl error: {e}")

def _on_begin_playback(player, *args, **kwargs):
    # Run a few attempts shortly after playback begins,
    # because the sink-input may appear a moment later.
    for ms in (30, 120, 300):
        QTimer.singleShot(ms, _set_sink_input_volume)

# Hook: when Anki's AV player begins playing
gui_hooks.av_player_did_begin_playing.append(_on_begin_playback)