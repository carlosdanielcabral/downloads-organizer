import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
ENTRY_POINT = str(PROJECT_ROOT / "main.py")
APP_NAME = "DownloadOrganizer"
ICON_DATA_SRC = "view/assets/icon.png"
ICON_DATA_DEST = "view/assets"

SEPARATOR = ";" if sys.platform == "win32" else ":"

PYINSTALLER_ARGS = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    f"--name={APP_NAME}",
    "--collect-data=customtkinter",
    "--collect-data=desktop_notifier",
    f"--add-data=default_config.json{SEPARATOR}.",
    f"--add-data={ICON_DATA_SRC}{SEPARATOR}{ICON_DATA_DEST}",
    ENTRY_POINT,
]


def main() -> None:
    print(f"Building {APP_NAME}...")
    print(f"Command: {' '.join(PYINSTALLER_ARGS)}\n")

    result = subprocess.run(PYINSTALLER_ARGS, cwd=PROJECT_ROOT)

    if result.returncode == 0:
        exe_path = PROJECT_ROOT / "dist" / f"{APP_NAME}.exe"
        print(f"\nBuild successful: {exe_path}")
    else:
        print(f"\nBuild failed with exit code {result.returncode}")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
