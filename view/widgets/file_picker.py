import customtkinter as ctk
from tkinter import filedialog


class FilePicker(ctk.CTkFrame):
    def __init__(self, master, initial_path: str = "", on_change=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_change = on_change
        
        self.entry = ctk.CTkEntry(self)
        self.entry.insert(0, initial_path)
        self.entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        self.button = ctk.CTkButton(self, text="...", width=40, command=self.browse_folder)
        self.button.pack(side="left", padx=5, pady=5)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(title="Selecione a pasta")
        
        if folder:
            self.entry.delete(0, "end")
            self.entry.insert(0, folder)
            
            if self.on_change:
                self.on_change(folder)
    
    def get_path(self) -> str:
        return self.entry.get()
    
    def set_path(self, path: str) -> None:
        self.entry.delete(0, "end")
        self.entry.insert(0, path)
