import subprocess
from pathlib import Path


def show_file_moved_notification(file_name: str, destination: Path):
    try:
        from win10toast import ToastNotifier
        
        toaster = ToastNotifier()
        
        def on_click():
            subprocess.run(["explorer", str(destination.parent)], shell=True)
        
        toaster.show_toast(
            "Download Organizer",
            f"{file_name} → {destination.parent.name}",
            duration=5,
            threaded=True,
            icon_path=None,
            callback_on_click=on_click
        )
    except ImportError:
        pass
    except Exception:
        pass
