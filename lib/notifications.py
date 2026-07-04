import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def show_file_moved_notification(file_name: str, destination: Path):
    try:
        import win32gui
        import win32con
        import win32api
        
        logger.info(f"Showing notification for: {file_name}")
        
        title = "Download Organizer"
        message = f"{file_name} → {destination.parent.name}"
        
        win32gui.MessageBox(
            0,
            message,
            title,
            win32con.MB_OK | win32con.MB_ICONINFORMATION
        )
        
        logger.info("Notification sent successfully")
    except ImportError as e:
        logger.error(f"pywin32 not installed: {e}")
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
