import threading
import logging
from pathlib import Path

from lib.config.config import Config
from lib.watcher.file_event_watcher import FileEventWatcher

logger = logging.getLogger(__name__)


class GuiManager:
    """
    Manages the lifecycle of the configuration window.

    Ensures only one window instance exists at any time (singleton pattern).
    Opens the window on a dedicated thread so it does not block the tray
    or watcher. When the window is already open, focuses it instead of
    creating a second one.
    """

    def __init__(self, watcher: FileEventWatcher, config: Config, config_path: Path, reload_config_callback=None):
        self._watcher = watcher
        self._config = config
        self._config_path = config_path
        self._reload_config_callback = reload_config_callback
        self._window = None
        self._lock = threading.Lock()

    def open_window(self) -> None:
        with self._lock:
            if self._is_window_open():
                self._bring_window_to_front()
                return

            self._start_window_thread()

    def _is_window_open(self) -> bool:
        return self._window is not None and self._window.winfo_exists()

    def _bring_window_to_front(self) -> None:
        self._window.lift()
        self._window.focus()

    def _start_window_thread(self) -> None:
        thread = threading.Thread(target=self._run_window, daemon=True)
        thread.start()

    def _run_window(self) -> None:
        from view.gui import ConfigWindow

        processor = self._watcher.get_processor()

        self._window = ConfigWindow(
            config=self._config,
            config_path=self._config_path,
            processor=processor,
            reload_config_callback=self._reload_config_callback,
        )

        self._window.mainloop()
        self._window = None
