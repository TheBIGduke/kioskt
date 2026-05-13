#!/bin/bash
# Created by Kaléin Tamaríz

# Get the script's directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
if [[ "$SCRIPT_DIR" == */deploy ]]; then
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
else
    PROJECT_ROOT="$SCRIPT_DIR"
fi

# Always run from the project root
cd "$PROJECT_ROOT" || exit 1

APP_NAME=$(basename "$PROJECT_ROOT")

# Resolve port using the same convention as the other kiosk apps:
#   1. Use port.txt if present (manual override, also read by the hub).
#   2. Otherwise derive a stable port from the app folder name with the same
#      md5(name) -> 3000 + (hash % 5000) formula the hub uses, so the value
#      always matches what the kiosk launches the iframe against.
PORT_FILE="$PROJECT_ROOT/port.txt"
if [ -f "$PORT_FILE" ]; then
    PORT=$(tr -d '[:space:]' < "$PORT_FILE")
else
    PORT=$(python3 -c "import hashlib, sys; n=sys.argv[1]; print(3000 + (int(hashlib.md5(n.encode()).hexdigest(), 16) % 5000))" "$APP_NAME")
fi

echo "Starting $APP_NAME on port $PORT"

# Check common virtual environment locations relative to PROJECT_ROOT
if [ -f ".venv/bin/activate" ]; then
    VENV_PATH=".venv/bin/activate"
elif [ -f "backend/.venv/bin/activate" ]; then
    VENV_PATH="backend/.venv/bin/activate"
elif [ -f "../../.venv/bin/activate" ]; then
    VENV_PATH="../../.venv/bin/activate"
else
    VENV_PATH=""
fi

if [ -n "$VENV_PATH" ]; then
    source "$VENV_PATH"
    echo "Virtual environment activated from $VENV_PATH"
else
    echo "Warning: Virtual environment not found. Attempting to run without it."
fi

# Run the FastAPI server from the backend directory
cd backend || exit 1
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
