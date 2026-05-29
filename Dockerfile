# Device Access Demo — container image
#
# NOTE: microphone, speaker, and camera are HOST hardware. Containers cannot
# reach them by default. This image runs the code and `make devices` works, but
# actually capturing/playing media requires passing devices through at runtime
# (see the run examples at the bottom). On macOS/Windows Docker Desktop, host
# audio/camera passthrough is generally NOT supported; use it on Linux hosts.

FROM python:3.12-slim

# System libraries required by OpenCV (libGL/glib) and sounddevice (PortAudio).
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libportaudio2 \
        libsndfile1 \
        make \
    && rm -rf /var/lib/apt/lists/*

# Install uv (copied from the official distroless image).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first for better layer caching.
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev

# Copy the rest of the project.
COPY . .

# Make the devices package importable (matches the Makefile).
ENV PYTHONPATH=/app/src

# Default: list detected devices.
CMD ["uv", "run", "--no-sync", "python", "-m", "devices.cli"]

# --- Run examples -----------------------------------------------------------
# List devices (no hardware needed):
#   docker build -t device-demo .
#   docker run --rm device-demo
#
# Linux host with device passthrough:
#   docker run --rm \
#     --device /dev/snd \
#     --device /dev/video0 \
#     -v "$PWD/out:/app/out" \
#     device-demo uv run --no-sync python examples/camera_capture.py
