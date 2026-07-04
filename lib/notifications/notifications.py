import asyncio
import logging
import os
import threading
from pathlib import Path

logger = logging.getLogger(__name__)

ICON_PATH = Path(__file__).parent.parent / "view" / "assets" / "icon.png"


class NotificationService:
    """
    Manages desktop notifications for the application.

    Runs a persistent asyncio event loop in a background thread, ensuring
    that WinRT callbacks (e.g. notification dismissed or button clicked)
    always have an active loop to be dispatched to.

    Must be started before use and stopped when the application exits.
    """

    def __init__(self):
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._notifier = None

    def start(self) -> None:
        self._thread.start()
        asyncio.run_coroutine_threadsafe(self._initialize_notifier(), self._loop).result()

    def stop(self) -> None:
        self._loop.call_soon_threadsafe(self._loop.stop)

    def notify_file_moved(self, file_name: str, destination: Path) -> None:
        asyncio.run_coroutine_threadsafe(
            self._send(file_name, destination),
            self._loop
        )

    async def _initialize_notifier(self) -> None:
        from desktop_notifier import DesktopNotifier

        self._notifier = DesktopNotifier("DownloadOrganizer")

    async def _send(self, file_name: str, destination: Path) -> None:
        try:
            from desktop_notifier import Button, Urgency

            logger.info(f"Showing notification for: {file_name}")

            await self._notifier.send(
                title="Download Organizer",
                message=f"{file_name} → {destination.parent.name}",
                buttons=[Button(title="Abrir", on_pressed=lambda: os.startfile(destination))],
                urgency=Urgency.Normal,
                icon=ICON_PATH
            )

            logger.info("Notification sent successfully")
        except Exception as error:
            logger.error(f"Error showing notification: {error}")
