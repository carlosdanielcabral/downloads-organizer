import logging
import threading
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer

from lib.handler import DownloadHandler
from lib.config import Config

logger = logging.getLogger(__name__)


class DownloadWatcher:
    def __init__(self, watch_path: Path, paused_event: threading.Event, config: Config):
        self.watch_path = watch_path
        self.paused_event = paused_event
        self.config = config
        self.observer: Optional[Observer] = None
        self.handler: Optional[DownloadHandler] = None

    def start(self):
        self.observer = Observer()
        self.handler = DownloadHandler(self.paused_event, self.config)
        self.observer.schedule(self.handler, str(self.watch_path), recursive=False)
        self.observer.start()

        logger.info(f"Watching: {self.watch_path}")

    def stop(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logger.info("Watcher stopped")
