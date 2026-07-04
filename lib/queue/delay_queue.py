from pathlib import Path
from typing import Callable

from lib.queue.delayed_task import DelayedTask
from lib.queue.pending_file import PendingFile


class DelayQueue:
    """
    Manages a set of file move operations that are waiting for a configured
    delay before being executed.

    Each file is associated with a DelayedTask that can be cancelled or
    forced to execute immediately. Scheduling a path that is already
    pending automatically replaces the previous task.

    Observers can subscribe via set_on_change to be notified whenever the
    queue is mutated (schedule, cancel or execute). The callback is called
    from whichever thread triggered the mutation, so callers must ensure
    thread-safe UI updates (e.g. tkinter's after(0, ...)).
    """

    def __init__(self):
        self._tasks: dict[str, DelayedTask] = {}
        self._on_change: Callable[[], None] | None = None

    def set_on_change(self, callback: Callable[[], None]) -> None:
        self._on_change = callback

    def clear_on_change(self) -> None:
        self._on_change = None

    def schedule(self, path: Path, delay: float, on_execute: Callable[[], None]) -> None:
        self._cancel_existing(path)

        task = DelayedTask(delay, lambda: self._on_task_executed(path, on_execute))
        self._tasks[str(path)] = task
        task.start()

        self._notify()

    def cancel(self, path: Path) -> None:
        self._cancel_existing(path)
        self._notify()

    def execute_now(self, path: Path) -> None:
        task = self._tasks.pop(str(path), None)

        if task:
            task.execute_now()
            self._notify()

    def execute_all_now(self) -> None:
        for task in list(self._tasks.values()):
            task.execute_now()

        self._tasks.clear()
        self._notify()

    def get_pending(self) -> list[PendingFile]:
        return [
            PendingFile(path=Path(path_key), scheduled_for=task.scheduled_for)
            for path_key, task in self._tasks.items()
        ]

    def _on_task_executed(self, path: Path, on_execute: Callable[[], None]) -> None:
        self._tasks.pop(str(path), None)
        on_execute()
        self._notify()

    def _cancel_existing(self, path: Path) -> None:
        task = self._tasks.pop(str(path), None)

        if task:
            task.cancel()

    def _notify(self) -> None:
        if self._on_change:
            self._on_change()
