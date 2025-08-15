import flet as ft
from tkinter import Tk, filedialog

from App.storage import app_state
import App.router as rout

import threading
import time


def main(page_control: ft.Page):
    page_control.title = "Многостраничное приложение"
    page_control.vertical_alignment = "center"
    page_control.horizontal_alignment = "center"



    def expectation():
        while not app_state.files:
            time.sleep(0.5)
        control(rout.Page_Home.link())


    # Функция переключения страниц
    def control(pageData):
        page_control.controls.clear()  # Очищаем текущий экран
        page_control.add(pageData)
        page_control.update()

    t1 = threading.Thread(target=expectation)
    t1.start()

    control(rout.Page_Open.link())
    

ft.app(target=main)