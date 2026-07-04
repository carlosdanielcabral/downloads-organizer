import logging
from pathlib import Path

from lib.config.config import Config
from lib.queue.delay_queue import DelayQueue
from lib.processing.file_mover import FileMover
from lib.notifications.notifications import NotificationService
from lib.processing.paths import is_inside_downloads, resolve_destination
from lib.processing.rules import PARTIAL_EXTENSIONS, get_category

logger = logging.getLogger(__name__)

DELAY_SECONDS_MINIMUM = 0


class FileProcessor:
    """
    Processes files detected in the Downloads folder.

    Validates each file, then schedules it to be moved after the configured
    delay. If the delay is zero, the move is executed immediately. All
    pending moves can be forced to execute immediately via move_pending.
    """

    def __init__(self, config: Config, delay_queue: DelayQueue, notification_service: NotificationService, file_mover: FileMover):
        self._config = config
        self._delay_queue = delay_queue
        self._notification_service = notification_service
        self._file_mover = file_mover

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

    def cancel(self, path: Path) -> None:
        self._delay_queue.cancel(path)

    def execute_now(self, path: Path) -> None:
        self._delay_queue.execute_now(path)

    def get_delay_queue(self):
        return self._delay_queue

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

        moved_to = self._file_mover.move(path, destination)

        if moved_to and self._config.get_enable_notifications():
            self._notification_service.notify_file_moved(path.name, moved_to)

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
