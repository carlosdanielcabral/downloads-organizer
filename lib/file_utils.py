import shutil
import time
from pathlib import Path


def is_file_locked(path: Path) -> bool:
    try:
        with open(path, "rb"):
            return False
    except (IOError, PermissionError):
        return True


def wait_until_unlocked(path: Path, *, max_retries: int = 15, delay: float = 2.0) -> bool:
    for attempt in range(max_retries):
        if not is_file_locked(path):
            return True

        time.sleep(delay)

    return False


def resolve_unique_path(directory: Path, filename: str) -> Path:
    base_path = directory / filename
    stem = base_path.stem
    suffix = base_path.suffix

    if not base_path.exists():
        return base_path

    counter = 1

    while True:
        new_filename = f"{stem} ({counter}){suffix}"
        new_path = directory / new_filename

        if not new_path.exists():
            return new_path

        counter += 1


def move_path(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source}")

    shutil.move(str(source), str(destination))
