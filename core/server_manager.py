import subprocess
import threading
import time
import queue
import os
import sys
from pathlib import Path
import config
from common import file_utils

class ServerManager:
    def __init__(self, served_folder_path: Path, log_callback=None):
        self._served_folder_path = served_folder_path
        self._log_callback = log_callback # Function to call with new log messages

        self.server_process: subprocess.Popen | None = None
        self.is_running = False # Status internal manager
        self._stop_event = threading.Event() # Untuk menghentikan pipe reader threads
        self._log_queue = queue.Queue() # Antrian untuk pesan log server
        self._stdout_reader_thread: threading.Thread | None = None
        self._stderr_reader_thread: threading.Thread | None = None


    def _log(self, message: str):
        """Helper to send log messages to the callback."""
        if self._log_callback:
            self._log_callback(message)
        else:
            print(message, file=sys.stderr) # Fallback to stderr if no callback

    def start(self):
        if self.is_running:
            self._log("Server is already running.")
            return False

        server_script_path = config.BASE_DIR / "server" / "flask_server.py"
        if not server_script_path.is_file():
            self._log(f"Error: Server script not found at {server_script_path}")
            return False

        self._log("--- Server starting ---")
        file_utils.clear_connected_ips_log(config.CONNECTED_IPS_LOG_PATH)

        try:
            env = os.environ.copy()
            env[config.FOLDER_ENV_VAR] = str(self._served_folder_path)
            server_command = [sys.executable, str(server_script_path)]
            self._log(f"Starting server process: {' '.join(server_command)}")
            self._log(f"Serving folder: {self._served_folder_path}")

            self.server_process = subprocess.Popen(
                server_command,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                cwd=config.BASE_DIR # Set CWD to the base directory for relative paths in server
            )
            self._log(f"Server process started (PID: {self.server_process.pid}).")

            self._stop_event.clear() # Clear stop signal
            self._stdout_reader_thread = threading.Thread(
                target=self._read_pipe_thread,
                args=(self.server_process.stdout, 'stdout', self._log_queue, self._stop_event),
                daemon=True # Allow GUI to exit even if threads are alive
            )
            self._stderr_reader_thread = threading.Thread(
                target=self._read_pipe_thread,
                args=(self.server_process.stderr, 'stderr', self._log_queue, self._stop_event),
                daemon=True
            )

            self._stdout_reader_thread.start()
            self._stderr_reader_thread.start()
            time.sleep(1.0) # Reduced initial wait
            if self.server_process.poll() is not None:
                 exit_code = self.server_process.poll()
                 self._log(f"Server failed to start or exited unexpectedly. Exit Code: {exit_code}")
                 self._cleanup_process_resources() # Clean up resources
                 self.is_running = False # Update internal state
                 return False

            self.is_running = True # Update internal state
            self._log("Server is running.")

            return True

        except Exception as e:
            self._log(f"Error starting server: {e}")
            self._cleanup_process_resources()
            self.is_running = False
            return False

    def stop(self):
        self._stop_process()
        self._cleanup_process_resources() # Clean up resources
        self.is_running = False
        self._log("Server stopped.")

    def _stop_process(self):
        """Attempts to terminate/kill the server subprocess."""
        if self.server_process and self.server_process.poll() is None:
            self._log(f"Attempting to stop server process (PID: {self.server_process.pid})....")
            try:
                self._stop_event.set()
                self.server_process.terminate()
                try:
                    self.server_process.wait(timeout=5) # Wait a few seconds for graceful exit
                    self._log("Server terminated gracefully.")
                except subprocess.TimeoutExpired:
                    self._log("Server did not terminate gracefully, killing...")
                    self.server_process.kill() # Force kill
                    self.server_process.wait() # Wait for kill to complete
                    self._log("Server killed.")
            except Exception as e:
                self._log(f"Error during server process termination: {e}")
        elif self.server_process and self.server_process.poll() is not None:
             self._log(f"Server process was already stopped (Exit Code: {self.server_process.poll()}).")
        else:
             self._log("Server process reference is null or not running.")


    def _cleanup_process_resources(self):
        """Cleans up subprocess and related thread references."""
        self.server_process = None
        self._stdout_reader_thread = None
        self._stderr_reader_thread = None

    def get_status(self) -> str:
        """Returns the current status string (e.g., 'Running', 'Stopped', 'Exited')."""
        if self.server_process is not None and self.server_process.poll() is None:
             return "Running"
        elif self.server_process is not None and self.server_process.poll() is not None:
             return f"Exited ({self.server_process.poll()})"
        else:
             return "Stopped"

    def get_served_folder(self) -> Path:
        """Returns the path to the folder currently configured to be served."""
        return self._served_folder_path

    def set_served_folder(self, folder_path: Path):
        """Sets the folder path to be used the *next* time the server starts."""
        if self.is_running:
             self._log("Cannot change folder while server is running. Stop server first.")
             return False
        if not folder_path.is_dir():
             self._log(f"Error: Selected path is not a valid directory: {folder_path}")
             return False

        self._served_folder_path = folder_path
        self._log(f"Served folder set to: {self._served_folder_path}. Restart server to apply.")
        return True

    def _read_pipe_thread(self, pipe, pipe_name, queue, stop_event):
        """Dedicated thread function to read from a single subprocess pipe."""
        try:
            while not stop_event.is_set():
                 line_bytes = pipe.readline()

                 if not line_bytes:
                     break

                 try:
                     encoding = sys.stderr.encoding if pipe_name == 'stderr' else sys.stdout.encoding
                     line = line_bytes.decode(encoding or 'utf-8', errors='replace').strip()
                     if line:
                         queue.put(f"[{pipe_name.upper()}] {line}")
                 except Exception as decode_error:
                     queue.put(f"[{pipe_name.upper()}] Error decoding line: {decode_error}")

        except ValueError:
             pass
        except Exception as e:
             queue.put(f"[{pipe_name.upper()}] Unexpected error reading pipe: {e}")
        finally:
             try:
                 pipe.close()
             except Exception as e:
                  print(f"Error closing pipe {pipe_name}: {e}", file=sys.stderr)


    def process_log_queue(self):
        """Retrieves and processes messages from the log queue."""
        messages = []
        try:
            while True:
                 message = self._log_queue.get_nowait()
                 messages.append(message)
                 self._log_queue.task_done() # Tandai item sudah diproses
        except queue.Empty:
            pass # Antrian kosong, selesai
        for msg in messages:
            self._log(msg) # Gunakan metode _log yang memanggil callback GUI


    def get_connected_ips_from_log(self) -> set[str]:
        """Reads and returns unique connected IPs from the log file using file_utils."""
        return file_utils.get_connected_ips(config.CONNECTED_IPS_LOG_PATH)

    def shutdown(self):
        """Performs a full shutdown sequence."""
        self.stop() # Stop the server process and signals its reader threads
        self._log("ServerManager shut down complete.")