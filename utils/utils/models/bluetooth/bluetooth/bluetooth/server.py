import socket
import threading
from utils.config import Config
from utils.logger import get_logger

logger = get_logger("BT_Server")

class BluetoothServer:
    def __init__(self, port=Config.RFCOMM_CHANNEL):
        self.port = port
        self.server_sock = None
        self.client_sock = None
        self.running = False

    def get_socket_family(self):
        if hasattr(socket, 'AF_BTH'):
            return socket.AF_BTH  # Windows
        elif hasattr(socket, 'AF_BLUETOOTH'):
            return socket.AF_BLUETOOTH  # Linux
        return socket.AF_INET # Fallback

    def start(self, on_connected):
        self.running = True
        threading.Thread(target=self._listen_thread, args=(on_connected,), daemon=True).start()

    def _listen_thread(self, on_connected):
        try:
            family = self.get_socket_family()
            protocol = socket.BTPROTO_RFCOMM if family != socket.AF_INET else 0
            self.server_sock = socket.socket(family, socket.SOCK_STREAM, protocol)
            if family == socket.AF_INET:
                self.server_sock.bind(('0.0.0.0', 8080)) 
            else:
                self.server_sock.bind((socket.BDADDR_ANY if hasattr(socket, 'BDADDR_ANY') else "", self.port))
            
            self.server_sock.listen(1)
            logger.info("Listening for incoming Bluetooth connections...")
            self.client_sock, client_info = self.server_sock.accept()
            logger.info(f"Accepted connection from {client_info}")
            on_connected(self.client_sock, client_info[0])
        except Exception as e:
            logger.error(f"Server error: {e}")

    def stop(self):
        self.running = False
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()
