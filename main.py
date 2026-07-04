import logging
import threading
from pathlib import Path

from lib.config import Config
from lib.paths import get_downloads_folder
from view.tray import run_tray
from lib.watcher import DownloadWatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    config_path = Path(__file__).parent / "config.json"
    config = Config.load(config_path)

    paused = threading.Event()
    downloads_folder = get_downloads_folder()

    watcher = DownloadWatcher(downloads_folder, paused, config)
    watcher.start()

    try:
        run_tray(watcher, paused, config, config_path)
    except KeyboardInterrupt:
        watcher.stop()


if __name__ == "__main__":
    main()
