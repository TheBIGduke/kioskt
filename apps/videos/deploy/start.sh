#!/bin/bash
PORT=${1:-$(python3 -c "import hashlib; h=int(hashlib.md5(b'videos').hexdigest(),16); print(3000 + (h % 5000))")}
cd "$(dirname "$0")/.."
exec python3 server.py "$PORT"
