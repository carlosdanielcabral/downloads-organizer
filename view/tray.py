import subprocess
import sys
from pathlib import Path

import pystray

from lib.watcher.file_event_watcher import FileEventWatcher
from view.icon import create_icon


class TrayIcon:
    """
    System tray icon for the Download Organizer application.

    Manages the tray icon lifecycle, builds the context menu, and delegates
    user actions (pause/resume, move now, open settings, quit) to the
    appropriate components.
    """

    def __init__(self, watcher: FileEventWatcher, config_path: Path, ipc_port: int):
        self._watcher = watcher
        self._config_path = config_path
        self._ipc_port = ipc_port
        self._icon = pystray.Icon(
            "download_organizer",
            create_icon(),
            "Download Organizer",
            menu=self._build_menu(is_paused=False)
        )

    def run(self) -> None:
        self._icon.run()

    def stop(self) -> None:
        self._icon.stop()

    def _build_menu(self, *, is_paused: bool) -> pystray.Menu:
        if is_paused:
            status_label = "Pausado"
            toggle_label = "Retomar"
        else:
            status_label = "Monitorando"
            toggle_label = "Pausar"

        return pystray.Menu(
            pystray.MenuItem(status_label, None, enabled=False),
            pystray.MenuItem(toggle_label, self._on_pause_toggle),
            pystray.MenuItem("Mover Agora", self._on_move_now),
            pystray.MenuItem("Configurações", self._on_config),
            pystray.MenuItem("Sair", self._on_quit)
        )

    def _on_pause_toggle(self, icon, item):
        if self._watcher.is_paused():
            self._watcher.resume()
        else:
            self._watcher.pause()

        icon.menu = self._build_menu(is_paused=self._watcher.is_paused())

    def _on_move_now(self, icon, item):
        self._watcher.move_pending_files()

    def _on_config(self, icon, item):
        config_path = self._config_path
        ipc_port = self._ipc_port

        subprocess.Popen([sys.executable, "-c", f"from view.gui import show_config_window; from lib.config.config import Config; from lib.ipc.ipc_client import send_move_now, send_reload_config; from pathlib import Path; config = Config.load(Path(r'{config_path}')); show_config_window(config, Path(r'{config_path}'), move_now_callback=lambda: send_move_now({ipc_port}), reload_config_callback=lambda: send_reload_config({ipc_port}))"])

    def _on_quit(self, icon, item):
        self._watcher.stop()
        self._icon.stop()
