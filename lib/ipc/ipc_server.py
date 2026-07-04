import logging
import socket
import threading

logger = logging.getLogger(__name__)

COMMAND_MOVE_NOW = "MOVE_NOW"
COMMAND_RELOAD_CONFIG = "RELOAD_CONFIG"
RESPONSE_OK = "OK"
RESPONSE_ERROR = "ERROR"


class IpcServer:
    def __init__(self):
        self._server_socket: socket.socket | None = None
        self._thread: threading.Thread | None = None
        self._port: int | None = None
        self._handlers: dict[str, callable] = {}

    def register_handler(self, command: str, handler: callable) -> None:
        self._handlers[command] = handler

    def get_port(self) -> int | None:
        return self._port

    def start(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("127.0.0.1", 0))
        self._port = self._server_socket.getsockname()[1]
        self._server_socket.listen(5)

        self._thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._thread.start()

        logger.info(f"IPC server listening on port {self._port}")

    def stop(self) -> None:
        if self._server_socket:
            self._server_socket.close()
            self._server_socket = None

        logger.info("IPC server stopped")

    def _accept_loop(self) -> None:
        while self._server_socket:
            try:
                client_socket, address = self._server_socket.accept()
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,),
                    daemon=True
                )
                client_thread.start()
            except OSError:
                break

    def _handle_client(self, client_socket: socket.socket) -> None:
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            logger.info(f"IPC received command: {data}")

            handler = self._handlers.get(data)

            if handler:
                handler()
                client_socket.sendall(RESPONSE_OK.encode("utf-8"))
            else:
                logger.warning(f"IPC unknown command: {data}")
                client_socket.sendall(RESPONSE_ERROR.encode("utf-8"))
        except Exception as error:
            logger.error(f"IPC error handling client: {error}")
        finally:
            client_socket.close()
