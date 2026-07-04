import logging
import asyncio
import threading
from pathlib import Path

logger = logging.getLogger(__name__)


def show_file_moved_notification(file_name: str, destination: Path):
    try:
        from desktop_notifier import DesktopNotifier, Urgency
        
        logger.info(f"Showing notification for: {file_name}")
        
        icon_path = Path(__file__).parent.parent / "view" / "assets" / "icon.png"
        
        async def send_notification():
            notifier = DesktopNotifier("DownloadOrganizer")
            await notifier.send(
                title="Download Organizer",
                message=f"{file_name} → {destination.parent.name}",
                urgency=Urgency.Normal,
                icon=icon_path
            )
        
        def run_in_thread():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(send_notification())
            loop.close()
        
        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()
        
        logger.info("Notification sent successfully")
    except ImportError as e:
        logger.error(f"desktop-notifier not installed: {e}")
    except Exception as e:
        logger.error(f"Error showing notification: {e}")
