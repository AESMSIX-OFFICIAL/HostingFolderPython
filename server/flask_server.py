import sys
from pathlib import Path
import os
script_dir = Path(__file__).parent.resolve()
project_root = script_dir.parent.resolve()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from flask import Flask, render_template_string, send_from_directory, request, abort
import threading # Needed for server's internal IP logging set
from common.file_utils import get_blocked_ips, get_connected_ips, clear_connected_ips_log
import config
script_dir_server = Path(__file__).parent.resolve() # This is the 'server' directory
project_root_server = script_dir_server.parent.resolve() # This is the project root

folder_name = os.environ.get(config.FOLDER_ENV_VAR, config.DEFAULT_FOLDER_NAME)
if folder_name == config.DEFAULT_FOLDER_NAME:
    FILE_DIR = (project_root_server / folder_name).resolve()
else:
    FILE_DIR = (config.BASE_DIR / folder_name).resolve()
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
config.CONNECTED_IPS_LOG_PATH.touch(exist_ok=True)
config.BLOCKED_IPS_FILE_PATH.touch(exist_ok=True)
if not FILE_DIR.exists() and folder_name == config.DEFAULT_FOLDER_NAME:
    try:
        FILE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created default directory: {FILE_DIR}", file=sys.stderr)
    except OSError as e:
        print(f"Error creating default directory {FILE_DIR}: {e}. Exiting.", file=sys.stderr)
        sys.exit(1) # Exit if default creation fails

if not FILE_DIR.is_dir():
   print(f"Error: Specified FILE_DIR '{FILE_DIR}' does not exist or is not a directory. Exiting.", file=sys.stderr)
   sys.exit(1)


print(f"Flask server attempting to serve files from: {FILE_DIR}", file=sys.stderr)

app = Flask(__name__)
logged_ips_session = set()
ip_log_lock = threading.Lock() # Protect access to logged_ips_session and the log file append

def server_log_ip(ip_address):
    """Logs unique IP addresses *for this server instance's session* to a file."""
    with ip_log_lock:
        if ip_address not in logged_ips_session:
            logged_ips_session.add(ip_address)
            try:
                with open(config.CONNECTED_IPS_LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(f"{ip_address}\n")
            except Exception as e:
                print(f"Error writing to IP log {config.CONNECTED_IPS_LOG_PATH}: {e}", file=sys.stderr)


@app.before_request
def check_blocklist_and_log_ip():
    """Check if IP is blocked before processing any request and log access."""
    client_ip = request.remote_addr
    server_log_ip(client_ip) # Log the IP
    blocked_ips = get_blocked_ips(config.BLOCKED_IPS_FILE_PATH)
    if client_ip in blocked_ips:
        print(f"Blocked access attempt from: {client_ip}", file=sys.stderr)
        abort(403)
html_template_path = script_dir_server / "main.html" # Path relatif terhadap skrip server
html_template = "" # Default empty in case of read error

if not html_template_path.is_file():
    print(f"Error: Required HTML template not found at {html_template_path}. Cannot start server.", file=sys.stderr)
    sys.exit(1) # Penting: Exit jika template utama tidak ditemukan

try:
    with open(html_template_path, "r", encoding="utf-8") as f:
        html_template = f.read()
        print(f"Using HTML template from {html_template_path}", file=sys.stderr)
except Exception as e:
    print(f"Error reading HTML template {html_template_path}: {e}. Cannot start server.", file=sys.stderr)
    sys.exit(1) # Exit jika gagal membaca template utama
@app.route('/')
def index():
    try:
        files = [f for f in os.listdir(FILE_DIR) if (FILE_DIR / f).is_file()]
        return render_template_string(html_template, files=files)
    except FileNotFoundError:
         print(f"Error: Served directory '{FILE_DIR}' not found during request.", file=sys.stderr)
         return "Error: Served directory not found.", 500
    except Exception as e:
        print(f"Error listing files in '{FILE_DIR}': {e}", file=sys.stderr)
        return "Error listing files.", 500

@app.route('/open/<path:filename>')
def open_file(filename):
    try:
        requested_path = (FILE_DIR / filename).resolve()
        if not requested_path.is_file() or not requested_path.is_relative_to(FILE_DIR):
            print(f"Attempt to access non-existent or outside file: {filename} resolved to {requested_path}", file=sys.stderr)
            abort(404) # Not Found

        return send_from_directory(FILE_DIR, filename, as_attachment=False)
    except FileNotFoundError:
         abort(404)
    except Exception as e:
        print(f"Error sending file {filename} for opening: {e}", file=sys.stderr)
        abort(500)

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        requested_path = (FILE_DIR / filename).resolve()
        if not requested_path.is_file() or not requested_path.is_relative_to(FILE_DIR):
             print(f"Attempt to access non-existent or outside file: {filename} resolved to {requested_path}", file=sys.stderr)
             abort(404) # Not Found

        return send_from_directory(FILE_DIR, filename, as_attachment=True)
    except FileNotFoundError:
         abort(404)
    except Exception as e:
        print(f"Error sending file {filename} for download: {e}", file=sys.stderr)
        abort(500)

@app.route('/style.css') # Ubah route dari /web.css menjadi /style.css
def serve_css():
    css_path = script_dir_server / 'style.css'
    if css_path.is_file():
         print(f"Serving CSS from {css_path}", file=sys.stderr)
         return send_from_directory(script_dir_server, 'style.css')
    else:
         print(f"Error: CSS file not found at {css_path}", file=sys.stderr)
         abort(404)
if __name__ == '__main__':
    clear_connected_ips_log(config.CONNECTED_IPS_LOG_PATH)
    logged_ips_session.clear() # Clear internal set too

    print(f"Starting Flask server on http://{config.SERVER_HOST}:{config.SERVER_PORT}", file=sys.stderr)
    app.run(host=config.SERVER_HOST, port=config.SERVER_PORT, debug=False)