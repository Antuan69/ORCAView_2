from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser
import sys

def serve_ketcher():
    """Serve the Ketcher editor locally using a simple HTTP server."""
    # Get the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set the directory to serve from (Ketcher files are in orcaview/ketcher)
    ketcher_dir = os.path.join(script_dir, 'orcaview', 'ketcher')
    
    if not os.path.exists(ketcher_dir):
        print(f"Error: Ketcher directory not found at {ketcher_dir}")
        return
    
    print(f"Serving Ketcher files from: {ketcher_dir}")
    
    # Change to the Ketcher directory
    os.chdir(ketcher_dir)
    
    # Create a simple HTTP server
    server_address = ('', 8000)
    
    # Use the built-in SimpleHTTPRequestHandler
    handler_class = SimpleHTTPRequestHandler
    
    try:
        httpd = HTTPServer(server_address, handler_class)
        print(f"Serving Ketcher editor on http://localhost:{server_address[1]}/")
        
        # Open the browser
        webbrowser.open(f"http://localhost:{server_address[1]}/index.html")
        
        # Start the server
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()
        
    except OSError as e:
        print(f"Error: {e}")
        print("Port 8000 might be in use. Please close any other servers using this port.")
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        httpd.server_close()
        print("Server stopped.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    serve_ketcher()
