import threading
import logging
from pathlib import Path

from lib.config.config import Config
from lib.watcher.file_event_watcher import FileEventWatcher

logger = logging.getLogger(__name__)


class GuiManager:
    """
    Manages the lifecycle of the configuration window.

    Tkinter must run on a single dedicated thread for its entire lifetime.
    GuiManager starts that thread once and keeps it alive with a hidden root
    window. Open/focus requests from other threads are marshaled into the
    tkinter thread via after().
    """

    def __init__(self, watcher: FileEventWatcher, config: Config, config_path: Path, reload_config_callback=None):
        self._watcher = watcher
        self._config = config
        self._config_path = config_path
        self._reload_config_callback = reload_config_callback
        self._window = None
        self._root = None
        self._ready = threading.Event()

        self._thread = threading.Thread(target=self._run_gui_thread, daemon=True)
        self._thread.start()
        self._ready.wait()

    def open_window(self) -> None:
        self._root.after(0, self._open_or_focus_window)

    def _run_gui_thread(self) -> None:
        import customtkinter as ctk

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self._root = ctk.CTk()
        self._root.withdraw()
        self._ready.set()
        self._root.mainloop()

    def _open_or_focus_window(self) -> None:
        if self._is_window_open():
            self._bring_window_to_front()

            return

        self._open_window()

    def _is_window_open(self) -> bool:
        return self._window is not None and self._window.winfo_exists()

    def _bring_window_to_front(self) -> None:
        self._window.lift()
        self._window.focus_force()

    def _open_window(self) -> None:
        from view.gui import ConfigWindow

        processor = self._watcher.get_processor()

        self._window = ConfigWindow(
            config=self._config,
            config_path=self._config_path,
            processor=processor,
            reload_config_callback=self._reload_config_callback,
        )
