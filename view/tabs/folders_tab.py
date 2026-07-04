import customtkinter as ctk
from pathlib import Path
from lib.config.config import Config
from view.widgets.file_picker import FilePicker


class FoldersTab(ctk.CTkFrame):
    def __init__(self, master, config: Config, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config = config
        
        self.setup_ui()
        self.load_folders()
    
    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Mapeamento de Pastas", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, height=400)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.folder_pickers = {}
    
    def load_folders(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.folder_pickers = {}
        
        categories = ["IMAGES", "VIDEOS", "AUDIO", "DOCUMENTS", "OTHER"]
        
        for category in categories:
            self.add_folder_row(category)
    
    def add_folder_row(self, category: str):
        row = ctk.CTkFrame(self.scrollable_frame)
        row.pack(fill="x", pady=5)
        
        category_label = ctk.CTkLabel(row, text=category, width=100)
        category_label.pack(side="left", padx=5)
        
        current_path = self.config.get_folder_path(category)
        
        def on_path_change(path):
            self.config.set_folder_path(category, path)
        
        picker = FilePicker(row, initial_path=current_path, on_change=on_path_change)
        picker.pack(side="left", fill="x", expand=True, padx=5)
        
        self.folder_pickers[category] = picker
