import flet as ft
from App.storage import app_state
import App.router as rout
import os

def get_page_content(page):
    return ft.Column(
        controls=[
            ft.Text(f"Это Страница {page}", size=30, weight="bold"),
            ft.Text("Здесь может быть любой контент...", size=16),
            ft.ElevatedButton(
                "Назад",
                on_click=lambda e: rout.Page_Home.link(),  # Возврат на главную
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )