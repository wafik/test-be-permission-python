# Device Access Demo

Reusable Python examples for accessing the **microphone**, **speaker**, and
**camera** directly from the backend on the local machine. Managed with
[`uv`](https://docs.astral.sh/uv/) and run via `make`.

## Layout

```
src/devices/        reusable, importable helpers (no script boilerplate)
  microphone.py     record(), record_to_file(), list_input_devices()
  speaker.py        play_file(), play_array(), list_output_devices()
  camera.py         snapshot(), capture_frame(), preview(), list_cameras()
  cli.py            `python -m devices.cli` lists all devices
examples/           thin runnable scripts that use the helpers
Makefile            run targets
```

## Setup

```bash
make setup        # uv sync — creates the venv and installs deps
```

## Run / test

```bash
make devices                 # list mic / speaker / camera devices
make mic                     # record 3s from mic, then play it back
make mic SECONDS=5           # record 5s instead
make speaker                 # play example_audio.mp3
make speaker FILE=out/mic_recording.wav
make camera                  # save a snapshot to out/snapshot.jpg
make camera-preview          # live preview window for 3s (SECONDS to change)
make clean                   # remove generated output
```

## macOS permissions

The OS gates device access. The **first** time a script touches a device,
macOS prompts for permission. If you denied it earlier, enable it under:

- System Settings → Privacy & Security → **Microphone**
- System Settings → Privacy & Security → **Camera**

Grant access to your terminal app (Terminal / iTerm). Speaker output needs no
permission.

## Reuse in your own code

```python
from devices import microphone, speaker, camera

audio = microphone.record(seconds=2)        # numpy array
speaker.play_array(audio, sample_rate=44100)
camera.snapshot("out/photo.jpg")
```
