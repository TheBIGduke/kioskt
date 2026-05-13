#!/bin/bash
# Created by Kaléin Tamaríz

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
if [[ "$SCRIPT_DIR" == */deploy ]]; then
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
else
    PROJECT_ROOT="$SCRIPT_DIR"
fi

cd "$PROJECT_ROOT" || exit 1

APP_NAME=$(basename "$PROJECT_ROOT")
PORT_FILE="$PROJECT_ROOT/port.txt"
if [ -f "$PORT_FILE" ]; then
    PORT=$(tr -d '[:space:]' <"$PORT_FILE")
else
    PORT=$(python3 -c "import hashlib, sys; n=sys.argv[1]; print(3000 + (int(hashlib.md5(n.encode()).hexdigest(), 16) % 5000))" "$APP_NAME")
fi

echo "Starting $APP_NAME web server on port $PORT"
exec python3 -m http.server "$PORT"
