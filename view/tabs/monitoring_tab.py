import customtkinter as ctk
from lib.config import Config
from lib.paths import get_downloads_folder
from view.widgets.file_picker import FilePicker


class MonitoringTab(ctk.CTkFrame):
    def __init__(self, master, config: Config, **kwargs):
        super().__init__(master, **kwargs)
        
        self.config = config
        
        self.setup_ui()
        self.load_monitoring_settings()
    
    def setup_ui(self):
        self.label = ctk.CTkLabel(self, text="Monitoramento", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=20, pady=20)
        
        path_label = ctk.CTkLabel(frame, text="Pasta Monitorada:", font=("Arial", 12))
        path_label.pack(anchor="w", padx=5, pady=5)
        
        current_path = self.config.get_watch_folder() or str(get_downloads_folder())
        
        def on_path_change(path):
            self.config.set_watch_folder(path)
        
        self.file_picker = FilePicker(frame, initial_path=current_path, on_change=on_path_change)
        self.file_picker.pack(fill="x", padx=5, pady=5)
        
        info_label = ctk.CTkLabel(frame, text="Selecione a pasta que deseja monitorar para novos downloads.", font=("Arial", 10))
        info_label.pack(anchor="w", padx=5, pady=5)
        
        notifications_frame = ctk.CTkFrame(frame)
        notifications_frame.pack(fill="x", padx=5, pady=10)
        
        def on_notifications_toggle():
            self.config.set_enable_notifications(self.notifications_checkbox.get())
        
        self.notifications_checkbox = ctk.CTkCheckBox(
            notifications_frame,
            text="Habilitar notificações ao organizar arquivos",
            command=on_notifications_toggle
        )
        self.notifications_checkbox.pack(anchor="w", padx=5, pady=5)
        
        delay_frame = ctk.CTkFrame(frame)
        delay_frame.pack(fill="x", padx=5, pady=10)
        
        delay_label = ctk.CTkLabel(delay_frame, text="Delay antes de mover (minutos):", font=("Arial", 12))
        delay_label.pack(anchor="w", padx=5, pady=5)
        
        def on_delay_change(value):
            try:
                minutes = int(float(value))
                self.config.set_delay_minutes(minutes)
            except ValueError:
                pass
        
        self.delay_entry = ctk.CTkEntry(delay_frame, width=100)
        self.delay_entry.pack(anchor="w", padx=5, pady=5)
        self.delay_entry.bind("<KeyRelease>", lambda e: on_delay_change(e.widget.get()))
    
    def load_monitoring_settings(self):
        current_path = self.config.get_watch_folder()
        
        if current_path:
            self.file_picker.set_path(current_path)
        
        self.notifications_checkbox.set(self.config.get_enable_notifications())
        self.delay_entry.delete(0, "end")
        self.delay_entry.insert(0, str(self.config.get_delay_minutes()))
