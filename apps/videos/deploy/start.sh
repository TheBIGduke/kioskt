#!/bin/bash
# Serve the Videos app via server.py (provides /api/media endpoint + static file serving).
# Port is derived from the app folder name to match hub_backend.py logic.
APP_NAME="videos"
PORT=$(python3 -c "import hashlib; h=int(hashlib.md5('${APP_NAME}'.encode()).hexdigest(),16); print(3000 + (h % 5000))")

cd "$(dirname "$0")/.."
exec python3 server.py "$PORT"
