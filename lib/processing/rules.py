from pathlib import Path

from lib.config.config import Config


PARTIAL_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}


def get_category(file_path: Path, config: Config) -> str:
    extension = file_path.suffix.lower().lstrip(".")

    return config.get_extension_category(extension)
