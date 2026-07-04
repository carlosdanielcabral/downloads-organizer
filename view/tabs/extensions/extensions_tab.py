import customtkinter as ctk
from lib.config.config import Config


class ExtensionsTab(ctk.CTkFrame):
    CATEGORIES = ["IMAGES", "VIDEOS", "AUDIO", "DOCUMENTS", "OTHER"]
    
    def __init__(self, master, config: Config, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config = config
        
        self.setup_ui()
        self.load_extensions()
    
    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Mapeamento de Extensões", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, height=400)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.extension_rows = {}
    
    def load_extensions(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.extension_rows = {}
        
        for ext, category in sorted(self.config.data["extension_mappings"].items()):
            self.add_extension_row(ext, category)
    
    def add_extension_row(self, ext: str, category: str):
        row = ctk.CTkFrame(self.scrollable_frame)
        row.pack(fill="x", pady=2)
        
        ext_label = ctk.CTkLabel(row, text=f".{ext}", width=80)
        ext_label.pack(side="left", padx=5)
        
        def on_category_change(value):
            self.config.set_extension_category(ext, value)
        
        category_menu = ctk.CTkOptionMenu(
            row,
            values=self.CATEGORIES,
            command=on_category_change
        )
        category_menu.set(category)
        category_menu.pack(side="left", padx=5)
        
        remove_button = ctk.CTkButton(row, text="X", width=30, fg_color="red", command=lambda: self.remove_extension(ext, row))
        remove_button.pack(side="left", padx=5)
        
        self.extension_rows[ext] = {
            "row": row,
            "menu": category_menu
        }
    
    def remove_extension(self, ext: str, row_widget):
        del self.config.data["extension_mappings"][ext]
        row_widget.destroy()
        del self.extension_rows[ext]
    
    def add_new_extension(self):
        self.add_extension_row("", "OTHER")
