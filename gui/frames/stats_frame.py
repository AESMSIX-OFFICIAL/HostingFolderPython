import customtkinter as ctk
import psutil
import time
import config

class StatsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Network Traffic (System Wide)", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.send_label = ctk.CTkLabel(self, text="Send: 0.00 Mbps")
        self.send_label.grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.recv_label = ctk.CTkLabel(self, text="Receive: 0.00 Mbps")
        self.recv_label.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        self._last_net_io = psutil.net_io_counters()
        self._last_update_time = time.monotonic()

    def update_stats(self):
        """Calculates and updates network speed labels."""
        try:
            current_net_io = psutil.net_io_counters()
            current_time = time.monotonic()
            elapsed_time = current_time - self._last_update_time
            if elapsed_time <= 0.1: # Use a small threshold
                 self._last_net_io = current_net_io
                 self._last_update_time = current_time
                 return # Skip update if time hasn't passed

            bytes_sent = max(0, current_net_io.bytes_sent - self._last_net_io.bytes_sent)
            bytes_recv = max(0, current_net_io.bytes_recv - self._last_net_io.bytes_recv)
            send_speed_mbps = (bytes_sent * 8) / (1_000_000 * elapsed_time)
            recv_speed_mbps = (bytes_recv * 8) / (1_000_000 * elapsed_time)

            self.send_label.configure(text=f"Send: {send_speed_mbps:.2f} Mbps")
            self.recv_label.configure(text=f"Receive: {recv_speed_mbps:.2f} Mbps")

            self._last_net_io = current_net_io
            self._last_update_time = current_time

        except Exception as e:
            self.send_label.configure(text="Send: Error")
            self.recv_label.configure(text="Receive: Error")

    def update_ui(self):
         """Called by the main app's periodic update to refresh UI elements."""
         self.update_stats()