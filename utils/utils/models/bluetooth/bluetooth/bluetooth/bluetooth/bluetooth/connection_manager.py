import threading
import time
from queue import Queue
from .server import BluetoothServer
from .client import BluetoothClient
from .protocol import Protocol
from models.message import ChatMessage
from utils.config import Config
from utils.logger import get_logger

logger = get_logger("ConnManager")

class ConnectionManager:
    def __init__(self, on_message, on_disconnect):
        self.server = BluetoothServer()
        self.client = BluetoothClient()
        self.sock = None
        self.on_message = on_message
        self.on_disconnect = on_disconnect
        self.send_queue = Queue()
        self.running = False
        self.last_heartbeat = time.time()
        self.buffer = bytearray()

    def start_host(self, on_ready):
        self.server.start(self._setup_connection)
        on_ready()

    def connect_to(self, address, on_success, on_fail):
        sock = self.client.connect(address)
        if sock:
            self._setup_connection(sock, address)
            on_success()
        else:
            on_fail()

    def _setup_connection(self, sock, address):
        self.sock = sock
        self.running = True
        self.last_heartbeat = time.time()
        
        threading.Thread(target=self._receive_loop, daemon=True).start()
        threading.Thread(target=self._send_loop, daemon=True).start()
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()

    def send_message(self, msg: ChatMessage):
        self.send_queue.put(msg)

    def _receive_loop(self):
        while self.running and self.sock:
            try:
                data = self.sock.recv(Config.BUFFER_SIZE)
                if not data:
                    break
                self.buffer.extend(data)
                messages, self.buffer = Protocol.decode(self.buffer)
                
                for msg in messages:
                    if msg['type'] == 'heartbeat':
                        self.last_heartbeat = time.time()
                    else:
                        self.on_message(msg)
            except Exception as e:
                logger.error(f"Receive error: {e}")
                break
        self._trigger_disconnect()

    def _send_loop(self):
        while self.running and self.sock:
            try:
                msg = self.send_queue.get(timeout=1)
                data = Protocol.encode(msg)
                self.sock.sendall(data)
            except Exception:
                continue

    def _heartbeat_loop(self):
        while self.running:
            time.sleep(Config.HEARTBEAT_INTERVAL)
            self.send_message(ChatMessage(type="heartbeat", sender="system", text="ping"))
            if time.time() - self.last_heartbeat > Config.TIMEOUT_LIMIT:
                logger.warning("Heartbeat timeout! Connection lost.")
                self.running = False
                self._trigger_disconnect()
                break

    def _trigger_disconnect(self):
        self.running = False
        if self.sock:
            self.sock.close()
            self.sock = None
        self.on_disconnect()
