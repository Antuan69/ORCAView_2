from flask import Flask, send_from_directory
import os

# The static folder is relative to the Flask app's root path.
# Since ketcher_server.py is in 'orcaview', this path becomes 'orcaview/ketcher/standalone'.
# Construct an absolute path to the Ketcher 'standalone' directory to avoid any ambiguity.
_current_dir = os.path.dirname(os.path.abspath(__file__))
_static_folder = os.path.join(_current_dir, 'ketcher', 'standalone')

app = Flask(__name__, static_folder=_static_folder, static_url_path='')

@app.route('/')
def index():
    """Serves the main index.html file."""
    return send_from_directory(app.static_folder, 'index.html')

def run_server():
    print(f"[Ketcher Server] Serving files from: {app.static_folder}")
    if not os.path.exists(os.path.join(app.static_folder, 'index.html')):
        print("[Ketcher Server] ERROR: index.html not found at the specified path!")
        return
    
    # Run the server with debugging enabled. The reloader is disabled as it can cause issues in a threaded app.
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)

if __name__ == '__main__':
    run_server()
