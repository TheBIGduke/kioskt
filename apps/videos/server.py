#!/usr/bin/env python3
"""
Videos app server - serves static files and provides a /api/media endpoint
that lists all video files in the media/ directory.
"""

import os
import json
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "media")
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mkv", ".avi", ".mov", ".m4v"}

# Ensure the media folder exists
os.makedirs(MEDIA_DIR, exist_ok=True)

class VideosHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/media":
            self.send_media_list()
        else:
            super().do_GET()

    def send_media_list(self):
        try:
            files = []
            if os.path.isdir(MEDIA_DIR):
                for name in sorted(os.listdir(MEDIA_DIR)):
                    ext = os.path.splitext(name)[1].lower()
                    if ext in VIDEO_EXTENSIONS:
                        files.append(f"media/{name}")
            body = json.dumps(files).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_error(500, str(e))

    def log_message(self, format, *args):
        pass  # silence request logs

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    server = HTTPServer(("0.0.0.0", port), VideosHandler)
    print(f"Videos server running on port {port}", flush=True)
    server.serve_forever()
