import tkinter.messagebox
import customtkinter as ctk
import sys
from pathlib import Path
import os
import tkinter # Diperlukan untuk tkinter.Toplevel, dll jika menggunakan messagebox standar atau filedialog

 
import config
from common import file_utils
from core.server_manager import ServerManager
from gui.frames.status_frame import StatusFrame
from gui.frames.stats_frame import StatsFrame
from gui.frames.device_frame import DeviceFrame
from gui.frames.log_frame import LogFrame


class ServerControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Server Control Panel")
        self.geometry("700x650")
        ctk.set_appearance_mode("System") # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"

 
 
        self._initialize_files()

 
        saved_folder_path = file_utils.load_served_folder_setting(config.SERVED_FOLDER_SETTING_PATH)

 
        initial_served_folder = saved_folder_path if saved_folder_path else config.DEFAULT_SERVE_PATH

 
        self.server_manager = ServerManager(
            served_folder_path=initial_served_folder, # Gunakan jalur yang dimuat/default
            log_callback=self._append_log_message, # Pass method to handle logs
        )

 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Allow device frame to expand
        self.grid_rowconfigure(3, weight=1) # Allow log frame to expand


        self.status_frame = StatusFrame(self, server_manager=self.server_manager)
        self.status_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.stats_frame = StatsFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

 
        self.device_frame = DeviceFrame(self, server_manager=self.server_manager)
        self.device_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.log_frame = LogFrame(self)
        self.log_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

 
 
        self._schedule_log_queue_processing()

 
        self._schedule_periodic_updates()

 
        self.protocol("WM_DELETE_WINDOW", self._on_closing)


    def _initialize_files(self):
        """Ensures necessary directories and files exist."""
        try:
 
            file_utils.ensure_dirs_exist(config.LOG_DIR)

 
            file_utils.ensure_file_exists(config.CONNECTED_IPS_LOG_PATH)
            file_utils.ensure_file_exists(config.BLOCKED_IPS_FILE_PATH)
            file_utils.ensure_file_exists(config.SERVED_FOLDER_SETTING_PATH) # <--- Pastikan file pengaturan ada

 
            file_utils.ensure_dirs_exist(config.DEFAULT_SERVE_PATH)

        except Exception as e:
 
             tkinter.messagebox.showerror("Initialization Error", f"Could not create necessary files/folders: {e}")
 
 

 
    def _save_served_folder_setting(self, folder_path: Path):
        """Saves the current served folder path using file utilities."""
        file_utils.save_served_folder_setting(config.SERVED_FOLDER_SETTING_PATH, folder_path)
 
        self._append_log_message(f"[GUI] Saved served folder setting: {folder_path}")


    def _append_log_message(self, message: str):
        """Callback method to receive log messages from ServerManager and update GUI."""
        self.after(0, self.log_frame.append_log, message)


    def _schedule_log_queue_processing(self):
        """Schedules the periodic processing of the ServerManager's log queue."""
        self.server_manager.process_log_queue()
        self.after(config.LOG_QUEUE_CHECK_INTERVAL_MS, self._schedule_log_queue_processing)


    def _schedule_periodic_updates(self):
        """Schedules the periodic GUI updates."""
        self._perform_periodic_updates()
        self.after(config.UPDATE_INTERVAL_MS, self._schedule_periodic_updates)


    def _perform_periodic_updates(self):
        """Helper to call update_ui on all frames on the main thread."""
        self.status_frame.update_ui()
        self.stats_frame.update_ui()
        self.device_frame.update_ui()


    def _on_closing(self):
        """Handles the window closing event."""
        if tkinter.messagebox.askokcancel("Quit", "Do you want to quit? This will stop the server if it's running."):
 
            self.server_manager.shutdown()
            self.destroy() # Close the GUI window