import threading
from pathlib import Path

from lib.config.config import Config
from lib.history.move_history import MoveHistory
from lib.notifications.notifications import NotificationService
from lib.processing.file_mover import FileMover
from lib.processing.file_processor import FileProcessor
from lib.queue.delay_queue import DelayQueue
from lib.queue.file_queue import FileQueue
from lib.watcher.file_event_handler import FileEventHandler
from lib.watcher.file_event_watcher import FileEventWatcher


class FileEventWatcherFactory:
    """
    Responsible for assembling a fully configured FileEventWatcher.

    Centralizes the construction of all internal dependencies, keeping
    the FileEventWatcher constructor free of assembly logic and making
    each component independently substitutable for testing.
    """

    @staticmethod
    def create(watch_path: Path, config: Config, notification_service: NotificationService, move_history: MoveHistory) -> FileEventWatcher:
        file_queue = FileQueue()
        delay_queue = DelayQueue()
        file_mover = FileMover()
        paused_event = threading.Event()
        processor = FileProcessor(config, delay_queue, notification_service, file_mover, move_history)
        handler = FileEventHandler(file_queue)

        return FileEventWatcher(watch_path, file_queue, paused_event, processor, handler)
