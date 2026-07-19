import flet as ft
import asyncio
from utils.config import Config
from bluetooth.discovery import BluetoothDiscovery

class BluetoothSetupScreen(ft.Container):
    def __init__(self, connection_manager, on_connected):
        super().__init__()
        self.cm = connection_manager
        self.on_connected = on_connected
        self.expand = True
        self.bgcolor = Config.BG_COLOR
        self.padding = 20

        self.device_list = ft.ListView(expand=True, spacing=10)
        self.status_text = ft.Text("Turn on Bluetooth to scan devices", color=ft.colors.GREY_400)

        self.content = ft.Column([
            ft.Text("Bluetooth Devices", size=24, weight="bold", color=Config.TEXT_COLOR),
            self.status_text,
            ft.ElevatedButton("Turn On & Scan", icon=ft.icons.BLUETOOTH, on_click=self.scan_devices),
            ft.ElevatedButton("Host Chat (Wait for connection)", icon=ft.icons.CELL_WIFI, on_click=self.host_chat),
            ft.Divider(color=Config.PANEL_COLOR),
            self.device_list
        ])

    def scan_devices(self, e):
        self.status_text.value = "Scanning nearby devices..."
        self.device_list.controls.clear()
        self.update()
        
        loop = asyncio.new_event_loop()
        devices = loop.run_until_complete(BluetoothDiscovery.scan_devices())
        
        if not devices:
            self.status_text.value = "No devices found."
        else:
            self.status_text.value = "Select a device to connect:"
            for d in devices:
                self.device_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(d['name'], color=Config.TEXT_COLOR),
                        subtitle=ft.Text(d['address'], color=ft.colors.GREY_500),
                        leading=ft.Icon(ft.icons.BLUETOOTH_CONNECTED, color=Config.ACCENT_COLOR),
                        on_click=lambda e, addr=d['address'], name=d['name']: self.connect_to(addr, name)
                    )
                )
        self.update()

    def host_chat(self, e):
        self.status_text.value = "Hosting... waiting for connection."
        self.update()
        self.cm.start_host(on_ready=lambda: print("Hosting started"))
        self.cm.on_message = self.dummy_accept
        
    def dummy_accept(self, msg):
        if msg['type'] == 'system' and msg['text'] == 'connected':
            self.on_connected(msg['sender'])

    def connect_to(self, address, name):
        self.status_text.value = f"Connecting to {name}..."
        self.update()
        self.cm.connect_to(
            address,
            on_success=lambda: self.on_connected(name),
            on_fail=lambda: self.show_error()
        )

    def show_error(self):
        self.status_text.value = "Connection failed."
        self.update()
