#!/bin/bash

echo "Starting Kiosk Hub..."
cd ~/kioskt || exit

# Run the python module in the background
python3 hub_backend.py &

# --- CONFIGURATION ---
APP_URL="http://localhost:8000"
SCREEN_X=0
SCREEN_Y=800

# Create a temporary profile directory to prevent conflicts with other Chrome windows
USER_DATA_DIR="/tmp/kiosk_profile_$(date +%s)"
mkdir -p "$USER_DATA_DIR"

# Wait briefly to ensure the server starts
sleep 5

echo "Opening Kiosk Mode..."
chromium-browser --kiosk \
    --user-data-dir="$USER_DATA_DIR" \
    --window-position=$SCREEN_X,$SCREEN_Y \
    --no-first-run \
    --disable-features=TranslateUI \
    --use-fake-ui-for-media-stream \
    --app="$APP_URL"