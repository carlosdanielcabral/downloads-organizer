import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def show_file_moved_notification(file_name: str, destination: Path):
    try:
        from plyer import notification
        
        logger.info(f"Showing notification for: {file_name}")
        
        notification.notify(
            title="Download Organizer",
            message=f"{file_name} → {destination.parent.name}",
            app_name="Download Organizer",
            timeout=5
        )
        
        logger.info("Notification sent successfully")
    except ImportError as e:
        logger.error(f"plyer not installed: {e}")
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
