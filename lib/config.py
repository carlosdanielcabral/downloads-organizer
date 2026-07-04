import json
from pathlib import Path
from typing import Dict, Any


class Config:
    DEFAULT_CONFIG = {
        "extension_mappings": {
            "png": "IMAGES",
            "jpg": "IMAGES",
            "jpeg": "IMAGES",
            "gif": "IMAGES",
            "webp": "IMAGES",
            "bmp": "IMAGES",
            "svg": "IMAGES",
            "ico": "IMAGES",
            "tiff": "IMAGES",
            "mp4": "VIDEOS",
            "mkv": "VIDEOS",
            "avi": "VIDEOS",
            "mov": "VIDEOS",
            "wmv": "VIDEOS",
            "webm": "VIDEOS",
            "flv": "VIDEOS",
            "mp3": "AUDIO",
            "wav": "AUDIO",
            "flac": "AUDIO",
            "ogg": "AUDIO",
            "m4a": "AUDIO",
            "aac": "AUDIO",
            "wma": "AUDIO",
            "pdf": "DOCUMENTS",
            "doc": "DOCUMENTS",
            "docx": "DOCUMENTS",
            "xls": "DOCUMENTS",
            "xlsx": "DOCUMENTS",
            "ppt": "DOCUMENTS",
            "pptx": "DOCUMENTS",
            "txt": "DOCUMENTS",
            "md": "DOCUMENTS",
            "csv": "DOCUMENTS",
            "rtf": "DOCUMENTS",
            "exe": "DOCUMENTS",
            "msi": "DOCUMENTS",
            "bat": "DOCUMENTS",
            "cmd": "DOCUMENTS",
            "ps1": "DOCUMENTS",
            "zip": "DOCUMENTS",
            "rar": "DOCUMENTS",
            "7z": "DOCUMENTS",
            "tar": "DOCUMENTS",
            "gz": "DOCUMENTS",
        },
        "folder_mappings": {
            "IMAGES": "Imagens/Downloads",
            "VIDEOS": "Vídeos/Downloads",
            "AUDIO": "Músicas/Downloads",
            "DOCUMENTS": "Documentos/Downloads",
            "OTHER": "Downloads/Outros",
        },
        "watch_folder": None,
    }

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def default(cls) -> "Config":
        return cls(cls.DEFAULT_CONFIG.copy())

    def get_extension_category(self, extension: str) -> str:
        return self.data["extension_mappings"].get(extension.lower(), "OTHER")

    def get_folder_path(self, category: str) -> str:
        return self.data["folder_mappings"].get(category, "Downloads/Outros")

    def set_extension_category(self, extension: str, category: str) -> None:
        self.data["extension_mappings"][extension.lower()] = category

    def set_folder_path(self, category: str, path: str) -> None:
        self.data["folder_mappings"][category] = path

    def set_watch_folder(self, path: str) -> None:
        self.data["watch_folder"] = path

    def get_watch_folder(self) -> str:
        return self.data["watch_folder"]

    def save(self, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> "Config":
        if not path.exists():
            return cls.default()

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(data)
