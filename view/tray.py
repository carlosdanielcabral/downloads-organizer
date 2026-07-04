import threading
from pathlib import Path
from PIL import Image, ImageDraw

import pystray

from lib.watcher import DownloadWatcher
from lib.config import Config


def create_icon() -> Image.Image:
    image = Image.new("RGB", (64, 64), color=(0, 120, 215))
    draw = ImageDraw.Draw(image)

    draw.rectangle([16, 16, 48, 48], fill=(255, 255, 255))
    draw.rectangle([20, 20, 44, 44], fill=(0, 120, 215))

    return image


def run_tray(watcher: DownloadWatcher, paused: threading.Event, config: Config, config_path: Path) -> None:
    def on_pause_toggle(icon, item):
        if paused.is_set():
            paused.clear()
            item.text = "Pausar"
            status_item.text = "Monitorando"
        else:
            paused.set()
            item.text = "Retomar"
            status_item.text = "Pausado"

    def on_config(icon, item):
        from view.gui import show_config_window
        
        watcher.stop()
        show_config_window(config, config_path, on_save_callback=lambda: watcher.start())

    def on_quit(icon, item):
        watcher.stop()
        icon.stop()

    status_item = pystray.MenuItem("Monitorando", None, enabled=False)
    pause_item = pystray.MenuItem("Pausar", on_pause_toggle)
    config_item = pystray.MenuItem("Configurações", on_config)
    quit_item = pystray.MenuItem("Sair", on_quit)

    icon = pystray.Icon(
        "download_organizer",
        create_icon(),
        menu=pystray.Menu(status_item, pause_item, config_item, quit_item)
    )

    icon.run()
