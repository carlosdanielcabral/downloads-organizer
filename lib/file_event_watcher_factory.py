import threading
from pathlib import Path

from lib.config import Config
from lib.delay_queue import DelayQueue
from lib.file_event_handler import FileEventHandler
from lib.file_event_watcher import FileEventWatcher
from lib.file_processor import FileProcessor
from lib.file_queue import FileQueue
from lib.notifications import NotificationService


class FileEventWatcherFactory:
    """
    Responsible for assembling a fully configured FileEventWatcher.

    Centralizes the construction of all internal dependencies, keeping
    the FileEventWatcher constructor free of assembly logic and making
    each component independently substitutable for testing.
    """

    @staticmethod
    def create(watch_path: Path, config: Config, notification_service: NotificationService) -> FileEventWatcher:
        file_queue = FileQueue()
        delay_queue = DelayQueue()
        paused_event = threading.Event()
        processor = FileProcessor(config, delay_queue, notification_service)
        handler = FileEventHandler(file_queue)

        return FileEventWatcher(watch_path, file_queue, paused_event, processor, handler)
