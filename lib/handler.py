import logging
import threading
from pathlib import Path

from watchdog.events import FileSystemEventHandler

from lib.mover import organize_download
from lib.paths import is_inside_downloads, resolve_destination
from lib.rules import PARTIAL_EXTENSIONS, get_category
from lib.config import Config

logger = logging.getLogger(__name__)


class DownloadHandler(FileSystemEventHandler):
    def __init__(self, paused_event: threading.Event, config: Config):
        super().__init__()
        self.paused_event = paused_event
        self.config = config
        self._debounce_timers: dict[str, threading.Timer] = {}
        self._delay_timers: dict[str, threading.Timer] = {}

    def on_created(self, event):
        if event.is_directory:
            return

        self._handle_new_file(Path(event.src_path))

    def on_moved(self, event):
        if event.is_directory:
            return

        self._handle_new_file(Path(event.dest_path))

    def _handle_new_file(self, path: Path):
        logger.info(f"File event detected: {path}")

        if not path.exists():
            logger.debug(f"File does not exist: {path}")
            return

        if path.is_dir():
            logger.debug(f"Is directory, skipping: {path}")
            return

        if not is_inside_downloads(path):
            logger.debug(f"Not inside Downloads folder: {path}")
            return

        if path.suffix.lower() in PARTIAL_EXTENSIONS:
            logger.debug(f"Ignoring partial download: {path}")
            return

        file_key = str(path)

        if file_key in self._debounce_timers:
            self._debounce_timers[file_key].cancel()

        self._debounce_timers[file_key] = threading.Timer(
            1.5,
            lambda: self._process_file(path)
        )
        self._debounce_timers[file_key].start()

        logger.info(f"Scheduled processing for: {path}")

    def _process_file(self, path: Path):
        file_key = str(path)
        self._debounce_timers.pop(file_key, None)

        if self.paused_event.is_set():
            logger.debug(f"Watcher paused, skipping: {path}")
            return

        if not path.exists():
            return

        delay_minutes = self.config.get_delay_minutes()
        delay_seconds = delay_minutes * 60

        if delay_seconds > 0:
            if file_key in self._delay_timers:
                self._delay_timers[file_key].cancel()

            self._delay_timers[file_key] = threading.Timer(
                delay_seconds,
                lambda: self._move_file(path)
            )
            self._delay_timers[file_key].start()

            logger.info(f"Scheduled move for {path.name} in {delay_minutes} minutes")
        else:
            self._move_file(path)

    def _move_file(self, path: Path):
        file_key = str(path)
        self._delay_timers.pop(file_key, None)

        if not path.exists():
            logger.debug(f"File no longer exists: {path}")
            return

        category = get_category(path, self.config)
        destination = resolve_destination(category, self.config)

        logger.info(f"Processing {path.name} as {category}")

        organize_download(path, destination, self.config)
