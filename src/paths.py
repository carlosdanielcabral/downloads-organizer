import os
from pathlib import Path
from typing import Dict

from src.rules import Category


def get_user_home() -> Path:
    return Path(os.environ.get("USERPROFILE", Path.home()))


CATEGORY_FOLDERS: Dict[Category, str] = {
    Category.IMAGES: "Imagens/Downloads",
    Category.VIDEOS: "Vídeos/Downloads",
    Category.AUDIO: "Músicas/Downloads",
    Category.DOCUMENTS: "Documentos/Downloads",
    Category.OTHER: "Downloads/Outros",
}


def get_downloads_folder() -> Path:
    return get_user_home() / "Downloads"


def resolve_destination(category: Category) -> Path:
    relative_path = CATEGORY_FOLDERS[category]
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
