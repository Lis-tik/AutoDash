import flet as ft
from App.storage import app_state
import App.router as rout
import os

def setting_converter():
    return ft.Column(
        controls=[
            ft.Text(f"Это Страница для настройки конвертера", size=30, weight="bold"),
            ft.Text("Здесь может быть любой контент...", size=16),
            ft.ElevatedButton(
                "Назад",
                on_click=lambda e: app_state.new_page(rout.Page_Home),  # Возврат на главную
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )