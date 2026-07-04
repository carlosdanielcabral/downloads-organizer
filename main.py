import logging
from pathlib import Path

from lib.config import Config
from lib.ipc_server import IpcServer, COMMAND_MOVE_NOW, COMMAND_RELOAD_CONFIG
from lib.paths import get_downloads_folder
from view.tray import TrayIcon
from lib.watcher import DownloadWatcher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    config_path = Path(__file__).parent / "config.json"
    config = Config.load(config_path)

    downloads_folder = get_downloads_folder()

    watcher = DownloadWatcher(downloads_folder, config)
    watcher.start()

    ipc_server = IpcServer()
    ipc_server.register_handler(
        COMMAND_MOVE_NOW,
        lambda: watcher.handler.move_pending_files() if watcher.handler else None
    )

    def reload_config():
        new_config = Config.load(config_path)
        watcher.config = new_config

        if watcher.handler:
            watcher.handler.update_config(new_config)

    ipc_server.register_handler(COMMAND_RELOAD_CONFIG, reload_config)
    ipc_server.start()

    tray = TrayIcon(watcher, config_path, ipc_server.get_port())

    try:
        tray.run()
    except KeyboardInterrupt:
        watcher.stop()
    finally:
        ipc_server.stop()


if __name__ == "__main__":
    main()
