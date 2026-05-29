# Device Access Demo — microphone / speaker / camera via Python + uv
#
# Usage:
#   make setup            install dependencies into a uv-managed venv
#   make devices          list available mic / speaker / camera devices
#   make mic              record from mic (SECONDS=3) and play it back
#   make speaker          play an audio file (FILE=example_audio.mp3)
#   make camera           capture a snapshot to out/snapshot.jpg
#   make camera-preview   show a live camera preview window (SECONDS=5)
#   make clean            remove generated output

# Configurable variables (override on the command line, e.g. `make mic SECONDS=5`)
SECONDS ?= 3
FILE    ?= example_audio.mp3
INDEX   ?= 0

UV  := uv
RUN := PYTHONPATH=src $(UV) run python

.PHONY: setup devices mic speaker camera camera-preview clean

setup:
	$(UV) sync

devices:
	$(RUN) -m devices.cli

mic:
	$(RUN) examples/mic_record.py --seconds $(SECONDS)

speaker:
	$(RUN) examples/speaker_play.py --file $(FILE)

camera:
	$(RUN) examples/camera_capture.py --index $(INDEX)

camera-preview:
	$(RUN) examples/camera_capture.py --index $(INDEX) --preview $(SECONDS)

clean:
	rm -rf out
