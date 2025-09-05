# Anki Force MPV Volume (PipeWire/PulseAudio)

This Anki add-on forces all audio playback (such as TTS) to a fixed volume (default: 100%), regardless of the volume of other programs running in the background.

This is especially useful on Linux with PipeWire/PulseAudio, where Anki’s mpv playback can otherwise inherit the volume of applications like Spotify. With this add-on, you can keep Spotify at a lower volume while still hearing Anki’s sounds clearly.

## Installation

1. Download the latest `.ankiaddon` file from the [Releases](https://github.com/ViktorHoffmann/force_mpv_volume/releases) page.
2. In Anki, go to **Tools → Add-ons → Install from file…** and select the downloaded file.
3. Restart Anki.

## Configuration

- The target volume is set inside the source code (`TARGET_VOL` in `__init__.py`).
- Default is `100%`. You can change this to any other valid PulseAudio/PipeWire value, e.g. `120%`.
