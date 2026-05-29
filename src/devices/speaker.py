"""Reusable speaker playback helpers.

Thin wrappers around ``sounddevice`` / ``soundfile`` for playing audio either
from a file on disk or from an in-memory NumPy array.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf


def play_array(
    audio: np.ndarray,
    sample_rate: int,
    *,
    device: Optional[int] = None,
    blocking: bool = True,
) -> None:
    """Play an in-memory audio buffer through the speaker."""
    sd.play(audio, samplerate=sample_rate, device=device)
    if blocking:
        sd.wait()


def play_file(
    path: str | Path,
    *,
    device: Optional[int] = None,
    blocking: bool = True,
) -> None:
    """Play an audio file (wav, flac, ogg, mp3 via libsndfile) through the speaker."""
    src = Path(path)
    if not src.exists():
        raise FileNotFoundError(src)

    audio, sample_rate = sf.read(src, dtype="float32")
    play_array(audio, sample_rate, device=device, blocking=blocking)


def list_output_devices() -> list[dict]:
    """Return metadata for every device that can play audio."""
    devices = sd.query_devices()
    return [
        {"index": idx, "name": dev["name"], "channels": dev["max_output_channels"]}
        for idx, dev in enumerate(devices)
        if dev["max_output_channels"] > 0
    ]
