import customtkinter as ctk
from pathlib import Path
from lib.config import Config
from view.tabs.extensions_tab import ExtensionsTab
from view.tabs.folders_tab import FoldersTab
from view.tabs.monitoring_tab import MonitoringTab


class ConfigWindow(ctk.CTk):
    def __init__(self, config: Config, config_path: Path, on_save_callback=None, move_now_callback=None, reload_config_callback=None):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.config = config
        self.config_path = config_path
        self.on_save_callback = on_save_callback
        self.move_now_callback = move_now_callback
        self.reload_config_callback = reload_config_callback
        
        self.title("Download Organizer - Configurações")
        self.geometry("900x700")
        
        self.setup_ui()
    
    def setup_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("Pastas")
        self.tabview.add("Monitoramento")
        self.tabview.add("Extensões")
        
        self.folders_tab = FoldersTab(self.tabview.tab("Pastas"), self.config)
        self.folders_tab.pack(fill="both", expand=True)
        
        self.monitoring_tab = MonitoringTab(self.tabview.tab("Monitoramento"), self.config)
        self.monitoring_tab.pack(fill="both", expand=True)
        
        self.extensions_tab = ExtensionsTab(self.tabview.tab("Extensões"), self.config)
        self.extensions_tab.pack(fill="both", expand=True)
        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, padx=10, fill="x")
        
        move_now_button = ctk.CTkButton(button_frame, text="Mover Arquivos Pendentes Agora", command=self.move_now, height=40)
        move_now_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        
        save_button = ctk.CTkButton(button_frame, text="Salvar e Aplicar", command=self.save_and_apply, height=40)
        save_button.pack(side="left", padx=5, pady=5, expand=True, fill="x")
    
    def save_and_apply(self):
        self.config.save(self.config_path)

        if self.reload_config_callback:
            self.reload_config_callback()

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()

    def move_now(self):
        if self.move_now_callback:
            self.move_now_callback()


def show_config_window(config: Config, config_path: Path, on_save_callback=None, move_now_callback=None, reload_config_callback=None):
    app = ConfigWindow(config, config_path, on_save_callback, move_now_callback, reload_config_callback)
    app.mainloop()
    
    if on_save_callback:
        on_save_callback()
