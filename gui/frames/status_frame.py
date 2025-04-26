import sys
import customtkinter as ctk
import tkinter.filedialog
from pathlib import Path
import tkinter # Untuk tkinter.messagebox, dll

 
import config
from core.server_manager import ServerManager
 
if sys.version_info >= (3, 9):
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from gui.app import ServerControlApp # Import for type checking only

class StatusFrame(ctk.CTkFrame):
 
    def __init__(self, master: "ServerControlApp", server_manager: ServerManager, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master # Simpan referensi ke aplikasi utama
        self.server_manager = server_manager

        self.grid_columnconfigure(1, weight=1) # Allow folder label to expand

 
        ctk.CTkLabel(self, text="Server Status:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.status_label = ctk.CTkLabel(self, text="Stopped", text_color="red", anchor="w")
        self.status_label.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.toggle_button = ctk.CTkButton(self, text="Turn On Server", command=self._toggle_server)
        self.toggle_button.grid(row=0, column=2, padx=5, pady=5)

 
        ctk.CTkLabel(self, text="Serving Folder:", font=ctk.CTkFont(weight="bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.folder_label = ctk.CTkLabel(self, text=str(self.server_manager.get_served_folder()), anchor="w")
        self.folder_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.change_folder_button = ctk.CTkButton(self, text="Change Folder", command=self._change_folder)
        self.change_folder_button.grid(row=1, column=2, padx=5, pady=5)

 
 


    def _toggle_server(self):
        """Handles the server on/off button click."""
        if self.server_manager.is_running:
            self.server_manager.stop()
        else:
            if self.server_manager.start():
                 pass # GUI will update via periodic calls
            else:
                 pass # GUI will update via periodic calls on immediate failure

    def _change_folder(self):
        """Opens a dialog to select a new folder to serve."""
        if self.server_manager.is_running:
            tkinter.messagebox.showwarning("Server Running", "Please stop the server before changing the folder.")
            return

 
        initial_dir = str(self.server_manager.get_served_folder().parent)
        new_folder_str = tkinter.filedialog.askdirectory(initialdir=initial_dir, title="Select Folder to Serve")

        if new_folder_str:
            resolved_new_folder = Path(new_folder_str).resolve()
 
            if self.server_manager.set_served_folder(resolved_new_folder):
 
                 self.master._save_served_folder_setting(resolved_new_folder) # <--- Panggil metode simpan
 
                 self.update_folder_label()
 
                 if hasattr(self.master, 'device_frame') and self.master.device_frame:
                      self.master.device_frame.update_list(["Change folder selected. Restart server."])


    def update_status(self):
        """Updates the status label and button based on server state."""
        status = self.server_manager.get_status()
        self.status_label.configure(text=status)

        if status == "Running":
            self.status_label.configure(text_color="green")
            self.toggle_button.configure(text="Turn Off Server", state="normal")
            self.change_folder_button.configure(state="disabled")
        elif status.startswith("Exited"):
             self.status_label.configure(text_color="orange")
             self.toggle_button.configure(text="Turn On Server", state="normal")
             self.change_folder_button.configure(state="normal")
        else: # Stopped
            self.status_label.configure(text_color="red")
            self.toggle_button.configure(text="Turn On Server", state="normal")
            self.change_folder_button.configure(state="normal")

    def update_folder_label(self):
         """Updates the served folder label from the manager."""
         self.folder_label.configure(text=str(self.server_manager.get_served_folder()))

    def update_ui(self):
        """Called by the main app's periodic update to refresh UI elements."""
        self.update_status()
 