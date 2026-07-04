import logging
import threading
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer

from lib.handler import DownloadHandler
from lib.config import Config

logger = logging.getLogger(__name__)


class DownloadWatcher:
    """
    Monitors a folder for new files and coordinates their organization.

    Owns the pause state and exposes pause/resume controls. Manages the
    lifecycle of the watchdog Observer and the DownloadHandler attached to it.
    """

    def __init__(self, watch_path: Path, config: Config):
        self.watch_path = watch_path
        self.config = config
        self._paused_event = threading.Event()
        self.observer: Optional[Observer] = None
        self.handler: Optional[DownloadHandler] = None

    def pause(self) -> None:
        self._paused_event.set()

    def resume(self) -> None:
        self._paused_event.clear()

    def is_paused(self) -> bool:
        return self._paused_event.is_set()

    def start(self):
        self.observer = Observer()
        self.handler = DownloadHandler(self._paused_event, self.config)
        self.observer.schedule(self.handler, str(self.watch_path), recursive=False)
        self.observer.start()

        logger.info(f"Watching: {self.watch_path}")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Watcher stopped")
