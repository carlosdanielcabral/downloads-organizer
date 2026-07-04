from pathlib import Path

from PIL import Image


def create_icon() -> Image.Image:
    icon_path = Path(__file__).parent / "assets" / "icon.png"

    if icon_path.exists():
        return Image.open(icon_path)

    return Image.new("RGBA", (64, 64), color=(0, 120, 215, 255))
