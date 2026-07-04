import queue
from pathlib import Path


class FileQueue:
    """
    Thread-safe queue for passing detected file paths between the event
    handler and the file processing worker.

    Wraps the standard library queue.Queue, exposing a domain-specific
    interface that hides the underlying implementation.
    """

    def __init__(self):
        self._queue: queue.Queue[Path] = queue.Queue()

    def enqueue(self, path: Path) -> None:
        self._queue.put(path)

    def dequeue(self, timeout: float = 1.0) -> Path | None:
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None
