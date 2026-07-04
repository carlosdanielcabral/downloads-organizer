import threading
import subprocess
import sys
from pathlib import Path
from PIL import Image

import pystray

from lib.watcher import DownloadWatcher
from lib.config import Config


def create_icon() -> Image.Image:
    icon_path = Path(__file__).parent / "assets" / "icon.png"
    
    if icon_path.exists():
        return Image.open(icon_path)
    
    return Image.new("RGBA", (64, 64), color=(0, 120, 215, 255))


def run_tray(watcher: DownloadWatcher, paused: threading.Event, config: Config, config_path: Path, ipc_port: int) -> None:
    def on_pause_toggle(icon, item):
        if paused.is_set():
            paused.clear()
            icon.menu = pystray.Menu(
                pystray.MenuItem("Monitorando", None, enabled=False),
                pystray.MenuItem("Pausar", on_pause_toggle),
                pystray.MenuItem("Mover Agora", on_move_now),
                pystray.MenuItem("Configurações", on_config),
                pystray.MenuItem("Sair", on_quit)
            )
        else:
            paused.set()
            icon.menu = pystray.Menu(
                pystray.MenuItem("Pausado", None, enabled=False),
                pystray.MenuItem("Retomar", on_pause_toggle),
                pystray.MenuItem("Mover Agora", on_move_now),
                pystray.MenuItem("Configurações", on_config),
                pystray.MenuItem("Sair", on_quit)
            )

    def on_move_now(icon, item):
        if watcher.handler:
            watcher.handler.move_pending_files()

    def on_config(icon, item):
        watcher.stop()
        
        subprocess.Popen([sys.executable, "-c", f"from view.gui import show_config_window; from lib.config import Config; from lib.ipc_client import send_move_now; from pathlib import Path; config = Config.load(Path(r'{config_path}')); show_config_window(config, Path(r'{config_path}'), move_now_callback=lambda: send_move_now({ipc_port}))"])
        
        new_config = Config.load(config_path)
        watcher.config = new_config
        if watcher.handler:
            watcher.handler.update_config(new_config)
        watcher.start()

    def on_quit(icon, item):
        watcher.stop()
        icon.stop()

    icon = pystray.Icon(
        "download_organizer",
        create_icon(),
        "Download Organizer",
        menu=pystray.Menu(
            pystray.MenuItem("Monitorando", None, enabled=False),
            pystray.MenuItem("Pausar", on_pause_toggle),
            pystray.MenuItem("Mover Agora", on_move_now),
            pystray.MenuItem("Configurações", on_config),
            pystray.MenuItem("Sair", on_quit)
        )
    )

    icon.run()
