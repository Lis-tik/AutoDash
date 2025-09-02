import subprocess
from src.xml_master import MakerMPD



class ReadyVideoConfiguration:
    def __init__(self):
        self.path = None
        self.data = None
        self.qualities = []
        self.speed = 'slow'
        # self.speed = 4
        self.segment_time = 5
        

    def qualities_calculation(self):
        self.qualities = [
            {'access': 0, 'name': '2160p', 'width': 3840, 'height': 2160, 'vf': 'scale=-2:2160', 'b:v': '35000k', 'crf': '15'},
            {'access': 0, 'name': '1440p', 'width': 2560, 'height': 1440, 'vf': 'scale=-2:1440', 'b:v': '12000k', 'crf': '17'},
            {'access': 0, 'name': '1080p', 'width': 1920, 'height': 1080, 'vf': 'scale=-2:1080', 'b:v': '8000k', 'crf': '19'},
            {'access': 0, 'name': '720p', 'width': 1280, 'height': 720, 'vf': 'scale=-2:720', 'b:v': '5000k', 'crf': '24'},
            {'access': 0, 'name': '480p', 'width': 854, 'height': 480, 'vf': 'scale=-2:480', 'b:v': '2500k', 'crf': '26'},
            {'access': 0, 'name': '360p', 'width': 640, 'height': 360, 'vf': 'scale=-2:360', 'b:v': '1200k', 'crf': '28'}
        ]
        
        for read_q in self.qualities:
            if int(self.data['video'][0]['height']) >= int(read_q['height']):
                read_q['access'] = 1

        

        


    def start(self, global_path, data):
        self.data = data
        self.qualities_calculation()


        self.path = f'{global_path}/converted/series_{data['index']}'

        for quality in self.qualities:
            if quality['access']:
                cmd = [
                    'ffmpeg',
                    '-hwaccel', 'cuda',
                    '-hwaccel_output_format', 'cuda',

                    '-i', f"{data['name']}",

                    '-map', '0:v:0',
                    '-c:v', 'hevc_nvenc',
                    '-preset', str(self.speed),
                    '-profile:v', 'main10',
                    '-pix_fmt', 'p010le',
                    '-cq', str(quality['crf']),

                    '-dn', '-an', '-sn',
                    '-f', 'dash',
                    '-seg_duration', str(self.segment_time),
                    '-use_timeline', '1',
                    '-init_seg_name', 'init.mp4',
                    '-media_seg_name', 'segment_$Number%05d$.m4s',

                    '-g', '240',
                    '-vf', f'scale_cuda={quality['width']}:{quality['height']}:format=p010,hwdownload,format=p010le',
                    f"{global_path}/converted/series_{data['index']}/video/{quality['name']}/video.mpd"
                ]







                try:
                    subprocess.run(cmd, check=True, text=True) # capture_output=True
                except subprocess.CalledProcessError as e:
                    print(f"Ошибка FFmpeg: {e.stderr}")


        for x in range(len(data['subtitle'])):
            option = data['subtitle'][x]
            name = option['title']
            if option['path']:
                chanel_const = 0
                input = data['subtitle'][x]['path']
            else:
                chanel_const = x
                input = data['name']

            cmd = [
                'ffmpeg',
                '-i', f'{input}',
                '-map', f'0:s:{chanel_const}',  # Первый поток субтитров
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
                '-map', f'0:a:{option['index']}',  # Выбираем аудиопоток по индексу x


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