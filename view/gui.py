import customtkinter as ctk
from pathlib import Path
from PIL import Image, ImageTk

from lib.config.config import Config
from lib.history.move_history import MoveHistory
from lib.processing.file_processor import FileProcessor
from view.tabs.extensions.extensions_tab import ExtensionsTab
from view.tabs.folders.folders_tab import FoldersTab
from view.tabs.monitoring.monitoring_tab import MonitoringTab

WINDOW_TITLE = "Download Organizer"
WINDOW_GEOMETRY = "900x700"
ICON_PATH = Path(__file__).parent / "assets" / "icon.png"
ICON_SIZE = (32, 32)


class ConfigWindow(ctk.CTkToplevel):
    """
    Main configuration window for the Download Organizer application.

    Hosts three tabs: Monitoramento (default), Pastas and Extensões.
    Provides a footer with a single Salvar e Aplicar button that persists
    the configuration and closes the window.

    Unregisters the MonitoringTab queue observer when the window is closed
    to prevent dangling callbacks from a destroyed widget.
    """

    def __init__(self, config: Config, config_path: Path, processor: FileProcessor, reload_config_callback=None, move_history: MoveHistory = None):
        super().__init__()

        self.lift()
        self.focus_force()

        self._config = config
        self._config_path = config_path
        self._processor = processor
        self._reload_config_callback = reload_config_callback
        self._move_history = move_history

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_GEOMETRY)

        self._set_window_icon()
        self._setup_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _set_window_icon(self) -> None:
        if not ICON_PATH.exists():
            return

        try:
            pil_image = Image.open(ICON_PATH).resize(ICON_SIZE)
            self._icon_photo = ImageTk.PhotoImage(pil_image)
            self.iconphoto(True, self._icon_photo)
        except Exception:
            pass

    def _setup_ui(self) -> None:
        self._setup_footer()
        self._setup_tabs()

    def _setup_tabs(self) -> None:
        self._tabview = ctk.CTkTabview(self)
        self._tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self._tabview.add("Monitoramento")
        self._tabview.add("Pastas")
        self._tabview.add("Extensões")

        self._monitoring_tab = MonitoringTab(
            self._tabview.tab("Monitoramento"),
            config=self._config,
            processor=self._processor,
            move_history=self._move_history,
        )
        self._monitoring_tab.pack(fill="both", expand=True, anchor="n")

        self._folders_tab = FoldersTab(self._tabview.tab("Pastas"), self._config)
        self._folders_tab.pack(fill="both", expand=True)

        self._extensions_tab = ExtensionsTab(self._tabview.tab("Extensões"), self._config)
        self._extensions_tab.pack(fill="both", expand=True)

    def _setup_footer(self) -> None:
        footer_frame = ctk.CTkFrame(self)
        footer_frame.pack(side="bottom", pady=10, padx=10, fill="x")

        save_button = ctk.CTkButton(footer_frame, text="Salvar e Aplicar", command=self._on_save_and_apply, height=40)
        save_button.pack(padx=5, pady=5, fill="x")

    def _on_save_and_apply(self) -> None:
        self._config.save(self._config_path)

        if self._reload_config_callback:
            self._reload_config_callback()

        self._on_close()

    def _on_close(self) -> None:
        self._monitoring_tab.unregister_observer()
        self.destroy()
