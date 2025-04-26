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
