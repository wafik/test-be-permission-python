"""Reusable microphone capture helpers.

Thin wrappers around ``sounddevice`` so example scripts and other backend
code can record audio without repeating boilerplate.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf

DEFAULT_SAMPLE_RATE = 44_100
DEFAULT_CHANNELS = 1


def record(
    seconds: float,
    *,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    device: Optional[int] = None,
) -> np.ndarray:
    """Record ``seconds`` of audio from the microphone.

    Returns a float32 NumPy array shaped ``(frames, channels)``.
    """
    if seconds <= 0:
        raise ValueError("seconds must be positive")

    frames = int(seconds * sample_rate)
    recording = sd.rec(
        frames,
        samplerate=sample_rate,
        channels=channels,
        dtype="float32",
        device=device,
    )
    sd.wait()  # block until capture finishes
    return recording


def record_to_file(
    path: str | Path,
    seconds: float,
    *,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    device: Optional[int] = None,
) -> Path:
    """Record audio and save it to ``path`` (format inferred from extension)."""
    audio = record(
        seconds,
        sample_rate=sample_rate,
        channels=channels,
        device=device,
    )
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out, audio, sample_rate)
    return out


def list_input_devices() -> list[dict]:
    """Return metadata for every device that can capture audio."""
    devices = sd.query_devices()
    return [
        {"index": idx, "name": dev["name"], "channels": dev["max_input_channels"]}
        for idx, dev in enumerate(devices)
        if dev["max_input_channels"] > 0
    ]
