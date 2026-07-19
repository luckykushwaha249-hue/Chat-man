import flet as ft
from utils.config import Config
from .theme import get_base_container, get_title_style

class LockScreen(ft.Container):
    def __init__(self, on_unlock):
        super().__init__()
        self.on_unlock = on_unlock
        self.expand = True
        self.bgcolor = Config.BG_COLOR

        self.password_field = ft.TextField(
            hint_text="Enter Password",
            password=True,
            can_reveal_password=True,
            border_radius=30,
            text_align=ft.TextAlign.CENTER,
            width=300,
            bgcolor=Config.PANEL_COLOR,
            border_color="transparent"
        )
        
        self.error_text = ft.Text("", color=ft.colors.RED, size=12)

        self.content = ft.Column(
            controls=[
                ft.Icon(name=ft.icons.LOCK, size=80, color=Config.ACCENT_COLOR),
                ft.Text(Config.APP_NAME, style=get_title_style()),
                ft.Text("Enter password to continue", color=ft.colors.GREY_400),
                ft.Container(height=30),
                self.password_field,
                self.error_text,
                ft.ElevatedButton(
                    text="OK",
                    width=300,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=30),
                        bgcolor=Config.PANEL_COLOR,
                        color=Config.ACCENT_COLOR
                    ),
                    on_click=self.verify_password
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

    def verify_password(self, e):
        if self.password_field.value == Config.APP_PASSWORD:
            self.on_unlock()
        else:
            self.error_text.value = "Incorrect password!"
            self.password_field.value = ""
            self.update()
