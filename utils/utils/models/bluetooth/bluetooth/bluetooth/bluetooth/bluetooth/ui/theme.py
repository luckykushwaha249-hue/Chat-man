from utils.config import Config
import flet as ft

def get_base_container(content, expand=False):
    return ft.Container(
        content=content,
        bgcolor=Config.BG_COLOR,
        expand=expand,
        padding=20
    )

def get_title_style():
    return ft.TextStyle(size=28, weight=ft.FontWeight.BOLD, color=Config.TEXT_COLOR)
