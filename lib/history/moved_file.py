from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


@dataclass(frozen=True)
class MovedFile:
    """
    Immutable record of a successfully moved file.

    Carries the original filename, the full destination path and the
    datetime at which the move occurred. Used by MoveHistory to persist
    and display the move history.
    """

    source_name: str
    destination: Path
    moved_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_name": self.source_name,
            "destination": str(self.destination),
            "moved_at": self.moved_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MovedFile":
        return cls(
            source_name=data["source_name"],
            destination=Path(data["destination"]),
            moved_at=datetime.fromisoformat(data["moved_at"]),
        )
