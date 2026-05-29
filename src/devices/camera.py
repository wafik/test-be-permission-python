"""Reusable camera capture helpers.

Thin wrappers around OpenCV (``cv2``) so example scripts and backend code can
grab snapshots or short previews without repeating boilerplate.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import cv2


class CameraError(RuntimeError):
    """Raised when the camera cannot be opened or read."""


def _open(camera_index: int, warmup: float) -> "cv2.VideoCapture":
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise CameraError(f"Could not open camera index {camera_index}")
    # Let auto-exposure / white balance settle before the first read.
    if warmup > 0:
        time.sleep(warmup)
    return cap


def capture_frame(camera_index: int = 0, *, warmup: float = 0.5):
    """Capture a single frame (BGR NumPy array) from the camera."""
    cap = _open(camera_index, warmup)
    try:
        ok, frame = cap.read()
        if not ok or frame is None:
            raise CameraError("Failed to read a frame from the camera")
        return frame
    finally:
        cap.release()


def snapshot(
    path: str | Path,
    camera_index: int = 0,
    *,
    warmup: float = 0.5,
) -> Path:
    """Capture a single frame and save it to ``path``."""
    frame = capture_frame(camera_index, warmup=warmup)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(out), frame):
        raise CameraError(f"Failed to write image to {out}")
    return out


def preview(
    seconds: float,
    camera_index: int = 0,
    *,
    window_name: str = "camera preview (press q to quit)",
    warmup: float = 0.5,
) -> int:
    """Show a live preview window for ``seconds``. Returns the frame count."""
    cap = _open(camera_index, warmup)
    frames = 0
    deadline = time.time() + seconds
    try:
        while time.time() < deadline:
            ok, frame = cap.read()
            if not ok:
                break
            frames += 1
            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return frames


def list_cameras(max_index: int = 5) -> list[int]:
    """Probe camera indices ``0..max_index`` and return the ones that open."""
    available: list[int] = []
    for idx in range(max_index + 1):
        cap = cv2.VideoCapture(idx)
        if cap.isOpened():
            available.append(idx)
        cap.release()
    return available
