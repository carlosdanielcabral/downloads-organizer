import logging
import os
from pathlib import Path

from lib.config.config import Config
from lib.history.move_history import MoveHistory
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
    history_path = Path(__file__).parent / "history.json"

    notification_service = NotificationService()
    notification_service.start()

    move_history = MoveHistory(history_path, config)

    watcher = FileEventWatcherFactory.create(downloads_folder, config, notification_service, move_history)
    watcher.start()

    def reload_config():
        new_config = Config.load(config_path)
        watcher.update_config(new_config)

    gui_manager = GuiManager(
        watcher=watcher,
        config=config,
        config_path=config_path,
        reload_config_callback=reload_config,
        move_history=move_history,
    )

    gui_manager.open_window()

    tray = TrayIcon(watcher=watcher, gui_manager=gui_manager)

    gui_manager.set_quit_callback(tray.stop)

    try:
        tray.run()
    except KeyboardInterrupt:
        watcher.stop()
    finally:
        notification_service.stop()
        move_history.stop()
        os._exit(0)


if __name__ == "__main__":
    main()
