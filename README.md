# 📁 Local File Server with GUI Control

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/framework-Flask-blue.svg)](https://flask.palletsprojects.com/)
[![GUI Library](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen.svg)](https://customtkinter.tomschimansky.com/)
[![System Info](https://img.shields.io/badge/system-psutil-orange.svg)](https://psutil.readthedocs.io/)
A simple local file server application built with Python, Flask, and CustomTkinter GUI. It allows you to serve files from a chosen directory on your local network, control the server via a graphical interface, monitor connections, and block unwanted IP addresses.

## ✨ Features

* **Serve Files:** Host files over HTTP from any specified directory.
* **GUI Control:** Start and stop the Flask server directly from the intuitive CustomTkinter GUI.
* **Change Directory:** Easily change the directory being served via the GUI.
* **Web Interface:** Clients can browse and download files via a simple web page.
* **Connection Logging:** Log the IP addresses of clients who access the server (since the server was last started by the GUI).
* **IP Blocking:** Block specific IP addresses from accessing the server directly from the GUI. Blocked IPs are saved persistently.
* **Network Monitoring:** View system-wide network send/receive traffic in the GUI.
* **Server Log Output:** See the raw output (stdout/stderr) from the Flask server process within the GUI.
* **Remember Last Folder:** The application remembers the last served folder when you reopen the GUI.
* **Basic Security:** Implements path traversal protection to prevent clients from accessing files outside the served directory.

## 🚀 Getting Started

### Prerequisites

Make sure you have Python 3.8 or higher installed on your system. You will also need the following Python libraries:

* `Flask`
* `customtkinter`
* `psutil`

You can install them using pip:
pip install Flask customtkinter psutil


📂 Project Structure
your_project_folder/
├── main.py               # Entry point for the application
├── config.py             # Global configuration constants and paths
├── common/               # Utility functions
│   └── file_utils.py     # Functions for handling log and setting files
├── server/               # Flask server code and web files
│   ├── flask_server.py   # The Flask application definition and routes
│   ├── main.html         # HTML template for the web interface
│   └── style.css         # CSS for the web interface
├── core/                 # Core application logic
│   └── server_manager.py # Manages the Flask server subprocess
└── gui/                  # CustomTkinter GUI code
    ├── app.py            # Main CustomTkinter application class
    └── frames/           # Individual GUI components (CTkFrame subclasses)
        ├── __init__.py   # Makes 'frames' a Python package
        ├── status_frame.py # Frame for server status and folder selection
        ├── stats_frame.py  # Frame for network statistics display
        ├── device_frame.py # Frame for connected/blocked IP list and controls
        └── log_frame.py    # Frame for displaying server log output

🏗️ Architecture

The application follows a modular architecture:

    main.py starts the gui/app.py.
    gui/app.py is the main CustomTkinter application window. It initializes the core/server_manager.py and the various GUI frames (gui/frames/).
    core/server_manager.py is responsible for starting and stopping the server/flask_server.py as a separate subprocess using subprocess.Popen. It captures the server's standard output and standard error using threads and puts them into a queue. It also tracks the server's process status.
    The GUI (gui/app.py and its frames) communicates with the ServerManager. The GUI's main loop uses self.after to periodically update the UI by polling the ServerManager's status, processing the log queue, and reading data from the log/block files managed by common/file_utils.py.
    server/flask_server.py is a standalone Flask application. When run by the ServerManager, it receives the served folder path via an environment variable. It handles web requests, lists files from the specified directory, serves files, and checks/updates the shared log (connected_ips.log) and blocklist (blocked_ips.txt) files in the logs/ directory using functions from common/file_utils.py. It also incorporates path traversal protection.
    common/file_utils.py provides simple functions to read from and write to the .log and .txt files in the logs/ directory, used by both the server and the GUI to share persistent data (connected IPs, blocked IPs, last served folder).
    config.py centralizes constants used across different modules.

This separation of concerns allows the GUI to remain responsive while the server runs in a separate process, and makes the code more organized and maintainable.
