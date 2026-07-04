import logging
import threading
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer

from lib.config.config import Config
from lib.watcher.file_event_handler import FileEventHandler
from lib.processing.file_processor import FileProcessor
from lib.queue.file_queue import FileQueue

logger = logging.getLogger(__name__)

DEBOUNCE_SECONDS = 1.5
DEQUEUE_TIMEOUT_SECONDS = 1.0


class FileEventWatcher:
    """
    Orchestrates file system monitoring and coordinates file processing.

    Owns the pause state and manages the lifecycle of the watchdog Observer,
    the FileEventHandler, and the processing worker thread. Exposes a
    high-level interface for start, stop, pause, resume and move_pending_files.

    File events flow through a debounce mechanism in the worker loop before
    being dispatched to the FileProcessor.
    """

    def __init__(
        self,
        watch_path: Path,
        queue: FileQueue,
        paused_event: threading.Event,
        processor: FileProcessor,
        handler: FileEventHandler,
    ):
        self._watch_path = watch_path
        self._queue = queue
        self._paused_event = paused_event
        self._processor = processor
        self._handler = handler
        self._observer: Optional[Observer] = None
        self._worker: Optional[threading.Thread] = None
        self._stopped = False
        self._debounce_timers: dict[str, threading.Timer] = {}

    def start(self) -> None:
        self._stopped = False
        self._start_observer()
        self._start_worker()

        logger.info(f"Watching: {self._watch_path}")

    def stop(self) -> None:
        self._stopped = True
        self._stop_observer()

        logger.info("Watcher stopped")

    def pause(self) -> None:
        self._paused_event.set()

    def resume(self) -> None:
        self._paused_event.clear()

    def is_paused(self) -> bool:
        return self._paused_event.is_set()

    def move_pending_files(self) -> None:
        self._processor.move_pending()

    def update_config(self, config: Config) -> None:
        self._processor.update_config(config)

    def _start_observer(self) -> None:
        self._observer = Observer()
        self._observer.schedule(self._handler, str(self._watch_path), recursive=False)
        self._observer.start()

    def _stop_observer(self) -> None:
        if self._observer:
            self._observer.stop()
            self._observer.join()

    def _start_worker(self) -> None:
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()

    def _run(self) -> None:
        while not self._stopped:
            path = self._queue.dequeue(timeout=DEQUEUE_TIMEOUT_SECONDS)

            if path is None:
                continue

            self._debounce(path)

    def _debounce(self, path: Path) -> None:
        file_key = str(path)

        existing_timer = self._debounce_timers.get(file_key)

        if existing_timer:
            existing_timer.cancel()

        timer = threading.Timer(DEBOUNCE_SECONDS, lambda: self._dispatch(path))
        self._debounce_timers[file_key] = timer
        timer.start()

    def _dispatch(self, path: Path) -> None:
        self._debounce_timers.pop(str(path), None)

        if self._paused_event.is_set():
            logger.debug(f"Watcher paused, skipping: {path}")
            return

        self._processor.process(path)
