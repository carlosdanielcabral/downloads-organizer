from pathlib import Path
from typing import Callable

from lib.delayed_task import DelayedTask


class DelayQueue:
    """
    Manages a set of file move operations that are waiting for a configured
    delay before being executed.

    Each file is associated with a DelayedTask that can be cancelled or
    forced to execute immediately. Scheduling a path that is already
    pending automatically replaces the previous task.
    """

    def __init__(self):
        self._tasks: dict[str, DelayedTask] = {}

    def schedule(self, path: Path, delay: float, on_execute: Callable[[], None]) -> None:
        self._cancel_existing(path)

        task = DelayedTask(delay, on_execute)
        self._tasks[str(path)] = task
        task.start()

    def cancel(self, path: Path) -> None:
        self._cancel_existing(path)

    def execute_all_now(self) -> None:
        for task in list(self._tasks.values()):
            task.execute_now()

        self._tasks.clear()

    def _cancel_existing(self, path: Path) -> None:
        task = self._tasks.pop(str(path), None)

        if task:
            task.cancel()
