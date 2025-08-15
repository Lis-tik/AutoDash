

class AppState:
    def __init__(self):
        self.selected_directory = None
        self._files  = []
        self.page = -1
        self.project_name = "Мой проект"

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, new_value):
        print(f"Переменная изменилась: {self._files} -> {new_value}")
        self._files = new_value
        
app_state = AppState()  # Глобальный экземпляр