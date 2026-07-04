import customtkinter as ctk

from lib.config.config import Config
from lib.processing.file_processor import FileProcessor
from view.tabs.monitoring.settings_section import SettingsSection
from view.tabs.monitoring.status_section import StatusSection


class MonitoringTab(ctk.CTkFrame):
    """
    Orchestrates the Monitoramento tab by composing StatusSection and
    SettingsSection.

    Delegates observer lifecycle to StatusSection, which owns the queue
    reactivity. ConfigWindow calls unregister_observer() before destroying
    this tab to prevent dangling callbacks.
    """

    def __init__(self, master, config: Config, processor: FileProcessor, **kwargs):
        super().__init__(master, **kwargs)

        self._setup_ui(config, processor)

    def unregister_observer(self) -> None:
        self._status_section.unregister_observer()

    def _setup_ui(self, config: Config, processor: FileProcessor) -> None:
        self._setup_status_section(processor)
        self._setup_settings_section(config)

    def _setup_status_section(self, processor: FileProcessor) -> None:
        section_label = ctk.CTkLabel(self, text="Status", font=("Arial", 14, "bold"))
        section_label.pack(anchor="w", padx=20, pady=(15, 0))

        self._status_section = StatusSection(self, processor=processor)
        self._status_section.pack(fill="x", padx=20, pady=(5, 10))

    def _setup_settings_section(self, config: Config) -> None:
        section_label = ctk.CTkLabel(self, text="Configurações", font=("Arial", 14, "bold"))
        section_label.pack(anchor="w", padx=20, pady=(10, 0))

        self._settings_section = SettingsSection(self, config=config)
        self._settings_section.pack(fill="x", padx=20, pady=(5, 10))
