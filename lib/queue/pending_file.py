from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class PendingFile:
    """
    Immutable snapshot of a file waiting to be moved.

    Carries the file path and the datetime at which the move is scheduled
    to occur. Used by the GUI to display queue status without exposing
    internal queue implementation details.
    """

    path: Path
    scheduled_for: datetime
