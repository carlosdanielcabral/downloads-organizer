import logging
import threading

from lib.paths import get_downloads_folder
from view.tray import run_tray
from lib.watcher import DownloadWatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    paused = threading.Event()
    downloads_folder = get_downloads_folder()

    watcher = DownloadWatcher(downloads_folder, paused)
    watcher.start()

    try:
        run_tray(watcher, paused)
    except KeyboardInterrupt:
        watcher.stop()


if __name__ == "__main__":
    main()
