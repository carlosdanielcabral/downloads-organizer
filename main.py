import logging
from pathlib import Path

from lib.config.config import Config
from lib.notifications.notifications import NotificationService
from lib.processing.paths import get_downloads_folder
from lib.watcher.file_event_watcher_factory import FileEventWatcherFactory
from view.gui_manager import GuiManager
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

    def reload_config():
        new_config = Config.load(config_path)
        watcher.update_config(new_config)

    gui_manager = GuiManager(
        watcher=watcher,
        config=config,
        config_path=config_path,
        reload_config_callback=reload_config,
    )

    gui_manager.open_window()

    tray = TrayIcon(watcher=watcher, gui_manager=gui_manager)

    try:
        tray.run()
    except KeyboardInterrupt:
        watcher.stop()
    finally:
        notification_service.stop()


if __name__ == "__main__":
    main()
