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

        self.active = False
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=1))



def open_directory_dialog(mode):
    root = Tk()
    root.withdraw()  # Скрываем основное окно
    root.attributes('-topmost', True)  # Поверх других окон
    
    # Открываем диалог выбора директории
    directory = filedialog.askdirectory(title="Выберите папку")

    if directory:  # Если папка выбрана
        app_state.global_path = directory
        app_state.files = [f for f in os.listdir(directory)]




def text_currected(data, name):   
    Text = (f"{name}\n\nДетали:\nНомер в сборнике: №{data['index']}\nПолный путь: {data['name']}\n\nДанные видодорожек:\n")

    for video in data['video']:
        Text += f'Разрешение сторон: {video['width']}x{video['height']}\nФормат цветопередачи: {video['pix_fmt']}\nПрофиль: {video['profile']}\n\n'
    info_video_ref.current.value = Text

    Text = 'Данные аудиодорожек:\n'
    for audio in data['audio']:
        Text += f'Индекс: {audio['index']}\nОписание (имя): {audio['title']}\nЯзык: {audio['language']}\nКодек: {audio['codec_name']}\nКоличество каналов: {audio['channels']}\nБитрейт: {audio['bit_rate']}'
        if int(audio['path']):
            Text += f'\nПуть к директории: {audio['path']}'
        Text += '\n\n'
        
    info_audio_ref.current.value = Text

    Text = 'Данные субтитров:\n'
    for subtitle in data['subtitle']:
        Text += f'писание (имя): {subtitle['title']}\nЯзык: {subtitle['language']}\nФормат: {subtitle['format']}'
        if int(subtitle['path']):
            Text += f'\nПуть к директории: {subtitle['path']}'
        Text += '\n\n'

    info_subtitle_ref.current.value = Text
    


def get_data_file(name):
    temp = app_state._mediainfo.info_main_lib[app_state.global_path]
    for index, value in enumerate(temp):
        if name in value['name']:
            text_currected(value, name)
            for dtref in data_ref:
                dtref.current.update()
            break

info_video_ref = ft.Ref[ft.Text]()
info_audio_ref = ft.Ref[ft.Text]()
info_subtitle_ref = ft.Ref[ft.Text]()
data_ref = [info_video_ref, info_audio_ref, info_subtitle_ref]


def get_home_page():
    return ft.Column(
        controls=[
            # Заголовок
            ft.Container(
                content=ft.Text("ABR Maker", size=30, weight='bold'),
                padding=5,
            ),
            
            # Навигационная панель
            ft.Row(  # Лучше адаптируется для мобильных устройств
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
            ),
            
            # Информационная панель (занимает 100% ширины)
            ft.Row(
                controls=[                    
                    # Правый блок - список файлов
                    ft.Column(
                        controls = [
                            ft.ElevatedButton("Режим изменения для ВСЕХ МЕДИАФАЙЛОВ", on_click=lambda e: None),
                            ft.Container(
                                content=ft.Column(
                                    controls=[ContentButton(f, on_click=lambda e, file=f: get_data_file(file)) for f in app_state.files],
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
                    
                    # Левый блок - информационная панель
                    ft.Container(
                        content=ft.Column([
                            ft.Row(   # кнопки сверху
                                [
                                    ft.ElevatedButton("Изменить метаданные", on_click=lambda e: None),
                                    ft.ElevatedButton("Добавить аудиодорожку", on_click=lambda e: open_directory_dialog('audio')),
                                    ft.ElevatedButton("Добавить субтитры", on_click=lambda e: open_directory_dialog('subtitle'))
                                ],
                                alignment="start",
                            ),
                            ft.Text("Информация", size=20, weight="bold"),
                            ft.Divider(height=1),
                            ft.Text(ref=info_video_ref, size=16),
                            ft.Divider(height=1),
                            ft.Text(ref=info_audio_ref, size=16),
                            ft.Divider(height=1),
                            ft.Text(ref=info_subtitle_ref, size=16)
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=20,
                        bgcolor=ft.Colors.BLUE_GREY_50,
                        border_radius=15,
                        shadow=ft.BoxShadow(blur_radius=2),
                        # margin=ft.margin.symmetric(vertical=10),
                        expand=True,  # Занимает половину ширины Row
                    ),
                ],
                expand=True,  # Row растягивается на всю доступную ширину
                spacing=10,   # Расстояние между блоками
                vertical_alignment=ft.CrossAxisAlignment.START  # ← Ключевой параметр!
            )
        ],
        expand=True,
        spacing=20,
        # scroll=ft.ScrollMode.AUTO,  # Основная прокрутка страницы
    )