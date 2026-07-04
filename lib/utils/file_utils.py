import shutil
import time
from pathlib import Path


def is_file_locked(path: Path) -> bool:
    """
    Checks whether a file is currently locked by another process.

    Attempts to open the file in binary read mode. If the operation fails due
    to an I/O or permission error, the file is considered locked.

    Args:
        path: Path to the file to check.

    Returns:
        True if the file is locked, False otherwise.
    """
    try:
        with open(path, "rb"):
            return False
    except (IOError, PermissionError):
        return True


def wait_until_unlocked(path: Path, *, max_retries: int = 15, delay: float = 2.0) -> bool:
    """
    Waits until a file is no longer locked, retrying at regular intervals.

    Args:
        path: Path to the file to monitor.
        max_retries: Maximum number of attempts before giving up. Defaults to 15.
        delay: Seconds to wait between each attempt. Defaults to 2.0.

    Returns:
        True if the file became unlocked within the allowed attempts,
        False if it remained locked after all retries.
    """
    for attempt in range(max_retries):
        if not is_file_locked(path):
            return True

        time.sleep(delay)

    return False


def resolve_unique_path(directory: Path, filename: str) -> Path:
    """
    Resolves a non-conflicting file path within a directory.

    If a file with the given name already exists in the directory, appends an
    incrementing counter suffix to the stem (e.g. "file (1).txt", "file (2).txt")
    until a free name is found.

    Args:
        directory: Target directory where the file will be placed.
        filename: Desired filename including extension.

    Returns:
        A Path that does not yet exist in the directory.
    """
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
    """
    Moves a file or directory from source to destination.

    Args:
        source: Path to the file or directory to move.
        destination: Target path including the desired final name.

    Raises:
        FileNotFoundError: If the source path does not exist.
    """
    if not source.exists():
        raise FileNotFoundError(f"Source file does not exist: {source}")

    shutil.move(str(source), str(destination))
