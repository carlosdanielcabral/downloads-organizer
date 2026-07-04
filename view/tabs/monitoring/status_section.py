import customtkinter as ctk
from pathlib import Path

from lib.processing.file_processor import FileProcessor
from lib.queue.pending_file import PendingFile

SCHEDULED_TIME_FORMAT = "%H:%M:%S"
FILE_NOT_FOUND_MESSAGE = "Arquivo não encontrado — removido da fila."
FEEDBACK_DISPLAY_MS = 4000


class StatusSection(ctk.CTkFrame):
    """
    Displays the list of files pending movement and provides per-file
    and bulk action controls.

    Reacts to queue changes via the Observer pattern: registers itself
    on the DelayQueue and schedules thread-safe UI refreshes via
    tkinter's after(0, ...).
    """

    def __init__(self, master, processor: FileProcessor, **kwargs):
        super().__init__(master, **kwargs)

        self._processor = processor
        self._feedback_label: ctk.CTkLabel | None = None

        self._setup_ui()
        self._register_observer()

    def unregister_observer(self) -> None:
        self._processor.get_delay_queue().clear_on_change()

    def _register_observer(self) -> None:
        self._processor.get_delay_queue().set_on_change(self._on_queue_change)

    def _on_queue_change(self) -> None:
        self.after(0, self._refresh)

    def _setup_ui(self) -> None:
        self._pending_list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._pending_list_frame.pack(fill="x", padx=10, pady=(10, 5))

        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=10, pady=(5, 10))

        self._move_all_button = ctk.CTkButton(
            buttons_frame,
            text="Mover todos",
            command=self._on_move_all,
            height=32,
        )
        self._move_all_button.pack(side="left", padx=(0, 5))

        self._cancel_all_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar todos",
            fg_color="gray",
            hover_color="#555555",
            command=self._on_cancel_all,
            height=32,
        )
        self._cancel_all_button.pack(side="left")

        self._refresh()

    def _refresh(self) -> None:
        for widget in self._pending_list_frame.winfo_children():
            widget.destroy()

        pending_files = self._processor.get_delay_queue().get_pending()

        if not pending_files:
            self._render_empty_state()
        else:
            for pending_file in pending_files:
                self._render_pending_file_row(pending_file)

        has_pending = bool(pending_files)
        self._move_all_button.configure(state="normal" if has_pending else "disabled")
        self._cancel_all_button.configure(state="normal" if has_pending else "disabled")

    def _render_empty_state(self) -> None:
        empty_label = ctk.CTkLabel(
            self._pending_list_frame,
            text="Nenhum arquivo aguardando movimentação.",
            font=("Arial", 11),
            text_color="gray",
        )
        empty_label.pack(anchor="w", padx=5, pady=5)

    def _render_pending_file_row(self, pending_file: PendingFile) -> None:
        row = ctk.CTkFrame(self._pending_list_frame)
        row.pack(fill="x", pady=2)

        scheduled_time = pending_file.scheduled_for.strftime(SCHEDULED_TIME_FORMAT)

        file_label = ctk.CTkLabel(
            row,
            text=f"{pending_file.path.name}  —  movimentação prevista às {scheduled_time}",
            font=("Arial", 11),
            anchor="w",
        )
        file_label.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)

        move_button = ctk.CTkButton(
            row,
            text="Mover",
            width=70,
            height=28,
            command=lambda path=pending_file.path: self._on_move_file(path),
        )
        move_button.pack(side="right", padx=(5, 5), pady=5)

        cancel_button = ctk.CTkButton(
            row,
            text="Cancelar",
            width=70,
            height=28,
            fg_color="gray",
            hover_color="#555555",
            command=lambda path=pending_file.path: self._on_cancel_file(path),
        )
        cancel_button.pack(side="right", padx=(5, 0), pady=5)

    def _show_feedback(self, message: str) -> None:
        if self._feedback_label:
            self._feedback_label.destroy()

        self._feedback_label = ctk.CTkLabel(
            self,
            text=message,
            font=("Arial", 10),
            text_color="orange",
        )
        self._feedback_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.after(FEEDBACK_DISPLAY_MS, self._clear_feedback)

    def _clear_feedback(self) -> None:
        if self._feedback_label:
            self._feedback_label.destroy()
            self._feedback_label = None

    def _on_move_all(self) -> None:
        self._processor.move_pending()

    def _on_cancel_all(self) -> None:
        for pending_file in self._processor.get_delay_queue().get_pending():
            self._processor.cancel(pending_file.path)

    def _on_move_file(self, path: Path) -> None:
        if not path.exists():
            self._processor.cancel(path)
            self._show_feedback(FILE_NOT_FOUND_MESSAGE)

            return

        self._processor.execute_now(path)

    def _on_cancel_file(self, path: Path) -> None:
        self._processor.cancel(path)
