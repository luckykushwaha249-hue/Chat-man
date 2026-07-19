import flet as ft
from datetime import datetime
from utils.config import Config
from models.message import ChatMessage

class ChatScreen(ft.Container):
    def __init__(self, peer_name, connection_manager, on_back):
        super().__init__()
        self.peer_name = peer_name
        self.cm = connection_manager
        self.on_back = on_back
        self.expand = True
        self.bgcolor = Config.BG_COLOR
        self.padding = 10

        self.chat_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.msg_input = ft.TextField(
            hint_text="Type a message...",
            expand=True,
            border_radius=20,
            bgcolor=Config.PANEL_COLOR,
            border_color="transparent",
            on_change=self.send_typing_indicator,
            on_submit=self.send_message
        )
        
        self.typing_indicator = ft.Text(
            "", 
            color=Config.ACCENT_COLOR, 
            size=12, 
            italic=True,
            font_family="Consolas"
        )

        self.content = ft.Column([
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda e: self.on_back()),
                ft.Text(f"Connect with user {self.peer_name}", size=18, weight="bold")
            ], alignment=ft.MainAxisAlignment.START),
            ft.Divider(color=Config.PANEL_COLOR),
            self.chat_list,
            self.typing_indicator,
            ft.Row([
                self.msg_input,
                ft.IconButton(
                    icon=ft.icons.SEND,
                    icon_color=Config.ACCENT_COLOR,
                    on_click=self.send_message
                )
            ])
        ])

    def send_typing_indicator(self, e):
        if len(self.msg_input.value) % 3 == 1:
            msg = ChatMessage(type="typing", sender="self", text="typing")
            self.cm.send_message(msg)

    def send_message(self, e):
        text = self.msg_input.value.strip()
        if not text:
            return
            
        self.add_bubble(text, is_sender=True)
        
        msg = ChatMessage(type="message", sender="self", text=text)
        self.cm.send_message(msg)
        
        self.msg_input.value = ""
        self.update()

    def handle_incoming(self, msg: dict):
        if msg['type'] == 'typing':
            self.typing_indicator.value = f"{self.peer_name} is typing..."
            self.update()
            import threading
            threading.Timer(2.0, self.clear_typing).start()
        elif msg['type'] == 'message':
            self.clear_typing()
            self.add_bubble(msg['text'], is_sender=False)

    def clear_typing(self):
        self.typing_indicator.value = ""
        self.update()

    def add_bubble(self, text, is_sender):
        time_str = datetime.now().strftime("%I:%M %p")
        
        bubble = ft.Container(
            content=ft.Column([
                ft.Text(text, color=Config.TEXT_COLOR, size=15),
                ft.Text(time_str, color=ft.colors.GREY_400, size=10, text_align=ft.TextAlign.RIGHT)
            ], spacing=2),
            bgcolor=Config.SENDER_BUBBLE if is_sender else Config.RECEIVER_BUBBLE,
            border_radius=ft.border_radius.all(15),
            padding=10,
            max_width=300
        )

        row = ft.Row(
            [bubble],
            alignment=ft.MainAxisAlignment.START if is_sender else ft.MainAxisAlignment.END
        )
        self.chat_list.controls.append(row)
        self.update()

    def show_disconnect_popup(self, peer_name):
        def close_dlg(e):
            self.page.dialog.open = False
            self.page.update()
            self.on_back()

        dlg = ft.AlertDialog(
            title=ft.Text(f"chat end by user {peer_name}"),
            on_dismiss=lambda e: self.on_back(),
            actions=[ft.TextButton("OK", on_click=close_dlg)]
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
