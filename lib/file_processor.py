import logging
from pathlib import Path

from lib.config import Config
from lib.delay_queue import DelayQueue
from lib.mover import organize_download
from lib.paths import is_inside_downloads, resolve_destination
from lib.rules import PARTIAL_EXTENSIONS, get_category

logger = logging.getLogger(__name__)

DELAY_SECONDS_MINIMUM = 0


class FileProcessor:
    """
    Processes files detected in the Downloads folder.

    Validates each file, then schedules it to be moved after the configured
    delay. If the delay is zero, the move is executed immediately. All
    pending moves can be forced to execute immediately via move_pending.
    """

    def __init__(self, config: Config, delay_queue: DelayQueue):
        self._config = config
        self._delay_queue = delay_queue

    def process(self, path: Path) -> None:
        if not self._is_valid(path):
            return

        delay_seconds = self._config.get_delay_minutes() * 60

        if delay_seconds > DELAY_SECONDS_MINIMUM:
            self._schedule(path, delay_seconds)
        else:
            self._move(path)

    def move_pending(self) -> None:
        self._delay_queue.execute_all_now()

    def update_config(self, config: Config) -> None:
        self._config = config

    def _schedule(self, path: Path, delay_seconds: float) -> None:
        logger.info(f"Scheduled move for {path.name} in {self._config.get_delay_minutes()} minutes")
        self._delay_queue.schedule(path, delay_seconds, lambda: self._move(path))

    def _move(self, path: Path) -> None:
        if not path.exists():
            logger.debug(f"File no longer exists: {path}")
            return

        category = get_category(path, self._config)
        destination = resolve_destination(category, self._config)

        logger.info(f"Processing {path.name} as {category}")

        organize_download(path, destination, self._config)

    def _is_valid(self, path: Path) -> bool:
        if not path.exists():
            logger.debug(f"File does not exist: {path}")
            return False

        if path.is_dir():
            logger.debug(f"Is directory, skipping: {path}")
            return False

        if not is_inside_downloads(path):
            logger.debug(f"Not inside Downloads folder: {path}")
            return False

        if path.suffix.lower() in PARTIAL_EXTENSIONS:
            logger.debug(f"Ignoring partial download: {path}")
            return False

        return True
