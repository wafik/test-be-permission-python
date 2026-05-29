"""Example: play an audio file through the speaker.

Run with:
    make speaker                       # plays example_audio.mp3
    make speaker FILE=out/recording.wav
"""

from __future__ import annotations

import argparse

from devices import speaker

DEFAULT_FILE = "example_audio.mp3"


def main() -> None:
    parser = argparse.ArgumentParser(description="Play an audio file on the speaker")
    parser.add_argument("--file", default=DEFAULT_FILE, help="path to audio file")
    parser.add_argument("--device", type=int, default=None, help="output device index")
    args = parser.parse_args()

    print(f"Playing {args.file} ...")
    speaker.play_file(args.file, device=args.device)
    print("Done.")


if __name__ == "__main__":
    main()
