# Device Access Demo

Reusable Python examples for accessing the **microphone**, **speaker**, and
**camera** directly from the backend on the local machine. Managed with
[`uv`](https://docs.astral.sh/uv/) and run via `make`.

The device logic lives in a small, importable `devices` package. The scripts in
`examples/` are thin CLI wrappers over it, so you can reuse the helpers anywhere.

## Requirements

- [`uv`](https://docs.astral.sh/uv/) (installs and manages Python + deps)
- `make`
- A microphone, speaker, and camera (macOS / Linux / Windows)

Dependencies (installed automatically by `make setup`): `sounddevice`,
`soundfile`, `numpy`, `opencv-python`.

## Layout

```
src/devices/        reusable, importable helpers (no script boilerplate)
  microphone.py     record(), record_to_file(), list_input_devices()
  speaker.py        play_file(), play_array(), list_output_devices()
  camera.py         snapshot(), capture_frame(), preview(), list_cameras()
  cli.py            `python -m devices.cli` lists all devices
examples/           thin runnable scripts that use the helpers
  mic_record.py     record from the mic, then play it back
  speaker_play.py   play an audio file through the speaker
  camera_capture.py snapshot to disk, or a live preview window
Makefile            run targets
pyproject.toml      uv project + dependencies
example_audio.mp3   sample file used by `make speaker`
```

## Setup

```bash
make setup        # uv sync — creates the venv and installs deps
```

## Usage

| Command | What it does |
| --- | --- |
| `make devices` | List available mic / speaker / camera devices |
| `make mic` | Record 3s from the mic, then play it back |
| `make speaker` | Play `example_audio.mp3` through the speaker |
| `make camera` | Capture a snapshot to `out/snapshot.jpg` |
| `make camera-preview` | Show a live camera preview window for 3s |
| `make clean` | Remove generated output (`out/`) |

### Variables

Override on the command line:

```bash
make mic SECONDS=5                      # record 5s instead of 3
make speaker FILE=out/mic_recording.wav # play a different file
make camera INDEX=1                     # use camera index 1
make camera-preview SECONDS=10          # 10s preview
```

| Variable | Default | Used by |
| --- | --- | --- |
| `SECONDS` | `3` | `mic`, `camera-preview` |
| `FILE` | `example_audio.mp3` | `speaker` |
| `INDEX` | `0` | `camera`, `camera-preview` |

Generated files (recordings, snapshots) are written to `out/`.

## Permissions

The OS gates device access. The **first** time a script touches a device, the
system prompts for permission.

**macOS** — if you denied it earlier, enable it under:

- System Settings → Privacy & Security → **Microphone**
- System Settings → Privacy & Security → **Camera**

Grant access to your terminal app (Terminal / iTerm). Speaker output needs no
permission.

## Reuse in your own code

```python
from devices import microphone, speaker, camera

# microphone
audio = microphone.record(seconds=2)                 # numpy array (frames, channels)
microphone.record_to_file("out/clip.wav", seconds=2) # record straight to a file

# speaker
speaker.play_array(audio, sample_rate=44100)
speaker.play_file("example_audio.mp3")

# camera
frame = camera.capture_frame(camera_index=0)         # BGR numpy array
camera.snapshot("out/photo.jpg")                     # capture + save
camera.preview(seconds=5)                            # live window, q to quit

# enumeration
microphone.list_input_devices()
speaker.list_output_devices()
camera.list_cameras()
```

Every helper takes an optional `device` / `camera_index` argument so you can
target a specific device by the index shown in `make devices`.

## Troubleshooting

- **Camera snapshot is slow (~15-30s) the first time.** macOS avfoundation
  cold-starts the device; subsequent runs are fast.
- **`OpenCV: not authorized to capture video`.** Grant camera permission (see
  [Permissions](#permissions)), then re-run.
- **No audio devices listed.** Confirm the device is connected and not in
  exclusive use by another app, then re-run `make devices`.
