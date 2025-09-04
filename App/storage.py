from src.media_info import Info



class AppState:
    def __init__(self):
        self._files  = []
        self.page = None

        self.global_path = None
        self._transition = False
        self.project_name = "Мой проект"
        self.audio_formats = ['.mkv', '.mka', 'mp4']
        self.subtitles_formats = ['.srt', '.ass', '.vtt', '.sub', '.ttml', '.pgs']


        self._mediainfo = Info()


    def new_page(self, new_page):
        self.page = new_page
        self.transition = True
    
    @property
    def falg_transition(self):
        return self._transition
    
    @falg_transition.setter
    def transition(self, new_value):
        print(f"Переход на новую страницу: {self._transition} -> {new_value}")
        self._transition = new_value



    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, new_value):
        self._files = new_value

        info_list = []
        for i in new_value:
            info_list.append(f'{self.global_path}/{i}') 

        self._mediainfo.start_getinfo(info_list, self.global_path)
        print(self._mediainfo.summary_data())
        
    
        
app_state = AppState()  # Глобальный экземпляр
