"""Example: record from the microphone, then play it back.

Run with:
    make mic            # default 3 seconds
    make mic SECONDS=5  # custom duration
"""

from __future__ import annotations

import argparse

from devices import microphone, speaker

OUTPUT = "out/mic_recording.wav"


def main() -> None:
    parser = argparse.ArgumentParser(description="Record from mic and play it back")
    parser.add_argument("--seconds", type=float, default=3.0)
    parser.add_argument("--device", type=int, default=None, help="input device index")
    parser.add_argument("--no-playback", action="store_true")
    args = parser.parse_args()

    print(f"Recording {args.seconds}s of audio... speak now.")
    path = microphone.record_to_file(
        OUTPUT, args.seconds, device=args.device
    )
    print(f"Saved recording to {path}")

    if not args.no_playback:
        print("Playing it back through the speaker...")
        speaker.play_file(path)
        print("Done.")


if __name__ == "__main__":
    main()
