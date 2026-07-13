#!/bin/bash
# Double-click this file in Finder to build and preview the portfolio site.
# It opens http://localhost:8000 in your browser. Close the Terminal window to stop.

# Move to the folder this script lives in, so it works no matter where it's launched from.
cd "$(dirname "$0")" || exit 1

# First-time setup: create the virtual environment if it's missing.
if [ ! -x ".venv/bin/python" ]; then
  echo "→ First run: setting up (this happens only once)…"
  python3 -m venv .venv || { echo "Could not create .venv. Is Python 3 installed?"; exit 1; }
  .venv/bin/pip install -r requirements.txt || { echo "Could not install dependencies."; exit 1; }
fi

# Open the site in the default browser a moment after the server starts.
( sleep 2; open "http://localhost:8000" ) &

# Build and serve.
.venv/bin/python generate.py --serve
