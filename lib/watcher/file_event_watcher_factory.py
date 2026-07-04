import threading
from pathlib import Path

from lib.config.config import Config
from lib.queue.delay_queue import DelayQueue
from lib.watcher.file_event_handler import FileEventHandler
from lib.watcher.file_event_watcher import FileEventWatcher
from lib.processing.file_processor import FileProcessor
from lib.queue.file_queue import FileQueue
from lib.notifications.notifications import NotificationService


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
