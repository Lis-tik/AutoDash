import ffmpeg




def video_info(stream):
    data = {
        'width': stream.get('width'),
        'height': stream.get('height'),
        'pix_fmt': stream.get('pix_fmt', 'unknown'),
        'profile': stream.get('profile', 'unknown'),
        'is_avc': int('avc' in stream.get('codec_name', '').lower()),
        'status': 1
    }
    return data
    

def audio_info(stream, path=0):
    tags = stream.get('tags', {})  # Получаем мета-теги потока

    data = {
        'index': stream['index'],  # Индекс потока
        'codec_name': stream.get('codec_name', 'unknown'),  # Кодек
        'language': stream.get('tags', {}).get('language', 'unknown'),  # Язык (если есть)
        'title': tags.get('title', f'unknown'),  # Название дорожки (если есть)
        'channels': stream.get('channels', 'unknown'),  # Количество каналов
        'sample_rate': stream.get('sample_rate', 'unknown'),  # Частота дискретизации
        'bit_rate': stream.get('bit_rate', 'unknown'),  # Битрейт
        'status': 1,
        'path': path
    }
    return data

def subtitle_info(stream, path=0):
    data = {
        'format': stream.get('codec_name', 'unknown'),
        'language': stream.get('tags', {}).get('language', 'unknown'),
        'title':  stream.get('tags', {}).get('title', 'unknown'),
        # 'title': 'subs',
        'forced': int(stream.get('disposition', {}).get('forced', 0) == 1),
        'default': int(stream.get('disposition', {}).get('default', 0) == 1),
        'is_bitmap': int(stream.get('codec_name', '').lower() in ['dvd_subtitle', 'hdmv_pgs_subtitle', 'xsub']),
        'is_text': int(stream.get('codec_name', '').lower() in ['subrip', 'ass', 'ssa', 'mov_text', 'webvtt']),
        'status': 1,
        'path': path
    }
    return data
