import flet as ft
from ui.lock_screen import LockScreen
from ui.bluetooth_setup import BluetoothSetupScreen
from ui.chat_view import ChatScreen
from bluetooth.connection_manager import ConnectionManager
from utils.config import Config

class ChatManApp(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.expand = True
        self.connection_manager = ConnectionManager(self.on_message_received, self.on_disconnect)
        self.current_peer = None
        self.show_lock_screen()

    def show_lock_screen(self):
        self.content = LockScreen(on_unlock=self.show_bluetooth_setup)
        self.update()

    def show_bluetooth_setup(self):
        self.content = BluetoothSetupScreen(
            connection_manager=self.connection_manager,
            on_connected=self.show_chat_screen
        )
        self.update()

    def show_chat_screen(self, peer_name: str):
        self.current_peer = peer_name
        self.chat_screen = ChatScreen(
            peer_name=peer_name,
            connection_manager=self.connection_manager,
            on_back=self.show_bluetooth_setup
        )
        self.content = self.chat_screen
        self.update()

    def on_message_received(self, message: dict):
        if hasattr(self, 'chat_screen') and self.content == self.chat_screen:
            self.chat_screen.handle_incoming(message)

    def on_disconnect(self):
        if hasattr(self, 'chat_screen') and self.content == self.chat_screen:
            self.chat_screen.show_disconnect_popup(self.current_peer)
