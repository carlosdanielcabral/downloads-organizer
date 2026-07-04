import pystray

from lib.watcher.file_event_watcher import FileEventWatcher
from view.gui_manager import GuiManager
from view.icon import create_icon


class TrayIcon:
    """
    System tray icon for the Download Organizer application.

    Manages the tray icon lifecycle, builds the context menu, and delegates
    user actions (pause/resume, move now, open settings, quit) to the
    appropriate components. Left-clicking the icon opens the configuration
    window via GuiManager.
    """

    def __init__(self, watcher: FileEventWatcher, gui_manager: GuiManager):
        self._watcher = watcher
        self._gui_manager = gui_manager
        self._icon = pystray.Icon(
            "download_organizer",
            create_icon(),
            "Download Organizer",
            menu=self._build_menu(is_paused=False),
        )
        self._icon.on_activate = self._on_left_click

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
            pystray.MenuItem("Configurações", self._on_open_window, default=True),
            pystray.MenuItem("Sair", self._on_quit),
        )

    def _on_pause_toggle(self, icon, item) -> None:
        if self._watcher.is_paused():
            self._watcher.resume()
        else:
            self._watcher.pause()

        icon.menu = self._build_menu(is_paused=self._watcher.is_paused())

    def _on_move_now(self, icon, item) -> None:
        self._watcher.move_pending_files()

    def _on_open_window(self, icon, item) -> None:
        self._gui_manager.open_window()

    def _on_quit(self, icon, item) -> None:
        self._watcher.stop()
        self._icon.stop()
