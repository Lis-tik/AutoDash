cmd = [
    'ffmpeg',
    '-i', f'{data['name']}',  # Входной файл
    '-map', '0:v:0',  # Берём только первый видеопоток
    '-c:v', 'libsvtav1',  # Кодек
    '-preset', str(self.speed),  # Скорость/качество
    '-crf', str(quality['crf']),  # Качество (CRF)
    '-pix_fmt', str(data['video'][-1]['pix_fmt']),  # Формат пикселей

    '-dn', '-an', '-sn',  # Игнорируем данные, аудио и субтитры
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