#!/usr/bin/env bash

SCRIPT_DIR="/home/$USER/productsandsurveys_catalog/"
BACKEND_DIR="${SCRIPT_DIR}/backend"

source "${BACKEND_DIR}/.venv/bin/activate"
cd "${BACKEND_DIR}"

uvicorn main:app --host 0.0.0.0 --port 9999 &
sleep 2

USER_DATA_DIR="/tmp/kiosk_profile_$(date +%s)"
mkdir -p "$USER_DATA_DIR"

exec chromium-browser --kiosk \
  --user-data-dir="$USER_DATA_DIR" \
  --no-first-run \
  --disable-features=TranslateUI \
  --app="http://localhost:9999/"
