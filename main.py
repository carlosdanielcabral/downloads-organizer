import logging
import threading
from pathlib import Path

from lib.config import Config
from lib.ipc_server import IpcServer, COMMAND_MOVE_NOW
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

    ipc_server = IpcServer()
    ipc_server.register_handler(
        COMMAND_MOVE_NOW,
        lambda: watcher.handler.move_pending_files() if watcher.handler else None
    )
    ipc_server.start()

    try:
        run_tray(watcher, paused, config, config_path, ipc_server.get_port())
    except KeyboardInterrupt:
        watcher.stop()
    finally:
        ipc_server.stop()


if __name__ == "__main__":
    main()
