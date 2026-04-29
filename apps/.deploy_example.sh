#!/bin/bash
# Created by Kaléin Tamaríz

# The hub_backend.py dynamically assigns a port based on a hash of the folder name ("Slot Machine")
PORT=$(python3 -c "import hashlib; print(3000 + (int(hashlib.md5(b'Slot Machine').hexdigest(), 16) % 5000))")

echo "Starting Slot Machine web server on port $PORT"
python3 -m http.server $PORT
