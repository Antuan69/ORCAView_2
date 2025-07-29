import os
import sys
from flask import Flask, send_from_directory
import threading

# Add the parent directory to the Python path to allow for relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# The absolute path to the 'jsme' directory
JSME_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def editor():
    return send_from_directory(JSME_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(JSME_DIR, filename)

class JsmeServer(threading.Thread):
    def __init__(self, port=5001):
        super().__init__()
        self.port = port
        self.daemon = True # Allows main thread to exit even if this thread is running

    def run(self):
        # Use a different port to avoid conflicts
        app.run(port=self.port, debug=False)
