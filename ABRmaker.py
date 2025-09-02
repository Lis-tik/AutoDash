import flet as ft

from App.storage import app_state
import App.router as rout
import asyncio


def main(page_control: ft.Page):
    app_state.new_page(rout.Page_Open)
    
    # Инициализация заголовка
    page_control.title = app_state.page.title
    page_control.update()  # ← Важно!

    page_control.vertical_alignment = "center"
    page_control.horizontal_alignment = "center"


    async def mainApp():
        while True: 
            if app_state.transition:
                await control()
                page_control.title = app_state.page.title
                app_state.transition = False
                
            await asyncio.sleep(0.1)


    # Функция переключения страниц
    async def control():
        page_control.controls.clear()  # Очищаем текущий экран
        page_control.add(app_state.page.link())
        page_control.update()

    # Запуск асинхронных задач

    page_control.loop.create_task(mainApp())


    

ft.app(target=main)