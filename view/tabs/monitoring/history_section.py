import customtkinter as ctk

from lib.history.move_history import MoveHistory

MOVED_AT_FORMAT = "%d/%m/%Y %H:%M"
ROW_HEIGHT = 30
EMPTY_STATE_HEIGHT = 36
MAX_HEIGHT = 200


class HistorySection(ctk.CTkFrame):
    """
    Displays the list of successfully moved files in a scrollable frame.

    The frame height grows with the number of entries up to MAX_HEIGHT,
    after which it becomes scrollable. Reacts to new history entries via
    the Observer pattern: registers itself on MoveHistory and schedules
    thread-safe UI refreshes via tkinter's after(0, ...).
    """

    def __init__(self, master, move_history: MoveHistory, **kwargs):
        super().__init__(master, **kwargs)

        self._move_history = move_history

        self._setup_ui()
        self._register_observer()

    def unregister_observer(self) -> None:
        self._move_history.clear_on_change()

    def _register_observer(self) -> None:
        self._move_history.set_on_change(self._on_history_change)

    def _on_history_change(self) -> None:
        self.after(0, self._refresh)

    def _setup_ui(self) -> None:
        self._rows_frame = ctk.CTkFrame(self, height=EMPTY_STATE_HEIGHT)
        self._rows_frame.pack(fill="x", padx=10, pady=(10, 10))
        self._rows_frame.pack_propagate(False)

        self._refresh()

    def _refresh(self) -> None:
        for widget in self._rows_frame.winfo_children():
            widget.destroy()

        entries = self._move_history.get_all()

        if not entries:
            self._rows_frame.configure(height=EMPTY_STATE_HEIGHT)
            self._render_empty_state()

            return

        desired_height = min(len(entries) * ROW_HEIGHT, MAX_HEIGHT)
        self._rows_frame.configure(height=desired_height)

        for entry in entries:
            self._render_history_row(entry)

    def _render_empty_state(self) -> None:
        empty_label = ctk.CTkLabel(
            self._rows_frame,
            text="Nenhum arquivo movido ainda.",
            font=("Arial", 11),
            text_color="gray",
        )
        empty_label.pack(anchor="w", padx=5, pady=5)

    def _render_history_row(self, entry) -> None:
        moved_at = entry.moved_at.strftime(MOVED_AT_FORMAT)
        text = f"{entry.source_name}  →  {entry.destination}  —  {moved_at}"

        row_label = ctk.CTkLabel(
            self._rows_frame,
            text=text,
            font=("Arial", 11),
            anchor="w",
        )
        row_label.pack(fill="x", padx=5, pady=2)
