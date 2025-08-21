import flet as ft
from tkinter import Tk, filedialog
from App.storage import app_state
import App.router as rout
import os




def open_directory_dialog():
    # Создаем скрытое окно Tkinter
    root = Tk()
    root.withdraw()  # Скрываем основное окно
    root.attributes('-topmost', True)  # Поверх других окон
    
    # Открываем диалог выбора директории
    directory = filedialog.askdirectory(title="Выберите папку")

    if directory:  # Если папка выбрана
        app_state.global_path = directory
        app_state.files = [f for f in os.listdir(directory) if f.endswith('.mkv')]
        app_state.new_page(rout.Page_Home)
        




def create_project():
    return ft.Column(
        controls=[
            ft.Text(f"Добро пожаловать в ABR Maker", size=30, weight="bold"),
            ft.Text("Выберите директорию для нового проекта", size=16),
            ft.ElevatedButton(
                "Создать +",
                on_click=lambda e: open_directory_dialog(), 
            ),
        ],
        alignment="center",
        horizontal_alignment="center",
    )
