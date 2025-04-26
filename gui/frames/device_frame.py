import customtkinter as ctk
import tkinter
import tkinter.messagebox
import config
from common import file_utils
from core.server_manager import ServerManager # Diperlukan untuk type hinting dan memanggil metodenya

class DeviceFrame(ctk.CTkFrame):
    def __init__(self, master, server_manager: ServerManager, **kwargs):
        super().__init__(master, **kwargs)
        self.server_manager = server_manager # Need manager to get connected IPs

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1) # Allow listbox to expand

        ctk.CTkLabel(self, text="Logged Connections (Since Server Start)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.device_listbox = tkinter.Listbox(self, height=8, bg="#2D2D2D", fg="white", borderwidth=0, highlightthickness=0, selectbackground="#1F6AA5", selectforeground="white", selectmode=tkinter.EXTENDED) # Allow extended selection
        self.device_listbox.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.list_scrollbar = ctk.CTkScrollbar(self, command=self.device_listbox.yview)
        self.list_scrollbar.grid(row=1, column=2, padx=(0,5), pady=5, sticky='ns')
        self.device_listbox.configure(yscrollcommand=self.list_scrollbar.set)

        self.block_button = ctk.CTkButton(self, text="Block Selected", command=self._block_selected, state="disabled")
        self.block_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.unblock_button = ctk.CTkButton(self, text="Unblock Selected", command=self._unblock_selected, state="disabled")
        self.unblock_button.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    def get_selected_ips(self) -> list[str]:
        """Gets the raw IP addresses of selected items in the listbox."""
        selected_indices = self.device_listbox.curselection()
        selected_ips = []
        for i in selected_indices:
            item = self.device_listbox.get(i)
            selected_ips.append(item.split(" ")[0])
        return selected_ips

    def _block_selected(self):
        """Blocks selected IP addresses using file utilities."""
        selected_ips = self.get_selected_ips()
        if not selected_ips:
            tkinter.messagebox.showinfo("Block IP", "No IP address selected.")
            return

        ips_blocked_count = 0
        for ip in selected_ips:
            if file_utils.add_blocked_ip(config.BLOCKED_IPS_FILE_PATH, ip):
                ips_blocked_count += 1

        if ips_blocked_count > 0:
            self.update_ui() # Gunakan metode update_ui untuk refresh listbox
        else:
            tkinter.messagebox.showinfo("Block IP", "Selected IPs are already blocked or an error occurred.")


    def _unblock_selected(self):
        """Unblocks selected IP addresses using file utilities."""
        selected_ips = self.get_selected_ips()
        if not selected_ips:
            tkinter.messagebox.showinfo("Unblock IP", "No IP address selected.")
            return

        ips_unblocked_count = 0
        for ip in selected_ips:
             if file_utils.remove_blocked_ip(config.BLOCKED_IPS_FILE_PATH, ip):
                 ips_unblocked_count += 1

        if ips_unblocked_count > 0:
             self.update_ui() # Gunakan metode update_ui untuk refresh listbox
        else:
             tkinter.messagebox.showinfo("Unblock IP", "Selected IPs are not currently blocked or an error occurred.")
    def update_list(self, connected_ips: set[str] | None = None):
        """Updates the device listbox with current connected IPs."""
        ips_to_display = self.server_manager.get_connected_ips_from_log()

        current_selection_ips = set(self.get_selected_ips()) # Simpan seleksi saat ini
        self.device_listbox.delete(0, tkinter.END) # Hapus list saat ini

        if not ips_to_display:
            if not self.server_manager.is_running:
                 self.device_listbox.insert(tkinter.END, "Server stopped.")
            else:
                 self.device_listbox.insert(tkinter.END, "No connections logged yet.")
            self.block_button.configure(state="disabled")
            self.unblock_button.configure(state="disabled")
            return

        blocked_ips_set = file_utils.get_blocked_ips(config.BLOCKED_IPS_FILE_PATH) # Dapatkan daftar blokir terbaru
        sorted_ips = sorted(list(ips_to_display)) # Sortir IP untuk tampilan konsisten

        new_selection_indices = []
        for index, ip in enumerate(sorted_ips):
            display_text = ip
            if ip in blocked_ips_set:
                display_text += " (Blocked)"
            self.device_listbox.insert(tkinter.END, display_text)
            if ip in current_selection_ips:
                 new_selection_indices.append(index)
        for idx in new_selection_indices:
            self.device_listbox.select_set(idx)
        if new_selection_indices:
            self.device_listbox.see(new_selection_indices[0])
        if self.server_manager.is_running and len(ips_to_display) > 0:
             self.block_button.configure(state="normal")
             self.unblock_button.configure(state="normal")
        else:
             self.block_button.configure(state="disabled")
             self.unblock_button.configure(state="disabled")


    def update_ui(self):
         """Called by the main app's periodic update to refresh UI elements."""
         self.update_list()