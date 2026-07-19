import socket
from utils.config import Config
from utils.logger import get_logger

logger = get_logger("BT_Client")

class BluetoothClient:
    def __init__(self):
        self.sock = None

    def get_socket_family(self):
        if hasattr(socket, 'AF_BTH'):
            return socket.AF_BTH
        elif hasattr(socket, 'AF_BLUETOOTH'):
            return socket.AF_BLUETOOTH
        return socket.AF_INET

    def connect(self, address, port=Config.RFCOMM_CHANNEL):
        try:
            family = self.get_socket_family()
            protocol = socket.BTPROTO_RFCOMM if family != socket.AF_INET else 0
            self.sock = socket.socket(family, socket.SOCK_STREAM, protocol)
            
            if family == socket.AF_INET:
                self.sock.connect(('127.0.0.1', 8080)) 
            else:
                self.sock.connect((address, port))
                
            logger.info(f"Connected to {address}")
            return self.sock
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return None

    def disconnect(self):
        if self.sock:
            self.sock.close()
