import flet as ft
from App.storage import app_state
import App.router as rout



class ContentButton(ft.ElevatedButton):
    def __init__(self, text, on_click):
        super().__init__()
        self.text = text
        self.on_click = on_click

        self.active = False
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=1))


def get_data_file(name):
    temp = app_state._mediainfo.info_main_lib[app_state.global_path]
    for index, value in enumerate(temp):
        if name in value['name']:
            app_state.transition = True
            info_text_ref.current.value = f"Детали:\n{value}"
            break



    

info_text_ref = ft.Ref[ft.Text]()

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
                    ft.Container(
                        content=ft.Column(
                            controls=[ContentButton(f, on_click=lambda e: get_data_file(f)) for f in app_state.files],
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        expand=True,  # Занимает вторую половину ширины Row
                        border=ft.border.all(1, ft.Colors.GREY_400),
                        border_radius=10,
                        padding=10,
                        margin=ft.margin.symmetric(vertical=10),
                    ),
                    
                    # Левый блок - информационная панель
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Информация", size=20, weight="bold"),
                            ft.Divider(height=1),
                            ft.Text(ref=info_text_ref, size=16)
                        ]),
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