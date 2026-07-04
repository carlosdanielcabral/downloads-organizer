import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def show_file_moved_notification(file_name: str, destination: Path):
    try:
        from win10toast import ToastNotifier
        
        logger.info(f"Showing notification for: {file_name}")
        
        toaster = ToastNotifier()
        
        toaster.show_toast(
            "Download Organizer",
            f"{file_name} → {destination.parent.name}",
            duration=5,
            threaded=True
        )
        
        logger.info("Notification sent successfully")
    except ImportError as e:
        logger.error(f"win10toast not installed: {e}")
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
