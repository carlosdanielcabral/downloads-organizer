import threading
from datetime import datetime, timedelta
from typing import Callable


class DelayedTask:
    """
    Represents a single action scheduled to run after a delay.

    Wraps a threading.Timer to allow the action to be cancelled before
    it fires or executed immediately, bypassing the remaining wait time.
    """

    def __init__(self, delay: float, on_execute: Callable[[], None]):
        self._on_execute = on_execute
        self._timer = threading.Timer(delay, on_execute)
        self.scheduled_for: datetime = datetime.now() + timedelta(seconds=delay)

    def start(self) -> None:
        self._timer.start()

    def cancel(self) -> None:
        self._timer.cancel()

    def execute_now(self) -> None:
        self._timer.cancel()
        self._on_execute()
