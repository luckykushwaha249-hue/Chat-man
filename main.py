import flet as ft
from app import ChatManApp

def main(page: ft.Page):
    page.title = "chat-man"
    page.window_width = 450
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    
    app = ChatManApp(page)
    page.add(app)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
