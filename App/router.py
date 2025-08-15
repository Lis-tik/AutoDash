
from App.pages.open import create_project
from App.pages.home import get_home_page
from App.pages.multi_page import get_page_content


class Router:
    def __init__(self, page, link, title, data=None):
        self.page = page
        self.link = link
        self.title = title
        self.data = data

    def routdata(self, data):
        self.data = data


Page_Open = Router(1, create_project, 'Создайте проект!')
Page_Home = Router(2, get_home_page, 'Домашняя страница')
Page_Multi = Router(3, get_page_content, 'Страница')
