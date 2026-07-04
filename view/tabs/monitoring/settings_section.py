import customtkinter as ctk

from lib.config.config import Config
from lib.processing.paths import get_downloads_folder
from view.widgets.file_picker import FilePicker


class SettingsSection(ctk.CTkFrame):
    """
    Displays and manages the monitoring configuration inputs:
    watched folder, notifications toggle and move delay.

    Each input writes directly to the Config object on change.
    Persisting to disk is the responsibility of the caller (ConfigWindow).
    """

    def __init__(self, master, config: Config, **kwargs):
        super().__init__(master, **kwargs)

        self._config = config

        self._setup_ui()
        self._load_values()

    def _setup_ui(self) -> None:
        self._setup_watch_folder_input()
        self._setup_notifications_input()
        self._setup_delay_input()

    def _setup_watch_folder_input(self) -> None:
        path_label = ctk.CTkLabel(self, text="Pasta Monitorada:", font=("Arial", 12))
        path_label.pack(anchor="w", padx=5, pady=(10, 0))

        current_path = self._config.get_watch_folder() or str(get_downloads_folder())

        self._file_picker = FilePicker(self, initial_path=current_path, on_change=self._on_watch_folder_change)
        self._file_picker.pack(fill="x", padx=5, pady=5)

        info_label = ctk.CTkLabel(
            self,
            text="Selecione a pasta que deseja monitorar para novos downloads.",
            font=("Arial", 10),
        )
        info_label.pack(anchor="w", padx=5, pady=(0, 5))

    def _setup_notifications_input(self) -> None:
        notifications_frame = ctk.CTkFrame(self)
        notifications_frame.pack(fill="x", padx=5, pady=10)

        self._notifications_checkbox = ctk.CTkCheckBox(
            notifications_frame,
            text="Habilitar notificações ao organizar arquivos",
            command=self._on_notifications_toggle,
        )
        self._notifications_checkbox.pack(anchor="w", padx=5, pady=5)

    def _setup_delay_input(self) -> None:
        delay_frame = ctk.CTkFrame(self)
        delay_frame.pack(fill="x", padx=5, pady=10)

        delay_label = ctk.CTkLabel(delay_frame, text="Delay antes de mover (minutos):", font=("Arial", 12))
        delay_label.pack(anchor="w", padx=5, pady=5)

        self._delay_entry = ctk.CTkEntry(delay_frame, width=100)
        self._delay_entry.pack(anchor="w", padx=5, pady=5)
        self._delay_entry.bind("<KeyRelease>", lambda event: self._on_delay_change(event.widget.get()))

    def _load_values(self) -> None:
        current_path = self._config.get_watch_folder()

        if current_path:
            self._file_picker.set_path(current_path)

        self._notifications_checkbox.set(self._config.get_enable_notifications())
        self._delay_entry.delete(0, "end")
        self._delay_entry.insert(0, str(self._config.get_delay_minutes()))

    def _on_watch_folder_change(self, path: str) -> None:
        self._config.set_watch_folder(path)

    def _on_notifications_toggle(self) -> None:
        self._config.set_enable_notifications(self._notifications_checkbox.get())

    def _on_delay_change(self, value: str) -> None:
        try:
            minutes = int(float(value))
            self._config.set_delay_minutes(minutes)
        except ValueError:
            pass
