from pathlib import Path

from watchdog.events import FileSystemEventHandler

from lib.queue.file_queue import FileQueue


class FileEventHandler(FileSystemEventHandler):
    """
    Watchdog event handler responsible solely for detecting file system
    events and enqueuing the affected paths for processing.

    Ignores directory events and partial download files. Does not perform
    any file processing — its only responsibility is to feed the FileQueue.
    """

    def __init__(self, queue: FileQueue):
        super().__init__()
        self._queue = queue

    def on_created(self, event) -> None:
        if event.is_directory:
            return

        self._queue.enqueue(Path(event.src_path))

    def on_moved(self, event) -> None:
        if event.is_directory:
            return

        self._queue.enqueue(Path(event.dest_path))
