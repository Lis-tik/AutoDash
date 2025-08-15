import flet as ft
from App.storage import app_state
import App.router as rout
import os



# Главная страница (навигация)
def get_home_page():
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("Шапка сайта", size=30, weight='bold'),
                padding=10,
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton("Главная", on_click=lambda e: rout.Page_Multi.link(1)),
                    ft.ElevatedButton("Конвертер", on_click=lambda e: rout.Page_Multi.link(2)),
                    ft.ElevatedButton("Манифест", on_click=lambda e: rout.Page_Multi.link(3)),
                    ft.ElevatedButton("Запуск", on_click=lambda e: rout.Page_Multi.link(4)),
                ],
                spacing=10,
            ),
            ft.Column(
                controls=[ft.FloatingActionButton(f) for f in app_state.files],
                spacing=10,
            )
        ],
        expand=True,
        spacing=10,     
    )