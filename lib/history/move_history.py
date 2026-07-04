import json
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

from lib.history.moved_file import MovedFile

logger = logging.getLogger(__name__)

PURGE_INTERVAL_SECONDS = 86400


class MoveHistory:
    """
    Manages the persistent history of successfully moved files.

    Loads existing entries from a JSON file on init, purges entries older
    than the configured retention period, and persists changes to disk on
    every record call. A daily timer ensures stale entries are removed even
    when no new files are moved. Observers can subscribe via set_on_change
    to be notified whenever a new entry is recorded.
    """

    def __init__(self, history_path: Path, config):
        self._history_path = history_path
        self._config = config
        self._on_change: Callable[[], None] | None = None
        self._timer: threading.Timer | None = None
        self._entries: list[MovedFile] = self._load()

        self._purge_old_entries()
        self._schedule_daily_purge()

    def record(self, source_name: str, destination: Path) -> None:
        entry = MovedFile(
            source_name=source_name,
            destination=destination,
            moved_at=datetime.now(),
        )

        self._entries.append(entry)
        self._purge_old_entries()
        self._persist()
        self._notify()

    def get_all(self) -> list[MovedFile]:
        return list(reversed(self._entries))

    def set_on_change(self, callback: Callable[[], None]) -> None:
        self._on_change = callback

    def clear_on_change(self) -> None:
        self._on_change = None

    def stop(self) -> None:
        if self._timer:
            self._timer.cancel()
            self._timer = None

    def _schedule_daily_purge(self) -> None:
        self._timer = threading.Timer(PURGE_INTERVAL_SECONDS, self._on_daily_purge)
        self._timer.daemon = True
        self._timer.start()

    def _on_daily_purge(self) -> None:
        self._purge_old_entries()
        self._persist()
        self._schedule_daily_purge()

    def _purge_old_entries(self) -> None:
        retention_days = self._config.get_history_retention_days()
        cutoff = datetime.now() - timedelta(days=retention_days)

        self._entries = [
            entry for entry in self._entries if entry.moved_at >= cutoff
        ]

    def _persist(self) -> None:
        try:
            data = [entry.to_dict() for entry in self._entries]
            self._history_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError:
            logger.warning(f"Failed to persist history to {self._history_path}")

    def _load(self) -> list[MovedFile]:
        if not self._history_path.exists():
            return []

        try:
            data = json.loads(self._history_path.read_text(encoding="utf-8"))

            return [MovedFile.from_dict(item) for item in data]
        except (OSError, json.JSONDecodeError, KeyError):
            logger.warning(f"Failed to load history from {self._history_path}, starting fresh")

            return []

    def _notify(self) -> None:
        if self._on_change:
            self._on_change()
