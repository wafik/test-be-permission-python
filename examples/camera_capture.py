"""Example: capture a snapshot from the camera (and optionally a live preview).

Run with:
    make camera                 # save a snapshot to out/snapshot.jpg
    make camera-preview         # show a live preview window for 5 seconds
"""

from __future__ import annotations

import argparse

from devices import camera

OUTPUT = "out/snapshot.jpg"


def main() -> None:
    parser = argparse.ArgumentParser(description="Capture from the camera")
    parser.add_argument("--index", type=int, default=0, help="camera index")
    parser.add_argument("--preview", type=float, default=0.0,
                        help="seconds of live preview (0 = snapshot only)")
    args = parser.parse_args()

    if args.preview > 0:
        print(f"Showing {args.preview}s live preview (press q to quit early)...")
        frames = camera.preview(args.preview, args.index)
        print(f"Displayed {frames} frames.")
    else:
        print("Capturing snapshot...")
        path = camera.snapshot(OUTPUT, args.index)
        print(f"Saved snapshot to {path}")


if __name__ == "__main__":
    main()
