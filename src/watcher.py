import logging
import threading
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer

from src.handler import DownloadHandler

logger = logging.getLogger(__name__)


class DownloadWatcher:
    def __init__(self, watch_path: Path, paused_event: threading.Event):
        self.watch_path = watch_path
        self.paused_event = paused_event
        self.observer: Optional[Observer] = None

    def start(self):
        self.observer = Observer()
        handler = DownloadHandler(self.paused_event)
        self.observer.schedule(handler, str(self.watch_path), recursive=False)
        self.observer.start()

        logger.info(f"Watching: {self.watch_path}")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Watcher stopped")
