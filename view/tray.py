import threading
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

import pystray

from lib.watcher import DownloadWatcher
from lib.config import Config


def create_icon() -> Image.Image:
    image = Image.new("RGBA", (64, 64), color=(0, 120, 215, 255))
    draw = ImageDraw.Draw(image)

    draw.rectangle([16, 16, 48, 48], fill=(255, 255, 255, 255))
    draw.rectangle([20, 20, 44, 44], fill=(0, 120, 215, 255))

    return image


def run_tray(watcher: DownloadWatcher, paused: threading.Event, config: Config, config_path: Path) -> None:
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
        watcher.handler.move_pending_files()

    def on_config(icon, item):
        watcher.stop()
        
        subprocess.Popen([sys.executable, "-c", f"from view.gui import show_config_window; from lib.config import Config; from pathlib import Path; config = Config.load(Path(r'{config_path}')); show_config_window(config, Path(r'{config_path}'), move_now_callback=lambda: watcher.handler.move_pending_files())"])
        
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
