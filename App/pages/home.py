import flet as ft
from App.storage import app_state
import App.router as rout
from tkinter import Tk, filedialog
import os



class ContentCheckbox(ft.Checkbox):
    def __init__(self, text):
        super().__init__()
        self.label = text
        self.on_change = self.get_data_file
        self.value = False
        
    def get_data_file(self, e):
        app_state.activeFilesHome.append(self.label) 
        app_state.new_page(rout.Page_Home)
        

class ModeButton(ft.ElevatedButton):
    def __init__(self, text, mode):
        super().__init__()
        self.text = text
        self.mode = mode
        self.on_click = self.infoModeTool

        self.active = True if app_state.infoMode == self.mode else False

        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=1),
            bgcolor=(ft.Colors.GREY_300 if self.active else ft.Colors.WHITE)
            )
    

    def infoModeTool(self, e):
        app_state.infoMode = self.mode
        app_state.new_page(rout.Page_Home)
        
    


class HomePageClasster:
    def __init__(self):
        self.data = app_state._mediainfo.info_main_lib[app_state.global_path]
        self.filesMain = [ContentCheckbox(f) for f in app_state.files]
        self.filesMain.insert(0, ft.ElevatedButton("Выборочный режим",on_click=lambda e: None))




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
                ft.Text(f"{app_state.activeFilesHome if app_state.activeFilesHome else 'Информация'}", size=20, weight="bold"),
                ft.Divider(height=1),
                ft.Row(   # кнопки сверху
                    [
                        ModeButton("Видео", 'video'),
                        ModeButton("Аудио", 'audio'),
                        ModeButton("Субтитры", 'subtitle')
                    ],
                    alignment="start",
                ),
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
        if not app_state.activeFilesHome:
            return ft.Container(
                content=ft.Row([ft.Text("Выберете файл для просмотра информации", size=15)])
            )
        
        info_page = []
        
        for value in self.data:
            if app_state.activeFilesHome[-1] in value['name']:
                for state in value[app_state.infoMode]:
                    if app_state.infoMode == 'audio':
                        textField = ft.Column([
                            ft.Row([
                                ft.Text("Описание (имя) аудиодорожки:", size=15),
                                ft.TextField(
                                    hint_text="Введите имя аудиодорожки",
                                    value=state['title'],  # Устанавливаем значение здесь
                                    width=300,
                                    height=40
                                )
                            ]),
                            ft.Row([
                                ft.Text(f"Индекс в контейнере:", size=15),
                                ft.Text(f"{state['index']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Язык аудиодорожки:", size=15),
                                ft.Text(f"{state['language']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Кодек аудиодорожки:", size=15),
                                ft.Text(f"{state['codec_name']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Количество каналов:", size=15),
                                ft.Text(f"{state['channels']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Битрейт:", size=15),
                                ft.Text(f"{state['bit_rate']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Источник:", size=15),
                                ft.Text(f"{state['path'] if state['path'] else '[в составе контейнера]'}", size=15, weight='bold'),
                            ]),
                            ft.Divider(height=1)
                        ])


                    elif app_state.infoMode == 'video':
                        textField = ft.Column([
                            ft.Row([
                                ft.Text(f"Разрешение сторон:", size=15),
                                ft.Text(f"{state['width']}x{state['height']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Тип цветопередачи:", size=15),
                                ft.Text(f"{state['pix_fmt']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Профиль:", size=15),
                                ft.Text(f"{state['profile']}", size=15, weight='bold'),
                            ]),
                            ft.Divider(height=1)
                        ])

                    
                    elif app_state.infoMode == 'subtitle':
                        textField = ft.Column([
                            ft.Row([
                                ft.Text("Описание (имя) субтитров:", size=15),
                                ft.TextField(
                                    hint_text="Введите имя субтитров",
                                    value=state['title'],  # Устанавливаем значение здесь
                                    width=300,
                                    height=40
                                )
                            ]),
                            ft.Row([
                                ft.Text(f"Язык субтитров:", size=15),
                                ft.Text(f"{state['language']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Формат:", size=15),
                                ft.Text(f"{state['format']}", size=15, weight='bold'),
                            ]),
                            ft.Row([
                                ft.Text(f"Источник:", size=15),
                                ft.Text(f"{state['path'] if state['path'] else '[в составе контейнера]'}", size=15, weight='bold'),
                            ]),
                            ft.Divider(height=1)
                        ])

                    info_page.append(textField)

        return ft.Container(
            content=ft.Column(info_page)
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
                on_click=lambda e: app_state.new_page(rout.Page_setting_converter),
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









     









