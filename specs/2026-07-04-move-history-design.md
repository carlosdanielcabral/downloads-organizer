# Move History — Design Spec

**Date:** 2026-07-04  
**Status:** Approved

---

## Overview

Add a persistent history of successfully moved files, displayed in a scrollable section in the Monitoramento tab, below the Status section. History entries are retained for a configurable number of days (default: 30).

---

## Data Layer — `lib/history/`

### `MovedFile` (`lib/history/moved_file.py`)

Dataclass representing a single history entry:

```
source_name: str       # original filename
destination: Path      # full path where the file was placed
moved_at: datetime     # UTC timestamp of the successful move
```

### `MoveHistory` (`lib/history/move_history.py`)

Single-responsibility class managing read/write of the history file.

**Constructor:** `MoveHistory(history_path: Path, config: Config)`
- Loads existing entries from `history_path` on init.
- Calls `purge_old_entries()` on init to discard stale records.

**Public interface:**
- `record(source_name: str, destination: Path) -> None` — appends an entry, purges old entries, persists to disk, fires `_on_change`.
- `get_all() -> list[MovedFile]` — returns all entries sorted newest-first.
- `set_on_change(callback: Callable[[], None]) -> None`
- `clear_on_change() -> None`
- `purge_old_entries() -> None` — removes entries older than `config.get_history_retention_days()` days.

**Persistence format:** JSON array at `history.json` (project root, alongside `config.json`):

```json
[
  {
    "source_name": "relatorio.pdf",
    "destination": "C:/Docs/PDFs/relatorio.pdf",
    "moved_at": "2026-07-03T14:32:00"
  }
]
```

---

## Configuration

Add to `Config`:
- `get_history_retention_days() -> int` — default `30`
- `set_history_retention_days(days: int) -> None`

Add `"history_retention_days": 30` to `default_config.json`.

---

## Integration — `FileProcessor`

`MoveHistory` injected via constructor (alongside existing dependencies):

```python
def __init__(self, config, delay_queue, notification_service, file_mover, move_history):
```

In `_move()`, after the notification (to avoid adding latency to the toast):

```python
moved_to = self._file_mover.move(path, destination)

if moved_to:
    if self._config.get_enable_notifications():
        self._notification_service.notify_file_moved(path.name, moved_to)

    self._move_history.record(path.name, moved_to)
```

`record()` runs on the worker thread — no UI blocking.

---

## Assembly — `FileEventWatcherFactory`

```python
move_history = MoveHistory(history_path, config)
processor = FileProcessor(config, delay_queue, notification_service, file_mover, move_history)
```

`history_path` (`Path(__file__).parent.parent / "history.json"`) resolved in `main.py` and passed to `FileEventWatcherFactory.create()`.

`FileEventWatcherFactory.create()` signature gains `move_history: MoveHistory` parameter.

---

## UI — `HistorySection` (`view/tabs/monitoring/history_section.py`)

- Receives `MoveHistory` in constructor.
- Registers `set_on_change` observer on init; `unregister_observer()` calls `clear_on_change()`.
- Renders a `CTkScrollableFrame` with one row per entry, newest first.
- Each row: `"filename  →  /path/to/destination  —  DD/MM/YYYY HH:MM"`
- Empty state: gray label "Nenhum arquivo movido ainda."
- On `_on_change` callback (worker thread): schedules `after(0, self._refresh)` — same pattern as `StatusSection`.

---

## UI — `MonitoringTab` changes

- Constructor receives `move_history: MoveHistory`.
- Section order: Status → **Histórico** → Configurações.
- `unregister_observer()` also calls `self._history_section.unregister_observer()`.

`ConfigWindow` and `GuiManager` propagate `move_history` down to `MonitoringTab`.

---

## Files changed / created

| Action  | Path |
|---------|------|
| Create  | `lib/history/__init__.py` |
| Create  | `lib/history/moved_file.py` |
| Create  | `lib/history/move_history.py` |
| Modify  | `lib/config/config.py` |
| Modify  | `default_config.json` |
| Modify  | `lib/processing/file_processor.py` |
| Modify  | `lib/watcher/file_event_watcher_factory.py` |
| Modify  | `main.py` |
| Create  | `view/tabs/monitoring/history_section.py` |
| Modify  | `view/tabs/monitoring/monitoring_tab.py` |
| Modify  | `view/gui.py` |
| Modify  | `view/gui_manager.py` |

---

## Testing

- Unit tests for `MoveHistory`: record, get_all ordering, purge_old_entries, persistence round-trip, on_change callback.
- Unit tests for `MovedFile` serialization/deserialization.
