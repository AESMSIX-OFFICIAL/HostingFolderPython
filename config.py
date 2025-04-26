import os
from pathlib import Path

 
DEFAULT_FOLDER_NAME = "files"
FOLDER_ENV_VAR = 'FLASK_SERVE_FOLDER'
SERVER_PORT = 8000
SERVER_HOST = '0.0.0.0'

 
 
BASE_DIR = Path(__file__).parent.resolve()

 
LOG_DIR_NAME = "logs"
LOG_DIR = BASE_DIR / LOG_DIR_NAME
CONNECTED_IPS_LOG_FILE_NAME = "connected_ips.log"
BLOCKED_IPS_FILE_NAME = "blocked_ips.txt"
CONNECTED_IPS_LOG_PATH = LOG_DIR / CONNECTED_IPS_LOG_FILE_NAME
BLOCKED_IPS_FILE_PATH = LOG_DIR / BLOCKED_IPS_FILE_NAME

 
SERVED_FOLDER_SETTING_FILE_NAME = "served_folder.txt" # <--- File baru
SERVED_FOLDER_SETTING_PATH = LOG_DIR / SERVED_FOLDER_SETTING_FILE_NAME # <--- Jalur file baru

 
DEFAULT_SERVE_PATH = BASE_DIR / DEFAULT_FOLDER_NAME

 
UPDATE_INTERVAL_MS = 1500 # For network stats and device list
LOG_QUEUE_CHECK_INTERVAL_MS = 50 # For processing log messages from server process