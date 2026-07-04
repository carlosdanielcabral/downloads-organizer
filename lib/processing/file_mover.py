import logging
from pathlib import Path

from lib.utils.file_utils import move_path, resolve_unique_path, wait_until_unlocked

logger = logging.getLogger(__name__)

MAX_RETRIES = 15
RETRY_DELAY = 2.0


class FileMover:
    """
    Responsible for moving a file to a destination folder.

    Handles locked files by retrying the operation at regular intervals.
    If the file remains locked after all attempts, the move is aborted
    and None is returned. Resolves name conflicts by appending an
    incrementing suffix to the filename.
    """

    def move(self, source: Path, dest_folder: Path) -> Path | None:
        """
        Moves a file to the given destination folder.

        Waits for the file to be unlocked before attempting the move,
        retrying up to MAX_RETRIES times. Resolves naming conflicts
        automatically.

        Args:
            source: Path to the file to move.
            dest_folder: Target directory where the file will be placed.

        Returns:
            The final Path of the moved file, or None if the move failed.
        """
        logger.info(f"Attempting to move: {source} → {dest_folder}")

        if not source.exists():
            logger.warning(f"Source file does not exist: {source}")

            return None

        for attempt in range(MAX_RETRIES):
            try:
                if not wait_until_unlocked(source, max_retries=1, delay=RETRY_DELAY):
                    logger.debug(f"File still locked, retry {attempt + 1}/{MAX_RETRIES}: {source}")
                    continue

                destination = resolve_unique_path(dest_folder, source.name)
                logger.info(f"Moving to: {destination}")

                move_path(source, destination)

                logger.info(f"Moved: {source.name} → {destination}")

                return destination

            except PermissionError as error:
                logger.debug(f"Permission error on attempt {attempt + 1}/{MAX_RETRIES}: {error}")

        logger.warning(f"Failed to move after {MAX_RETRIES} attempts: {source}")

        return None
