import customtkinter as ctk
import tkinter

class LogFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Allow textbox to expand

        ctk.CTkLabel(self, text="Server Log Output", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.log_box = ctk.CTkTextbox(self, wrap="word", state="disabled")
        self.log_box.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.log_scrollbar = ctk.CTkScrollbar(self, command=self.log_box.yview)
        self.log_scrollbar.grid(row=1, column=1, padx=(0,5), pady=5, sticky='ns')
        self.log_box.configure(yscrollcommand=self.log_scrollbar.set)

    def append_log(self, message: str):
        """Appends a message to the log textbox."""
        self.log_box.configure(state="normal") # Enable editing
        self.log_box.insert(tkinter.END, message + "\n")
        self.log_box.see(tkinter.END) # Scroll to the bottom
        self.log_box.configure(state="disabled") # Disable editing

    def update_ui(self):
         """This frame updates only when append_log is called, not on a timer."""
         pass # No periodic UI updates needed for the log box itself