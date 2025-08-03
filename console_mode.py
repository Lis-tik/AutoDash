import os
import threading
from src.media_info import Info
from pathlib import Path
from src.control import start_converted


start_message = 'Github разработчика: https://github.com/Lis-tik \n' \
'Данная программа создана для комфортного перекодирования медиа контента под dash (hls). База - ffmpeg\n\n' \
'Перед началом работы программы, зполните файл конфигурации (config.txt) по шаблону\n' \
'Либо выберете режим Create для ручного заполнения\n'

print(start_message)

class Main:
    def __init__(self):
        self.global_path = None 
        self.main_data = None
        self.container_files = None
        self.additionally_audio = []

        self.subtitles_formats = ['.srt', '.ass', '.vtt', '.sub', '.ttml', '.pgs']
        self.height = [2160, 1440, 1080, 720, 480, 360]

    def format_control(self, file):
        for _ in self.subtitles_formats:
            return any(file.endswith(x) for x in self.subtitles_formats)
        
    def master_create(self):
        for x in range(100):
            file_path = Path(f"./options/master_{x}.json")
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write('{'+f'"{str(self.global_path).replace("\\", '/')}": [' + '\n')

                    for data in self.main_data[self.global_path][:-1]:
                        file.write(str(data).replace("'", '"') + ',' + '\n')
                    file.write(str(self.main_data[self.global_path][-1]).replace("'", '"') + '\n')
                    file.write(']}')
                break
        self.workspace()

    def workspace(self):
        Path(f'{self.global_path}/converted').mkdir(parents=True, exist_ok=True)
        for ind in range(len(self.main_data[self.global_path])):
            path_nm = self.main_data[self.global_path][ind]

            Path(f'{self.global_path}/converted/series_{ind+1}/subtitle').mkdir(parents=True, exist_ok=True)    

            for audio in path_nm['audio']:
                Path(f'{self.global_path}/converted/series_{ind+1}/audio/{audio['title']}').mkdir(parents=True, exist_ok=True)

            qualitie = int(path_nm['video'][0]['height'])
            for video in self.height:
                if qualitie >= video:
                    Path(f'{self.global_path}/converted/series_{ind+1}/video/{video}p').mkdir(parents=True, exist_ok=True)

        


            


    def start(self):
        mode = int(input('1. Create\n2. Editing \n3. Start\n4. Exit\n:'))
        if mode == 1:
            print('Включен режим создания dash проекта')
            self.manual_mode()
        elif mode == 3:
            print('Включен режим редактирования готового dash проекта')
            start_converted()


    def manual_mode(self):

        self.global_path = input('Шаг №1\nВведите полный путь к основной директории с проектом\n:')
        self.container_files = [f'{self.global_path}\{f}' for f in os.listdir(self.global_path) if (f.endswith('.mkv'))]
        print(f'В директории [{self.global_path}]: \n')

        info_main_video = Info()
        info_main_video.start_getinfo(self.container_files, self.global_path)
        self.main_data = info_main_video.info_main_lib

        # for value in self.main_data:
        #     print(value)

        print(info_main_video.summary_data())

        print('Шаг №2')
        while True:
            aud_lt = input('\nДобавьте дополнительные файлы с аудиодорожками (mka и т.п.)\nНажмите [ENTER], чтобы пропустить\n:')
            
            if not aud_lt:
                break

            temp_list = [f'{aud_lt}\{f}' for f in os.listdir(aud_lt)]
            info_main_video.update_chanel(temp_list)


        print('Шаг №3')
        while True:
            sub_lt = input('\nДобавьте дополнительные файлы с субтитрами (ass, aas и т.п.)\nНажмите [ENTER], чтобы пропустить\n:')
            
            if not sub_lt:
                break
            
            temp_list = [f'{sub_lt}\{f}' for f in os.listdir(sub_lt) if (self.format_control(f))]
            info_main_video.update_chanel(temp_list)

        self.main_data = info_main_video.info_main_lib
        print(info_main_video.summary_data(), '\n')

        while True:
            print('Сборка готова к работе\n1. Старт\n2. Редактировать рабочее пространство')
            mode_last = int(input(':'))
            if mode_last == 1:
                self.master_create()
                start_converted()

            if mode_last == 2:
                self.main_data = info_main_video.edit_workspace()
                self.main_data = info_main_video.info_main_lib
                print(info_main_video.summary_data(), '\n')
    



if __name__ == '__main__':
    app = Main()
    app.start()

