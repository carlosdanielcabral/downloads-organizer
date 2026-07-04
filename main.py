import logging
from pathlib import Path

from lib.config.config import Config
from lib.watcher.file_event_watcher_factory import FileEventWatcherFactory
from lib.ipc.ipc_server import IpcServer, COMMAND_MOVE_NOW, COMMAND_RELOAD_CONFIG
from lib.notifications.notifications import NotificationService
from lib.processing.paths import get_downloads_folder
from view.tray import TrayIcon

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def main():
    config_path = Path(__file__).parent / "config.json"
    config = Config.load(config_path)

    downloads_folder = get_downloads_folder()

    notification_service = NotificationService()
    notification_service.start()

    watcher = FileEventWatcherFactory.create(downloads_folder, config, notification_service)
    watcher.start()

    ipc_server = IpcServer()
    ipc_server.register_handler(
        COMMAND_MOVE_NOW,
        lambda: watcher.move_pending_files()
    )

    def reload_config():
        new_config = Config.load(config_path)
        watcher.update_config(new_config)

    ipc_server.register_handler(COMMAND_RELOAD_CONFIG, reload_config)
    ipc_server.start()

    tray = TrayIcon(watcher, config_path, ipc_server.get_port())

    try:
        tray.run()
    except KeyboardInterrupt:
        watcher.stop()
    finally:
        ipc_server.stop()
        notification_service.stop()


if __name__ == "__main__":
    main()
