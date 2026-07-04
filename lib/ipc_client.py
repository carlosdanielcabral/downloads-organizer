import logging
import socket

from lib.ipc_server import COMMAND_MOVE_NOW, RESPONSE_OK

logger = logging.getLogger(__name__)


def send_move_now(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(5)
            client_socket.connect(("127.0.0.1", port))
            client_socket.sendall(COMMAND_MOVE_NOW.encode("utf-8"))
            response = client_socket.recv(1024).decode("utf-8").strip()

        success = response == RESPONSE_OK
        logger.info(f"IPC move_now response: {response}")

        return success
    except Exception as error:
        logger.error(f"IPC client error: {error}")

        return False
