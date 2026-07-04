import logging
from pathlib import Path

from src.file_utils import move_path, resolve_unique_path, wait_until_unlocked

logger = logging.getLogger(__name__)


def organize_download(source: Path, dest_folder: Path) -> Path | None:
    if not source.exists():
        return None

    MAX_RETRIES = 15
    RETRY_DELAY = 2.0

    for attempt in range(MAX_RETRIES):
        try:
            if not wait_until_unlocked(source, max_retries=1, delay=RETRY_DELAY):
                logger.debug(f"File still locked, retry {attempt + 1}/{MAX_RETRIES}: {source}")
                continue

            destination = resolve_unique_path(dest_folder, source.name)
            move_path(source, destination)

            logger.info(f"Organizado: {source.name} → {destination}")

            return destination

        except PermissionError as error:
            logger.debug(f"Permission error on attempt {attempt + 1}/{MAX_RETRIES}: {error}")

    logger.warning(f"Falha ao organizar após {MAX_RETRIES} tentativas: {source}")

    return None
