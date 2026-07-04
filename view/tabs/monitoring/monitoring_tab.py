import customtkinter as ctk
from pathlib import Path

from lib.config.config import Config
from lib.processing.file_processor import FileProcessor
from lib.processing.paths import get_downloads_folder
from lib.queue.pending_file import PendingFile
from view.widgets.file_picker import FilePicker

SCHEDULED_TIME_FORMAT = "%H:%M:%S"
FILE_NOT_FOUND_MESSAGE = "Arquivo não encontrado — removido da fila."


class MonitoringTab(ctk.CTkFrame):
    """
    Tab that displays the pending file queue (Status section) and the
    monitoring configuration inputs (Configurações section).

    Reacts to queue changes via the Observer pattern: the DelayQueue calls
    on_queue_change() from its own thread, which schedules a thread-safe
    UI refresh via tkinter's after(0, ...).
    """

    def __init__(self, master, config: Config, processor: FileProcessor, **kwargs):
        super().__init__(master, **kwargs)

        self._config = config
        self._processor = processor
        self._feedback_label: ctk.CTkLabel | None = None

        self._setup_ui()
        self._load_settings()
        self._register_observer()

    def on_queue_change(self) -> None:
        self.after(0, self._refresh_status)

    def unregister_observer(self) -> None:
        self._processor.get_delay_queue().clear_on_change()

    def _register_observer(self) -> None:
        self._processor.get_delay_queue().set_on_change(self.on_queue_change)

    def _setup_ui(self) -> None:
        self._setup_status_section()
        self._setup_settings_section()

    def _setup_status_section(self) -> None:
        section_label = ctk.CTkLabel(self, text="Status", font=("Arial", 14, "bold"))
        section_label.pack(anchor="w", padx=20, pady=(15, 0))

        self._status_frame = ctk.CTkFrame(self)
        self._status_frame.pack(fill="x", padx=20, pady=(5, 10))

        self._pending_list_frame = ctk.CTkFrame(self._status_frame, fg_color="transparent")
        self._pending_list_frame.pack(fill="x", padx=10, pady=(10, 5))

        self._move_all_button = ctk.CTkButton(
            self._status_frame,
            text="Mover Todos Agora",
            command=self._on_move_all,
            height=32,
        )
        self._move_all_button.pack(anchor="w", padx=10, pady=(5, 10))

        self._refresh_status()

    def _setup_settings_section(self) -> None:
        section_label = ctk.CTkLabel(self, text="Configurações", font=("Arial", 14, "bold"))
        section_label.pack(anchor="w", padx=20, pady=(10, 0))

        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(fill="x", padx=20, pady=(5, 10))

        self._setup_watch_folder_input(settings_frame)
        self._setup_notifications_input(settings_frame)
        self._setup_delay_input(settings_frame)

    def _setup_watch_folder_input(self, parent: ctk.CTkFrame) -> None:
        path_label = ctk.CTkLabel(parent, text="Pasta Monitorada:", font=("Arial", 12))
        path_label.pack(anchor="w", padx=5, pady=(10, 0))

        current_path = self._config.get_watch_folder() or str(get_downloads_folder())

        self._file_picker = FilePicker(parent, initial_path=current_path, on_change=self._on_watch_folder_change)
        self._file_picker.pack(fill="x", padx=5, pady=5)

        info_label = ctk.CTkLabel(parent, text="Selecione a pasta que deseja monitorar para novos downloads.", font=("Arial", 10))
        info_label.pack(anchor="w", padx=5, pady=(0, 5))

    def _setup_notifications_input(self, parent: ctk.CTkFrame) -> None:
        notifications_frame = ctk.CTkFrame(parent)
        notifications_frame.pack(fill="x", padx=5, pady=10)

        self._notifications_checkbox = ctk.CTkCheckBox(
            notifications_frame,
            text="Habilitar notificações ao organizar arquivos",
            command=self._on_notifications_toggle,
        )
        self._notifications_checkbox.pack(anchor="w", padx=5, pady=5)

    def _setup_delay_input(self, parent: ctk.CTkFrame) -> None:
        delay_frame = ctk.CTkFrame(parent)
        delay_frame.pack(fill="x", padx=5, pady=10)

        delay_label = ctk.CTkLabel(delay_frame, text="Delay antes de mover (minutos):", font=("Arial", 12))
        delay_label.pack(anchor="w", padx=5, pady=5)

        self._delay_entry = ctk.CTkEntry(delay_frame, width=100)
        self._delay_entry.pack(anchor="w", padx=5, pady=5)
        self._delay_entry.bind("<KeyRelease>", lambda event: self._on_delay_change(event.widget.get()))

    def _load_settings(self) -> None:
        current_path = self._config.get_watch_folder()

        if current_path:
            self._file_picker.set_path(current_path)

        self._notifications_checkbox.set(self._config.get_enable_notifications())
        self._delay_entry.delete(0, "end")
        self._delay_entry.insert(0, str(self._config.get_delay_minutes()))

    def _refresh_status(self) -> None:
        for widget in self._pending_list_frame.winfo_children():
            widget.destroy()

        pending_files = self._processor.get_delay_queue().get_pending()

        if not pending_files:
            self._render_empty_status()
        else:
            for pending_file in pending_files:
                self._render_pending_file_row(pending_file)

        self._move_all_button.configure(state="normal" if pending_files else "disabled")

    def _render_empty_status(self) -> None:
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
            self._status_frame,
            text=message,
            font=("Arial", 10),
            text_color="orange",
        )
        self._feedback_label.pack(anchor="w", padx=10, pady=(0, 5))

        self.after(4000, self._clear_feedback)

    def _clear_feedback(self) -> None:
        if self._feedback_label:
            self._feedback_label.destroy()
            self._feedback_label = None

    def _on_move_all(self) -> None:
        self._processor.move_pending()

    def _on_move_file(self, path: Path) -> None:
        if not path.exists():
            self._processor.cancel(path)
            self._show_feedback(FILE_NOT_FOUND_MESSAGE)
            return

        self._processor.execute_now(path)

    def _on_cancel_file(self, path: Path) -> None:
        self._processor.cancel(path)

    def _on_watch_folder_change(self, path: str) -> None:
        self._config.set_watch_folder(path)

    def _on_notifications_toggle(self) -> None:
        self._config.set_enable_notifications(self._notifications_checkbox.get())

    def _on_delay_change(self, value: str) -> None:
        try:
            minutes = int(float(value))
            self._config.set_delay_minutes(minutes)
        except ValueError:
            pass
