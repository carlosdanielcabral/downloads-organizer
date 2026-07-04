import json
import sys
from pathlib import Path
from typing import Dict, Any


def _get_default_config_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS) / "default_config.json"

    return Path(__file__).parent.parent / "default_config.json"


DEFAULT_CONFIG_PATH = _get_default_config_path()


class Config:
    """
    Represents the application configuration.

    Holds the mappings between file extensions and categories, categories and
    destination folder paths, as well as general settings such as the watched
    folder, notification preferences and delay before moving files.

    Can be loaded from a JSON file via `load`, falling back to the bundled
    defaults via `default`, and persisted back to disk via `save`.
    """

    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def default(cls) -> "Config":
        with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        return cls(data)

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

    def set_enable_notifications(self, enabled: bool) -> None:
        self.data["enable_notifications"] = enabled

    def get_enable_notifications(self) -> bool:
        return self.data.get("enable_notifications", True)

    def set_delay_minutes(self, minutes: int) -> None:
        self.data["delay_minutes"] = minutes

    def get_delay_minutes(self) -> int:
        return self.data.get("delay_minutes", 30)

    def get_history_retention_days(self) -> int:
        return self.data.get("history_retention_days", 30)

    def set_history_retention_days(self, days: int) -> None:
        self.data["history_retention_days"] = days

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
