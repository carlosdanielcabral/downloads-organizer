import os
from pathlib import Path

from lib.config.config import Config


def get_user_home() -> Path:
    return Path(os.environ.get("USERPROFILE", Path.home()))


def get_downloads_folder() -> Path:
    return get_user_home() / "Downloads"


def resolve_destination(category: str, config: Config) -> Path:
    relative_path = config.get_folder_path(category)
    destination = get_user_home() / relative_path

    destination.mkdir(parents=True, exist_ok=True)

    return destination


def is_inside_downloads(path: Path) -> bool:
    downloads_folder = get_downloads_folder()

    try:
        path.resolve().relative_to(downloads_folder.resolve())
        return True
    except ValueError:
        return False
