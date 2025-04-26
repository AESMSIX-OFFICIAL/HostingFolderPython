import os
from pathlib import Path
import sys
import threading

 
 

def ensure_dirs_exist(log_dir: Path):
    """Ensures log directory exists."""
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
 
    except OSError as e:
        print(f"Error ensuring log directory {log_dir} exists: {e}", file=sys.stderr)
 

def ensure_file_exists(file_path: Path):
    """Ensures a file exists (creates it if necessary)."""
    try:
 
 
        if not file_path.exists():
             file_path.touch()
 
    except OSError as e:
        print(f"Error ensuring file {file_path} exists: {e}", file=sys.stderr)
 


def get_blocked_ips(block_file_path: Path) -> set[str]:
    """Reads the list of blocked IPs from the file."""
    if not block_file_path.is_file():
        return set()
    try:
        with open(block_file_path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip() and not line.strip().startswith('#')) # Ignore comments and empty lines
    except Exception as e:
        print(f"Error reading blocklist file {block_file_path}: {e}", file=sys.stderr)
        return set()

def add_blocked_ip(block_file_path: Path, ip_address: str) -> bool:
    """Adds an IP address to the blocklist file if not already present."""
 
    existing_blocked_ips = get_blocked_ips(block_file_path)
    if ip_address in existing_blocked_ips:
        return False # Already blocked

    try:
        with open(block_file_path, "a", encoding="utf-8") as f:
            f.write(f"{ip_address}\n")
 
        return True
    except Exception as e:
        print(f"Error writing to blocklist file {block_file_path}: {e}", file=sys.stderr)
        return False

def remove_blocked_ip(block_file_path: Path, ip_address: str) -> bool:
    """Removes an IP address from the blocklist file."""
 
    existing_blocked_ips = get_blocked_ips(block_file_path)
    if ip_address not in existing_blocked_ips:
        return False # Not in blocklist

    try:
 
        lines = []
        if block_file_path.is_file():
             with open(block_file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() != ip_address:
                        lines.append(line)

        with open(block_file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
 
        return True
    except Exception as e:
        print(f"Error writing to blocklist file {block_file_path}: {e}", file=sys.stderr)
        return False

def get_connected_ips(log_file_path: Path) -> set[str]:
    """Reads the list of connected IPs from the log file."""
    if not log_file_path.is_file():
        return set()
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
 
             return set(line.strip() for line in f if line.strip())
    except Exception as e:
        print(f"Error reading IP log file {log_file_path}: {e}", file=sys.stderr)
        return set()

def clear_connected_ips_log(log_file_path: Path):
    """Clears the connected IPs log file."""
    try:
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("")
 
    except Exception as e:
        print(f"Warning: Could not clear IP log file {log_file_path}: {e}", file=sys.stderr)

 

def save_served_folder_setting(file_path: Path, folder_path: Path):
    """Saves the specified folder path to a setting file."""
    try:
 
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(folder_path.resolve())) # Simpan jalur absolut
 
    except Exception as e:
        print(f"Error saving served folder setting to {file_path}: {e}", file=sys.stderr)

def load_served_folder_setting(file_path: Path) -> Path | None:
    """Loads the served folder path from a setting file."""
    if not file_path.is_file():
        return None # File doesn't exist yet

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            saved_path_str = f.read().strip() # Baca dan hapus spasi/newline

        if not saved_path_str:
            return None # File kosong

        saved_path = Path(saved_path_str)

 
        if not saved_path.is_dir():
            print(f"Warning: Saved served folder path '{saved_path}' is not a valid directory.", file=sys.stderr)
            return None # Jalur tidak valid

 
        return saved_path # Kembalikan jalur yang dimuat

    except Exception as e:
        print(f"Error loading served folder setting from {file_path}: {e}", file=sys.stderr)
        return None # Tangani error saat membaca