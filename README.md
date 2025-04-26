
# 📁 Local File Server with GUI Control

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/framework-Flask-blue.svg)](https://flask.palletsprojects.com/)
[![GUI Library](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen.svg)](https://customtkinter.tomschimansky.com/)
[![System Info](https://img.shields.io/badge/system-psutil-orange.svg)](https://psutil.readthedocs.io/)

A simple local file server application built with Python, Flask, and CustomTkinter GUI. It allows you to serve files from a chosen directory on your local network, control the server via a graphical interface, monitor connections, and block unwanted IP addresses.

## ✨ Features

- **Serve Files:** Host files over HTTP from any specified directory.
- **GUI Control:** Start and stop the Flask server directly from the intuitive CustomTkinter GUI.
- **Change Directory:** Easily change the directory being served via the GUI.
- **Web Interface:** Clients can browse and download files via a simple web page.
- **Connection Logging:** Log the IP addresses of clients who access the server.
- **IP Blocking:** Block specific IP addresses from accessing the server directly from the GUI. Blocked IPs are saved persistently.
- **Network Monitoring:** View system-wide network traffic in the GUI.
- **Server Log Output:** View Flask server stdout/stderr in real-time within the GUI.
- **Remember Last Folder:** Remembers the last served folder upon reopening the application.
- **Basic Security:** Protects against path traversal attacks.

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.8+** installed. Install required libraries:

```bash
pip install Flask customtkinter psutil
```

### Installation

Clone the repository:

```bash
git clone https://github.com/AESMSIX-OFFICIAL/HostingFolderPython
cd HostingFolderPython
```

### Running the Application

```bash
python main.py
```

Steps:
1. GUI window will open.
2. Click **"Turn On Server"** to start.
3. Access via browser: `http://<IP_Lokal>:8000`.

> Find your IP address using `ipconfig` (Windows) or `ifconfig`/`ip a` (Linux/macOS).

## 📂 Project Structure

```
your_project_folder/
├── main.py               # Entry point
├── config.py              # Global configuration
├── common/
│   └── file_utils.py      # Log and settings handler
├── server/
│   ├── flask_server.py    # Flask server logic
│   ├── main.html          # Web UI
│   └── style.css          # Web UI styling
├── core/
│   └── server_manager.py  # Manages server subprocess
└── gui/
    ├── app.py             # Main GUI
    └── frames/
        ├── __init__.py
        ├── status_frame.py
        ├── stats_frame.py
        ├── device_frame.py
        └── log_frame.py
```

## 🏗️ Architecture Overview

- **`main.py`**: Launches the GUI.
- **`gui/app.py`**: Main CustomTkinter app, orchestrates frames and server control.
- **`core/server_manager.py`**: Manages server subprocess and communication.
- **`server/flask_server.py`**: Serves HTTP requests and manages logs/blocklists.
- **`common/file_utils.py`**: Helper functions for file I/O.
- **`config.py`**: Global constants.

The server runs in a separate process to keep the GUI responsive.

## 📸 Screenshots

*(Insert screenshots here)*

- GUI Interface
- Web Browser File Explorer

## 🤝 Contributing

Contributions are welcome!  
Please open an issue or pull request for suggestions, bugs, or improvements.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

Made with ❤️ in Python.
