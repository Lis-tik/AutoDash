import flet as ft
from tkinter import Tk, filedialog
import os

class AppState:
    def __init__(self):
        self.selected_directory = None
        self.files = []
        self.project_name = "Мой проект"
        # self.TegAccess = ['.mkv', '.mka', '.mp4', '.mp3']
        # Добавьте другие общие данные

app_state = AppState()  # Глобальный экземпляр

def main(page: ft.Page):
    page.title = "Многостраничное приложение"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    def open_directory_dialog():
        # Создаем скрытое окно Tkinter
        root = Tk()
        root.withdraw()  # Скрываем основное окно
        root.attributes('-topmost', True)  # Поверх других окон
        
        # Открываем диалог выбора директории
        directory = filedialog.askdirectory(title="Выберите папку")
        
        if directory:  # Если папка выбрана
            app_state.selected_directory = directory  
            app_state.files = [f for f in os.listdir(app_state.selected_directory) if f.endswith('.mkv')]
            go_to_page(0)

    
    # Содержимое страниц
    def get_page_content(page_number):
        return ft.Column(
            controls=[
                ft.Text(f"Это Страница {page_number}", size=30, weight="bold"),
                ft.Text("Здесь может быть любой контент...", size=16),
                ft.ElevatedButton(
                    "Назад",
                    on_click=lambda e: go_to_page(0),  # Возврат на главную
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    
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
                        ft.ElevatedButton("Главная", on_click=lambda e: go_to_page(1)),
                        ft.ElevatedButton("Конвертер", on_click=lambda e: go_to_page(2)),
                        ft.ElevatedButton("Манифест", on_click=lambda e: go_to_page(3)),
                        ft.ElevatedButton("Запуск", on_click=lambda e: go_to_page(4)),
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
    
    # Функция переключения страниц
    def go_to_page(page_number):
        page.controls.clear()  # Очищаем текущий экран
        if page_number == 0:
            page.add(get_home_page())
        elif page_number == -1:
            page.add(create_project())
        else:
            page.add(get_page_content(page_number))
        page.update()
    
    # Стартовая страница

    def create_project():
        return ft.Column(
            controls=[
                ft.Text(f"Добро пожаловать в ABR Maker", size=30, weight="bold"),
                ft.Text("Выберите директорию для нового проекта", size=16),
                ft.ElevatedButton(
                    "Создать +",
                    on_click=lambda e: open_directory_dialog(),  # Возврат на главную
                ),
            ],
            alignment="center",
            horizontal_alignment="center",
        )

    go_to_page(-1)

ft.app(target=main)