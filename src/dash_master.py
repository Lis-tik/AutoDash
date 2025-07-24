import subprocess
from src.xml_master import MakerMPD



class ReadyVideoConfiguration:
    def __init__(self):
        self.path = None
        self.data = None
        self.qualities = []
        self.speed = 4
        self.segment_time = 2
        

    def qualities_calculation(self):
        self.qualities = [
            {'access': 0, 'name': '2160p', 'width': 3840, 'height': 2160, 'vf': 'scale=-2:2160', 'b:v': '35000k', 'crf': '20'},
            {'access': 0, 'name': '1440p', 'width': 2560, 'height': 1440, 'vf': 'scale=-2:1440', 'b:v': '12000k', 'crf': '22'},
            {'access': 0, 'name': '1080p', 'width': 1920, 'height': 1080, 'vf': 'scale=-2:1080', 'b:v': '8000k', 'crf': '24'},
            {'access': 0, 'name': '720p', 'width': 1280, 'height': 720, 'vf': 'scale=-2:720', 'b:v': '5000k', 'crf': '26'},
            {'access': 0, 'name': '480p', 'width': 854, 'height': 480, 'vf': 'scale=-2:480', 'b:v': '2500k', 'crf': '28'},
            {'access': 0, 'name': '360p', 'width': 640, 'height': 360, 'vf': 'scale=-2:360', 'b:v': '1200k', 'crf': '30'}
        ]
        
        for read_q in self.qualities:
            if self.data['video'][-1]['height'] >= read_q['height']:
                read_q['access'] = 1


    def start(self, global_path, data):
        self.data = data
        self.qualities_calculation()

        print(self.qualities)

        self.path = f'{global_path}/converted/series_{data['index']}'

        for quality in self.qualities:
            if quality['access']:
                cmd = [
                    'ffmpeg',
                    '-i', f'{data['name']}',  # Входной файл
                    '-c:v', 'libsvtav1',  # Кодек
                    '-preset', str(self.speed),  # Скорость/качество
                    '-crf', str(quality['crf']),  # Качество (CRF)
                    '-pix_fmt', str(data['video'][-1]['pix_fmt']),  # Формат пикселей

                    '-an', '-sn',  # Без аудио и субтитров
                    '-f', 'dash',  # Формат вывода (DASH)

                    '-seg_duration', str(self.segment_time),  # Длительность сегментов
                    '-use_timeline', '1',  # Включить временную шкалу
                    '-init_seg_name', 'init.mp4',                          # инициализационный сегмент
                    '-media_seg_name', 'segment_$Number%05d$.m4s',         # аудиосегменты

                    '-g', '240',
                    '-svtav1-params', 'tune=0:film-grain=8',
                    '-vf', f'{quality['vf']}:flags=lanczos',
                    f"{global_path}/converted/series_{data['index']}/video/{quality['name']}/video.mpd"  # Выходной файл
                ]

                try:
                    subprocess.run(cmd, check=True, text=True) # capture_output=True
                except subprocess.CalledProcessError as e:
                    print(f"Ошибка FFmpeg: {e.stderr}")


        for x in range(len(data['subtitle'])):
            option = data['subtitle'][x]
            name = option['title']
            if option['path']:
                input = data['subtitle'][x]['path']
            else:
                input = data['name']

            cmd = [
                'ffmpeg',
                '-i', f'{input}',
                '-map', f'0:s:{x}',  # Первый поток субтитров
                '-codec', 'ass',  # Явно указываем кодек ASS
                '-f', 'ass',       # Формат выходного файла
                f'{global_path}/converted/series_{data['index']}/subtitle/{name}.ass'
            ]
            
            
            try:
                subprocess.run(cmd, check=True, text=True) # capture_output=True
            except subprocess.CalledProcessError as e:
                print(f"Ошибка FFmpeg: {e.stderr}")



        for x in range(len(data['audio'])):
            option = data['audio'][x]
            name = option['title']
            if option['path']:
                input = data['audio'][x]['path']
            else:
                input = data['name']

            cmd = [
                'ffmpeg',
                '-i', f'{input}',
                '-map', f'0:a:{x}',  # Выбираем аудиопоток по индексу x


                '-ac', '2',  # Устанавливаем количество аудиоканалов
                '-codec', 'aac',     # Кодек аудио (можно изменить на нужный)

                '-sn',  # без субтитров
                '-vn',  # без видео

                '-af', 'aresample=async=1',
                '-f', 'dash',        # Формат выходного файла - DASH
                '-seg_duration', str(self.segment_time), # Длительность сегмента в секундах
                '-frag_type', 'every_frame',
                # '-dash_segment_type', 'mp4',
                f"{global_path}/converted/series_{data['index']}/audio/{name}/output.mpd"
            ]

                        
            
            try:
                subprocess.run(cmd, check=True, text=True) # capture_output=True
            except subprocess.CalledProcessError as e:
                print(f"Ошибка FFmpeg: {e.stderr}")

        mpd = MakerMPD(self.path)
        mpd.main_control()