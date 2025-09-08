import flet as ft
from App.storage import app_state
import App.router as rout
from tkinter import Tk, filedialog
import os



class ContentButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.text = text
        self.on_click = on_click

        self.active = True if app_state.activeFileHome == text else False
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=1))




class HomePageClasster:
    def __init__(self):
        self.data = app_state._mediainfo.info_main_lib[app_state.global_path]
        self.newData = None
        self.filesMain = [ContentButton(f, on_click=lambda e, file=f: self.get_data_file(file)) for f in app_state.files]
        self.info_page = []


    def data_currected(self, active):
        return
            


    def get_data_file(self, name):
        app_state.activeFileHome = name
        app_state.new_page(rout.Page_Home)


    def open_directory_dialog(self, mode):
        root = Tk()
        root.withdraw()  # Скрываем основное окно
        root.attributes('-topmost', True)  # Поверх других окон
        
        # Открываем диалог выбора директории
        directory = filedialog.askdirectory(title="Выберите папку")

        if directory:  # Если папка выбрана
            app_state.global_path = directory
            app_state.files = [f for f in os.listdir(directory)]


    def Information(self):
        return ft.Row(
            controls=[                    
                # Правый блок - список файлов
                ft.Column(
                    controls = [
                        ft.Container(
                            content=ft.Column(
                                controls=self.filesMain,
                                spacing=10,
                                scroll=ft.ScrollMode.AUTO,
                            ),
                            expand=True,  # Занимает вторую половину ширины Row
                            border=ft.border.all(1, ft.Colors.GREY_400),
                            border_radius=10,
                            padding=10,
                            margin=ft.margin.symmetric(vertical=10),
                        ),
                    ]
                ),
                self.metaData()
            ],
            expand=True,  # Row растягивается на всю доступную ширину
            spacing=10,   # Расстояние между блоками
            vertical_alignment=ft.CrossAxisAlignment.START  # ← Ключевой параметр!
        )
    
    def metaData(self):
        return ft.Container(
            content=ft.Column([
                ft.Row(   # кнопки сверху
                    [
                        ft.ElevatedButton("Добавить аудиодорожку", on_click=lambda e: self.open_directory_dialog('audio')),
                        ft.ElevatedButton("Добавить субтитры", on_click=lambda e: self.open_directory_dialog('subtitle'))
                    ],
                    alignment="start",
                ),
                ft.Text("Информация", size=20, weight="bold"),
                ft.Divider(height=1),
                self.distributionData()
            ],
            scroll=ft.ScrollMode.AUTO,
            ),
            padding=20,
            bgcolor=ft.Colors.BLUE_GREY_50,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=2),
            expand=True,  # Занимает половину ширины Row
        )
    
    def distributionData(self):
        if not app_state.activeFileHome:
            return ft.Container(
                content=ft.Row([ft.Text("Выберете файл для просмотра информации", size=15)])
            )
        
        for value in self.data:
            if app_state.activeFileHome in value['name']:
                for audio in value['audio']:
                    
                    textField = ft.Row([
                        ft.Text("Описание (имя) аудиодорожки:", size=15),
                        ft.TextField(
                            hint_text="Введите имя аудиодорожки",
                            value=audio['title'],  # Устанавливаем значение здесь
                            width=300
                        )
                    ])
                    self.info_page.append(textField)

        return ft.Container(
            content=ft.Column(self.info_page)
        )





def navigation():
    return ft.Row(  # Лучше адаптируется для мобильных устройств
        controls=[
            ft.ElevatedButton(
                "Главная",
                on_click=lambda e: app_state.new_page(rout.multipage(1)),
            ),
            ft.ElevatedButton(
                "Конвертер", 
                on_click=lambda e: app_state.new_page(rout.multipage(2)),
            ),
            ft.ElevatedButton(
                "Манифест",
                on_click=lambda e: app_state.new_page(rout.multipage(3)),
            ),
            ft.ElevatedButton(
                "Запуск",
                on_click=lambda e: app_state.new_page(rout.multipage(4)),
            ),
        ],
        spacing=10,
        run_spacing=10,  # Перенос на новую строку при нехватке места
    )

def Label():
    return ft.Container(
        content=ft.Text("ABR Maker", size=30, weight='bold'),
        padding=5,
    )

def get_home_page():
    homePage = HomePageClasster()
    return ft.Column(
        controls=[
            Label(),
            navigation(),
            homePage.Information(),
        ],
        expand=True,
        spacing=20,
    )









     









