"""Small CLI to list available audio and video devices."""

from __future__ import annotations

from . import camera, microphone, speaker


def list_all() -> None:
    print("== Microphones (input) ==")
    for dev in microphone.list_input_devices():
        print(f"  [{dev['index']}] {dev['name']} ({dev['channels']} ch)")

    print("\n== Speakers (output) ==")
    for dev in speaker.list_output_devices():
        print(f"  [{dev['index']}] {dev['name']} ({dev['channels']} ch)")

    print("\n== Cameras ==")
    cams = camera.list_cameras()
    if cams:
        for idx in cams:
            print(f"  [{idx}] camera available")
    else:
        print("  (none detected)")


if __name__ == "__main__":
    list_all()
