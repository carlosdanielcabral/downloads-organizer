from enum import Enum
from pathlib import Path


class Category(Enum):
    IMAGES = "IMAGES"
    VIDEOS = "VIDEOS"
    AUDIO = "AUDIO"
    DOCUMENTS = "DOCUMENTS"
    OTHER = "OTHER"


EXTENSION_MAP = {
    "png": Category.IMAGES,
    "jpg": Category.IMAGES,
    "jpeg": Category.IMAGES,
    "gif": Category.IMAGES,
    "webp": Category.IMAGES,
    "bmp": Category.IMAGES,
    "svg": Category.IMAGES,
    "ico": Category.IMAGES,
    "tiff": Category.IMAGES,
    "mp4": Category.VIDEOS,
    "mkv": Category.VIDEOS,
    "avi": Category.VIDEOS,
    "mov": Category.VIDEOS,
    "wmv": Category.VIDEOS,
    "webm": Category.VIDEOS,
    "flv": Category.VIDEOS,
    "mp3": Category.AUDIO,
    "wav": Category.AUDIO,
    "flac": Category.AUDIO,
    "ogg": Category.AUDIO,
    "m4a": Category.AUDIO,
    "aac": Category.AUDIO,
    "wma": Category.AUDIO,
    "pdf": Category.DOCUMENTS,
    "doc": Category.DOCUMENTS,
    "docx": Category.DOCUMENTS,
    "xls": Category.DOCUMENTS,
    "xlsx": Category.DOCUMENTS,
    "ppt": Category.DOCUMENTS,
    "pptx": Category.DOCUMENTS,
    "txt": Category.DOCUMENTS,
    "md": Category.DOCUMENTS,
    "csv": Category.DOCUMENTS,
    "rtf": Category.DOCUMENTS,
    "exe": Category.DOCUMENTS,
    "msi": Category.DOCUMENTS,
    "bat": Category.DOCUMENTS,
    "cmd": Category.DOCUMENTS,
    "ps1": Category.DOCUMENTS,
    "zip": Category.DOCUMENTS,
    "rar": Category.DOCUMENTS,
    "7z": Category.DOCUMENTS,
    "tar": Category.DOCUMENTS,
    "gz": Category.DOCUMENTS,
}


PARTIAL_EXTENSIONS = {".crdownload", ".part", ".tmp", ".download"}


def get_category(file_path: Path) -> Category:
    extension = file_path.suffix.lower().lstrip(".")

    return EXTENSION_MAP.get(extension, Category.OTHER)
